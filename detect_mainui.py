"""
@Auth ： 挂科边缘
@IDE ：PyCharm
@Motto:学习新思想，争做新青年
@Email ：179958974@qq.com
@qq ：179958974
"""

from pprint import pprint
from ultralytics import YOLO
from ultralytics.data.loaders import LoadStreams
from ultralytics.engine.predictor import BasePredictor
from ultralytics.utils import DEFAULT_CFG, SETTINGS
from ultralytics.utils.torch_utils import smart_inference_mode
from ultralytics.utils.files import increment_path
from ultralytics.cfg import get_cfg
from ultralytics.utils.checks import check_imshow
from PySide6.QtCore import Signal, QObject
from pathlib import Path
import datetime
import numpy as np
import time
import cv2
from main_utils import check_path

x_axis_time_graph = []
y_axis_count_graph = []
video_id_count = 0


class YoloPredictor(BasePredictor, QObject):
    yolo2main_trail_img = Signal(np.ndarray)
    yolo2main_box_img = Signal(np.ndarray)
    yolo2main_status_msg = Signal(str)  # 检测/暂停/停止等信号
    yolo2main_fps = Signal(str)

    yolo2main_labels = Signal(dict)
    yolo2main_progressBar = Signal(int)
    yolo2main_class_num = Signal(int)
    yolo2main_target_num = Signal(int)


    def __init__(self, cfg=DEFAULT_CFG, overrides=None):
        super(YoloPredictor, self).__init__()
        QObject.__init__(self)

        try:
            self.args = get_cfg(cfg, overrides)
        except:
            pass
        project = self.args.project or Path(SETTINGS['runs_dir']) / self.args.task
        name = f'{self.args.mode}'
        self.save_dir = increment_path(Path(project) / name, exist_ok=self.args.exist_ok)
        self.done_warmup = False
        if self.args.show:
            self.args.show = check_imshow(warn=True)


        self.used_model_name = None
        self.new_model_name = None  # 新更改的模型

        self.source = ''
        self.progressBar_value = 0

        self.stop_dtc = False  # 终止bool
        self.continue_dtc = True  # 暂停bool


        # config
        self.iou_thres = 0.7  # iou
        self.conf_thres = 0.25  # conf
        self.speed_thres = 0.01  # delay, ms （缓冲）

        self.save_res = False  # 保存MP4
        self.save_txt = False  # 保存txt
        self.save_res_path = "pre_result"
        self.save_txt_path = "pre_labels"

        self.show_labels = True  # 显示图像标签bool



        # 运行时候的参数放这里
        self.start_time = None # 拿来算FPS的计数变量
        self.count = None
        self.sum_of_count = None
        self.class_num = None
        self.total_frames = None
        self.lock_id = None


    # 点击开始检测按钮后的检测事件
    @smart_inference_mode()  # 一个修饰器，用来开启检测模式：如果torch>=1.9.0，则执行torch.inference_mode()，否则执行torch.no_grad()
    def run(self):
        self.yolo2main_status_msg.emit('正在加载模型...')
        LoadStreams.capture = ''
        self.count = 0
        self.start_time = time.time()
        global video_id_count

        # 检查保存路径
        if self.save_txt:
            check_path(self.save_txt_path)
        if self.save_res:
            check_path(self.save_res_path)

        model = self.load_yolo_model()

        # 获取数据源 （不同的类型获取不同的数据源）
        iter_model = iter(model.track(source=self.source, show=False, stream=True, iou=self.iou_thres, conf=self.conf_thres))

        # 折线图数据初始化
        global x_axis_time_graph, y_axis_count_graph
        x_axis_time_graph = []
        y_axis_count_graph = []

        self.yolo2main_status_msg.emit('检测中...')

        # 使用OpenCV读取视频——获取进度条
        if 'mp4' in self.source or 'avi' in self.source or 'mkv' in self.source or 'flv' in self.source or 'mov' in self.source:
            cap = cv2.VideoCapture(self.source)
            self.total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            cap.release()

        # 如果保存，则创建写入对象
        img_res, result, height, width = self.recognize_res(iter_model)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = None  # 视频写出变量
        if self.save_res:
            out = cv2.VideoWriter(f'{self.save_res_path}/video_result_{video_id_count}.mp4', fourcc, 25,
                                  (width, height), True)  # 保存检测视频的路径

        # 开始死循环检测
        while True:
            try:
                # 暂停与开始
                if self.continue_dtc:
                    img_res, result, height, width = self.recognize_res(iter_model)
                    self.res_address(img_res, result, height, width, model, out)

                # 终止
                if self.stop_dtc:
                    if self.save_res:
                        if out:
                            out.release()
                            video_id_count += 1
                    self.source = None
                    self.yolo2main_status_msg.emit('检测终止')
                    self.release_capture()
                    break


            # 检测截止（本地文件检测）
            except StopIteration:
                if self.save_res:
                    out.release()
                    video_id_count += 1
                    print('writing complete')
                self.yolo2main_status_msg.emit('检测完成')
                self.yolo2main_progressBar.emit(100)
                cv2.destroyAllWindows()  # 单目标追踪停止！
                self.source = None

                break
        try:
            out.release()
        except:
            pass

    # 进行识别——并返回所有结果
    def res_address(self, img_res, result, height, width, model, out):
            # 复制一份
            img_box = np.copy(img_res)   # 右边的图（会绘制标签！） img_res是原图-不会受影响
            img_trail = np.copy(img_res) # 左边的图

            # 如果没有识别的：
            if result.boxes.id is None:
                # 目标都是0
                self.sum_of_count = 0
                self.class_num = 0
                labels_write = "暂未识别到目标！"
            # 如果有识别的
            else:

                # id = detections.tracker_id  # id
                # xyxy = detections.xyxy  # 位置
                # for class_id in detections.class_id:
                #     if class_id == 0:
                #         self.sum_of_count += 1  # 目标总数


                img_trail = img_res  # 显示原图


                img_box = result.plot()


                id = result.boxes.id.tolist()
                self.id = [int(j) for j in id]

                coordinates = result.boxes.xyxy.tolist()
                self.coordinates = [list(map(int, e)) for e in coordinates]

                cls_list = result.boxes.cls.tolist()
                self.cls_list = [int(i) for i in cls_list]

                self.names = model.names

                self.conf_list = result.boxes.conf.tolist()
                self.conf_list = ['%.2f %%' % (each * 100) for each in self.conf_list]

                self.yolo2main_tabel_show.emit(self.id, self.coordinates, self.cls_list, self.conf_list,self.names,self.source)


            # 预测视频写入本地
            if self.save_res:
                out.write(img_box)

            # 传递信号给主窗口
            self.emit_res(img_trail, img_box)

    # 识别结果处理
    def recognize_res(self, iter_model):
            # 检测 ---然后获取有用的数据
            result = next(iter_model)  # 这里是检测的核心，每次循环都会检测一帧图像,可以自行打印result看看里面有哪些key可以用
            img_res = result.orig_img  # 原图
            height, width, _ = img_res.shape

            return img_res, result, height, width



    # 信号发送区
    def emit_res(self, img_trail, img_box):

        time.sleep(self.speed_thres/1000)  # 缓冲
        # 轨迹图像（左边）
        self.yolo2main_trail_img.emit(img_trail)
        # 标签图（右边）
        self.yolo2main_box_img.emit(img_box)
        # 总类别数量 、 总目标数
        self.yolo2main_class_num.emit(self.class_num)
        self.yolo2main_target_num.emit(self.sum_of_count)
        # 进度条
        if '0' in self.source or '1' in self.source or 'rtsp' in self.source:
            self.yolo2main_progressBar.emit(0)

        if 'avi' in self.source or 'mp4' in self.source:
            self.progressBar_value = int(self.count / self.total_frames * 100)
            self.yolo2main_progressBar.emit(self.progressBar_value)

        # 计算FPS
        self.count += 1
        if self.count % 3 == 0 and self.count >= 3:  # 计算FPS
            self.yolo2main_fps.emit(str(int(3 / (time.time() - self.start_time))))
            self.start_time = time.time()

    # 加载模型
    def load_yolo_model(self):
        if self.used_model_name != self.new_model_name:
            self.setup_model(self.new_model_name)
            self.used_model_name = self.new_model_name
            print('加载成功')
            self.model = YOLO(self.new_model_name)
            self.model = (np.zeros((48, 48, 3)))  # 预先加载推理模型

        return YOLO(self.new_model_name)



    # 获取类别数
    def get_class_number(self, detections):
        class_num_arr = []
        for each in detections.class_id:
            if each not in class_num_arr:
                class_num_arr.append(each)
        return len(class_num_arr)

    # 释放摄像头
    def release_capture(self):
        LoadStreams.capture = 'release'