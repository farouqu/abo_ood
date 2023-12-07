import json
import argparse
import os
from tqdm import tqdm

# Image width and height from the AboShips dataset
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720


def load_annotation_data(file_path):
    """
    Load JSON annotation data from the specified file path.

    Args:
        file_path (str): The path to the JSON annotation file.

    Returns:
        list: The loaded annotation data.
    """
    with open(file_path, "r") as read_file:
        return json.load(read_file)


def normalize_bbox_coordinates(bbox, image_width, image_height):
    """
    Normalize bounding box coordinates.

    Args:
        bbox (list): List containing [x, y, width, height] of the bounding box.
        image_width (int): Width of the image.
        image_height (int): Height of the image.

    Returns:
        tuple: Normalized (x_normalized, y_normalized, w_normalized, h_normalized) coordinates.
    """
    x, y, w, h = bbox
    x_normalized = max(0, (2 * x + w) / (2 * image_width))
    y_normalized = max(0, (2 * y + h) / (2 * image_height))
    w_normalized = max(0, w / image_width)
    h_normalized = max(0, h / image_height)
    return x_normalized, y_normalized, w_normalized, h_normalized


def save_normalized_data(normalized_data, output_directory):
    """
    Save normalized data to text files.

    Args:
        normalized_data (list): List of normalized data.
        output_directory (str): Directory to save the text files.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for item in tqdm(normalized_data, desc="Converting bounding boxes to YOLO format", unit="box"):
        category_id = item["category_id"]
        bbox = item["bbox"]
        image_path = item["image_path"]

        x_norm, y_norm, w_norm, h_norm = normalize_bbox_coordinates(bbox, IMAGE_WIDTH, IMAGE_HEIGHT)

        # Create the output string
        output_str = f"{category_id} {x_norm} {y_norm} {w_norm} {h_norm}"

        # Save the output string to a text file named after the image
        output_filename = os.path.join(output_directory, f"{image_path.split('.')[0]}.txt")
        with open(output_filename, "a") as file:
            file.write(output_str + "\n")

    print("Conversion and saving complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert and save normalized annotation data.")
    parser.add_argument("--input_file_path", type=str, help="Path to the input JSON annotation file", required=True)
    parser.add_argument("--output_directory", type=str, help="Directory to save the normalized text files", required=True)

    args = parser.parse_args()

    annotation_data = load_annotation_data(args.input_file_path)
    save_normalized_data(annotation_data, args.output_directory)
