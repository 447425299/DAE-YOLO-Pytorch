import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/runs/train/115/weights/last.pt') # 选择训练好的权重路径
    model.val(data=r' /media/star/Data/K/BYSJ/ultralytics-yolo11-20241207/ultralytics-yolo11-main/dataset/dataset_visdrone/data.yaml',
              split='test', # split可以选择train、val、test 根据自己的数据集情况来选择.
              imgsz=1024,
              batch=2,
              # iou=0.7,
              # rect=False,
              save_json=True, # if you need to cal coco metrice
              project='runs/val',
              name='11-',
              )