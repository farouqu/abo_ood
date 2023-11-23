import json

file_path = "data/AboShips/labels/train/annotation_info.json"

with open(file_path, "r") as read_file:
    data = json.load(read_file)

for item in data:
    category_id = item["category_id"]
    bbox = item["bbox"]
    image_path = item["image_path"]

    x, y, w, h = bbox
    x_normalized = x / 1280
    y_normalized = y / 720
    w_normalized = w / 1280
    h_normalized = h / 720

    # Create the output string
    output_str = f"{category_id} {x_normalized} {y_normalized} {w_normalized} {h_normalized}"

    # Save the output string to a text file named after the image
    output_filename = f"data/AboShips/labels/train/{image_path.split('.')[0]}.txt"
    with open(output_filename, "a") as file:
        file.write(output_str + "\n")

print("Conversion and saving complete.")
