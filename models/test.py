from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("runs/detect/train8/weights/best.pt")

if __name__ == "__main__":
    # Train the model
    results = model.val(data="dataloaders/test.yaml", split="test", plots=True, iou=0.7)
