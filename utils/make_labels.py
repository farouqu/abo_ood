import json

file_path = "data/aboships/labels/val/annotation_info.json"

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

with open(file_path, "r") as read_file:
    data = json.load(read_file)

for item in data:
    category_id = item["category_id"]
    bbox = item["bbox"]
    image_path = item["image_path"]

    x, y, w, h = bbox
    x_normalized = (2 * x + w) / (2 * IMAGE_WIDTH)
    y_normalized = (2 * y + h) / (2 * IMAGE_HEIGHT)
    w_normalized = w / IMAGE_WIDTH
    h_normalized = h / IMAGE_HEIGHT

    # Create the output string
    output_str = f"{category_id} {x_normalized} {y_normalized} {w_normalized} {h_normalized}"

    # Save the output string to a text file named after the image
    output_filename = f"data/aboships/labels/val/{image_path.split('.')[0]}.txt"
    with open(output_filename, "a") as file:
        file.write(output_str + "\n")

print("Conversion and saving complete.")
