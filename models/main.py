from ultralytics import YOLO

SEED = 42

# Load a pretrained YOLOv8n model
model = YOLO("yolov8m.pt")

if __name__ == "__main__":
    # Train the model
    results = model.train(
        data="dataloaders/ships.yaml",
        resume=True,
        epochs=30,
        imgsz=640,
        pretrained=True,
        seed=SEED,
        plots=True,
        save=True,
        device=[0],
    )
    results = model.val()
