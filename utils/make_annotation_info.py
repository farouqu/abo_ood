import json

file_path = "data/AboShips/annotations/train.json"

with open(file_path, "r") as read_file:
    data = json.load(read_file)

image_info = data["images"]
annotation_info = data["annotations"]


image_id_to_path = {int(item["id"]): item["file_name"] for item in image_info if "file_name" in item}


new_annotation_data = []
for item in annotation_info:
    if "image_id" in item:
        image_id = item["image_id"]
        if image_id in image_id_to_path:
            item["image_path"] = image_id_to_path[image_id]
            new_annotation_data.append(item)


with open("data/AboShips/labels/train/annotation_info.json", "w") as file:
    json.dump(new_annotation_data, file, indent=2)

print("Processing complete. Check 'new_annotation_data.json'.")
