import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/runs/train/11-V+L+BRA/weights/last.pt') # select your model.pt path
    model.predict(source=r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/dataset/plane/test/images',
                  imgsz=1024,
                  project='runs/detect',
                  name='11',
                  save=True,
                  # conf=0.2,
                  # iou=0.7,
                  # agnostic_nms=True,
                  # visualize=True, # visualize model features maps
                  # line_width=2, # line width of the bounding boxes
                  # show_conf=False, # do not show prediction confidence
                  show_labels=False, # do not show prediction labels
                  # save_txt=True, # save results as .txt file
                  # save_crop=True, # save cropped images with results
                )