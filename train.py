from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data=r"C:\Users\Prakhar\railguard\dataset\data.yaml",
    epochs=30,
    imgsz=640,
    batch=8
)
