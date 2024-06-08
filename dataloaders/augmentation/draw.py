import argparse
import os

from utils import draw_yolo, get_input_data, get_plain_bboxes_list

CLASSES = [0, 1]


def draw(image_file):
    parts = image_file.split(os.path.sep)

    folder_path = os.path.join(*parts[:-2])
    image_file = parts[-1]
    label_path = os.path.splitext(parts[-1])[0] + ".txt"

    labels = get_plain_bboxes_list(f"{folder_path}/labels/{label_path}", CLASSES)
    image, gt_bboxes, aug_file_name = get_input_data(folder_path, image_file)

    draw_yolo(folder_path, image, labels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augment images.")
    parser.add_argument("--image_path", type=str, help="Path to the source image")

    args = parser.parse_args()
    draw(args.image_path)
