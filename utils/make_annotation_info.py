import json
import os
import argparse
from tqdm import tqdm


def load_data(file_path):
    """
    Load JSON data from the specified file path.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, "r") as read_file:
        return json.load(read_file)


def get_image_id_to_path_mapping(image_info):
    """
    Create a mapping of image IDs to file paths.

    Args:
        image_info (list): List of image information.

    Returns:
        dict: Mapping of image IDs to file paths.
    """
    return {int(item["id"]): item["file_name"] for item in image_info if "file_name" in item}


def filter_annotations_by_image_id(annotation_info, image_id_to_path):
    """
    Filter annotation data based on available image IDs.

    Args:
        annotation_info (list): List of annotation information.
        image_id_to_path (dict): Mapping of image IDs to file paths.

    Returns:
        list: Filtered annotation data.
    """
    new_annotation_data = []
    for item in tqdm(annotation_info, desc="Filtering annotations", unit="annotation"):
        if "image_id" in item:
            image_id = item["image_id"]
            if image_id in image_id_to_path:
                item["image_path"] = image_id_to_path[image_id]
                new_annotation_data.append(item)
    return new_annotation_data


def save_annotation_data(new_annotation_data, output_path):
    """
    Save filtered annotation data to a JSON file.

    Args:
        new_annotation_data (list): Filtered annotation data.
        output_path (str): The path to save the JSON file.
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(output_path, "w") as file:
        json.dump(new_annotation_data, file, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Process annotation data.")
    parser.add_argument("--input_file_path", type=str, help="Path to the input JSON file", required=True)
    parser.add_argument("--output_file_path", type=str, help="Path to the output JSON file", required=True)

    args = parser.parse_args()

    data = load_data(args.input_file_path)
    image_info = data.get("images", [])
    annotation_info = data.get("annotations", [])

    image_id_to_path = get_image_id_to_path_mapping(image_info)

    new_annotation_data = filter_annotations_by_image_id(annotation_info, image_id_to_path)

    save_annotation_data(new_annotation_data, args.output_file_path)


if __name__ == "__main__":
    main()
