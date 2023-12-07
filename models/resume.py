from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("runs/detect/train8/weights/last.pt")

if __name__ == "__main__":
    # Train the model
    results = model.train(resume=True)
    results = model.val()
