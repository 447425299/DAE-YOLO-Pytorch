from ultralytics import YOLO

model = YOLO(r'/home/star/Desktop/ultralytics-yolo11-20241207/ultralytics-yolo11-main/runs/train/115/weights/last.pt')
results = model.train(resume=True)