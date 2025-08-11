import os
import sys

from heatmap import yolov8_heatmap
from message import DialogOver

sys.path.append('ui')
import cv2
import numpy as np
from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide6.QtGui import QImage, QPixmap, QGuiApplication, QPalette, \
    QBrush
from PySide6.QtCore import Qt




from detect_mainui import YoloPredictor

from detect_ui_v3 import Ui_MainWindow
from main_utils import check_url


class HeatmapThread(QThread):
    heatmap_signal = Signal(str)

    def __init__(self, img_path, params, save_dir):
        super().__init__()
        self.img_path = img_path
        self.params = params
        self.save_dir = save_dir

    def run(self):
        try:
            os.makedirs(self.save_dir, exist_ok=True)
            heatmap_generator = yolov8_heatmap(**self.params)
            save_path = os.path.join(self.save_dir, os.path.basename(self.img_path))
            heatmap_generator(self.img_path, save_path)
            result_path = os.path.join(save_path, 'result.png')
            self.heatmap_signal.emit(result_path)
        except Exception as e:
            print(f"热力图生成错误: {str(e)}")
            self.heatmap_signal.emit(None)


class DetectMain(QMainWindow, Ui_MainWindow):

    main2yolo_begin_sgl = Signal()
    def __init__(self, parent=None):
        super(DetectMain, self).__init__(parent)

        self.setupUi(self)  # 初始化界面


        #palette = QPalette()
        #palette.setBrush(QPalette.Window, QBrush(QPixmap("52DB360E999F65B5A6D3390BAE2914B4.jpg")))
        #self.setPalette(palette)

        self.yolo_init()  # 实例化YOLO

        # 主要功能绑定
        self.main_function_bind()
        self.pushButton_start_stop.setCheckable(True)  # 将按钮设置为开关状态为真

        self.yolo_predict.new_model_name = r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/runs/train/11-V+L+BRA/weights/best.pt'
        print(self.yolo_predict.new_model_name)

        self.yolo_predict.load_yolo_model()

    def yolo_init(self):
        # Yolo-v8 thread  初始化
        '''

        '''
        self.yolo_predict = YoloPredictor()
        self.yolo_thread = QThread()
        # 将 Yolo 类中的信号绑定到主线程的槽函数上
        # # 显示预测视频（左，右）
        self.yolo_predict.yolo2main_trail_img.connect(lambda x: self.show_image(x, self.label, 'img'))  # 绑定原始图

        self.yolo_predict.yolo2main_box_img.connect(lambda x: self.show_image(x, self.label_14, 'img'))  # 绑定结果图


        # 将主线程的信号绑定到 Yolo 类的槽函数上，并启动 Yolo 线程
        self.yolo_predict.moveToThread(self.yolo_thread)
        self.main2yolo_begin_sgl.connect(self.yolo_predict.run)
        self.yolo_predict.yolo2main_status_msg.connect(lambda x: self.show_status(x))

        # 热力图参数
        self.heatmap_params = {
            'weight': r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/runs/train/11-V+L+BRA/weights/best.pt',
            'device': 'cuda:0',
            'method': 'HiResCAM',
            'layer': [10, 12, 14, 16, 18],
            'backward_type': 'class',
            'conf_threshold': 0.2,
            'ratio': 0.02,
            'show_box': False,
            'renormalize': True
        }

    # 主页面各功能绑定
    def main_function_bind(self):
        # 打开文件夹
        self.pushButton_openimg.clicked.connect(self.open_src_file)
        self.pushButton_start_stop_2.clicked.connect(self.generate_heatmap)
        # 开始
        self.pushButton_start_stop.clicked.connect(self.run_or_continue)
        # 终止
        self.pushButton_exit.clicked.connect(self.stop)

    def generate_heatmap(self):
        if not hasattr(self.yolo_predict, 'source') or not self.yolo_predict.source:
            DialogOver(parent=self, text="请先选择图像并完成检测", title="错误", flags="danger")
            return
        self.heatmap_thread = HeatmapThread(
            img_path=self.yolo_predict.source,
            params=self.heatmap_params,
            save_dir='heatmap_results'
        )
        self.heatmap_thread.heatmap_signal.connect(self.show_heatmap)
        self.heatmap_thread.start()
        DialogOver(parent=self, text="热力图生成中...", title="提示", flags="info")

    def show_heatmap(self, heatmap_path):
        if heatmap_path and os.path.exists(heatmap_path):
            self.show_image(heatmap_path, self.label_15, 'path')
        else:
            DialogOver(parent=self, text="热力图文件未找到", title="错误", flags="danger")


    #主窗口显示原图与检测结果
    @staticmethod
    def show_image(img, label, flag):

        if flag == "path":
            img_src = cv2.imdecode(np.fromfile(img, dtype=np.uint8), -1)
        else:
            img_src = img

        # Resize the image
        img_src_ = cv2.resize(img_src,(640, 480))

        # 将 OpenCV 图像转换为 QImage 对象，并将其显示在 QLabel 组件中
        frame = cv2.cvtColor(img_src_, cv2.COLOR_BGR2RGB)
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[2] * frame.shape[1],QImage.Format_RGB888)

        label.setPixmap(QPixmap.fromImage(img))
        label.setScaledContents(True)  # 自适应界面大小




    # 控制开始|暂停
    def run_or_continue(self):
        if self.yolo_predict.source == '' or self.yolo_predict.source is None:
            DialogOver(parent=self, text="请重新上传文件", title="运行失败", flags="danger")
            self.pushButton_start_stop.setChecked(False)
            return


        self.yolo_predict.stop_dtc = False
        # 开始
        if self.pushButton_start_stop.isChecked():

            # 图片预测
            file_extension = self.yolo_predict.source[-3:].lower()
            if file_extension == 'png' or file_extension == 'jpg':
                self.img_predict()
                return

            # 视频预测
            self.pushButton_start_stop.setChecked(True)

            if '0' in self.yolo_predict.source or '1' in  self.yolo_predict.source or 'rtsp' in self.yolo_predict.source:
                #self.progressBar.setFormat('实时视频流检测中...')
                pass
            if 'avi' in self.yolo_predict.source or 'mp4' in self.yolo_predict.source:
                #self.progressBar.setFormat('当前检测进度:%p%')
                pass
            self.yolo_predict.continue_dtc = True
            # 开始检测
            if not self.yolo_thread.isRunning():
                self.yolo_thread.start()
                self.main2yolo_begin_sgl.emit()
        # 暂停
        else:

            self.yolo_predict.continue_dtc = False
            self.pushButton_start_stop.setChecked(False)
            DialogOver(parent=self, text="已暂停检测", title="运行暂停", flags="warning")

    # select local file
    def open_src_file(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Video/image', 'test_images',"Pic File(*.mp4 *.mkv *.avi *.flv *.jpg *.png)")
        self.stop()
        if name:
            self.yolo_predict.source = name
            print('Loaded file：{}'.format(os.path.basename(name)))
            self.stop()
            if ".avi" in name or ".mp4" in name:
                # 显示第一帧
                self.cap = cv2.VideoCapture(name)
                ret, frame = self.cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.show_image(rgbImage, self.label, 'img')

                else:
                    self.cap.release()
            else:
                self.show_image(name, self.label, 'path')


    def show_status(self, msg):
        print(msg)
        if msg == '检测完成':
            #self.progressBar.setValue(0)
            self.pushButton_start_stop.setChecked(False)
            # 终止yolo线程
            if self.yolo_thread.isRunning():
                self.yolo_thread.quit()

        elif msg == '检测终止':
            #self.progressBar.setValue(0)
            self.pushButton_start_stop.setChecked(False)
            # 终止yolo线程
            if self.yolo_thread.isRunning():
                self.yolo_thread.quit()
            self.label.clear()
            self.label_14.clear()


    # Terminate button and associated state
    def stop(self):
        try:
            self.yolo_predict.release_capture()  # 这里是为了终止使用摄像头检测函数的线程，改了yolo源码
            # 结束线程
            self.yolo_thread.quit()

        except:
            pass

        self.yolo_predict.stop_dtc = True
        self.pushButton_start_stop.setChecked(False)  # 恢复按钮状态
        self.label.clear()  # 清空视频显示
        self.label_14.clear()  # 清空视频显示
        self.label_15.clear()  # 清空视频显示


    def img_predict(self):
        if check_url(self.yolo_predict.source):
            return

        self.pushButton_start_stop.setChecked(False)  # 按钮
        # 读取照片
        image = cv2.imread(self.yolo_predict.source)
        org_img = image.copy()
        # 加载模型
        model = self.yolo_predict.load_yolo_model()

        try:
            # 获取数据源
            iter_model = iter(model.track(source=image, show=False, iou=self.yolo_predict.iou_thres, conf=self.yolo_predict.conf_thres))
            result = next(iter_model)

            # 检查是否有检测结果
            if result.boxes.id is None or len(result.boxes.id) == 0:
                raise ValueError("没有检测到目标")

            id = result.boxes.id.tolist()
            self.id = [int(j) for j in id]

            coordinates = result.boxes.xyxy.tolist()
            self.coordinates = [list(map(int, e)) for e in coordinates]

            cls_list = result.boxes.cls.tolist()
            self.cls_list = [int(i) for i in cls_list]
            self.names = model.names

            self.conf_list = result.boxes.conf.tolist()
            self.conf_list = ['%.2f %%' % (each * 100) for each in self.conf_list]


            # 画标签
            img_box = result.plot()

            # 显示图片
            self.show_image(org_img, self.label, 'img')  # left
            self.show_image(img_box, self.label_14, 'img')  # right
        except ValueError as e:
            # 如果没有检测到目标，则显示原始图像
            print(e)
            self.show_image(org_img, self.label, 'img')
            self.show_image(org_img, self.label_14, 'img')






if __name__ == "__main__":
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Ceil)
    app = QApplication(sys.argv)
    Home = DetectMain()
    Home.show()
    sys.exit(app.exec())
