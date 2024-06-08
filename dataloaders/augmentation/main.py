import argparse
import os
from dataloaders.augmentation.utils import get_augmented_results, get_input_data, is_image_by_extension, save_augmentation
from utils import *


def run_yolo_augmentor(input_path, output_path):
    """
    Run the YOLO augmentor on a set of images.

    This function processes each image in the input directory, applies augmentations,
    and saves the augmented images and labels to the output directories.

    Args:
        input_path (str): Name of input folder.
        output_path (str): Name of the output folder.

    """
    imgs = [img for img in os.listdir(f"{input_path}/images") if is_image_by_extension(img)]

    for img_num, img_file in enumerate(imgs):
        print(f"{img_num+1}-image is processing...\n")
        image, gt_bboxes, aug_file_name = get_input_data(input_path, img_file)
        aug_img, aug_label = get_augmented_results(image, gt_bboxes)
        if len(aug_img) and len(aug_label):
            save_augmentation(aug_img, aug_label, aug_file_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augment images.")
    parser.add_argument("--input_folder", type=str, help="Path to the source folder for images")
    parser.add_argument("--output_folder", type=str, help="Path to the destination folder to store augmented images")

    args = parser.parse_args()
    run_yolo_augmentor(args.input_folder, args.output_folder)
