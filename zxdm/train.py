import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/dataset/yolo11.yaml')
    model.train(data=r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/dataset/plane/mydate.yaml',
                cache=False,
                imgsz=1024,
                epochs=300,
                batch=2,
                close_mosaic=0,
                workers=0,
                optimizer='SGD',
                patience=0,
                resume=True,
                amp=False,
                project='runs/train',
                name='11-',
                )