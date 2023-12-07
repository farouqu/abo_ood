import os
import shutil
import argparse
from tqdm import tqdm


def reorganize_dataset(source_folder, destination_folder):
    """
    Reorganize images and labels in the dataset folder structure.

    Args:
        source_folder (str): Path to the source dataset folder.
        destination_folder (str): Path to the destination dataset folder.
    """

    for split in ["train", "test", "val"]:
        images_source_path = os.path.join(source_folder, "images", split)
        labels_source_path = os.path.join(source_folder, "labels", split)

        images_destination_path = os.path.join(destination_folder, split, "images")
        labels_destination_path = os.path.join(destination_folder, split, "labels")

        # Create destination folders if they don't exist
        os.makedirs(images_destination_path, exist_ok=True)
        os.makedirs(labels_destination_path, exist_ok=True)

        # Move images and labels
        copy_files(images_source_path, images_destination_path)
        copy_files(labels_source_path, labels_destination_path)


def copy_files(source_path, destination_path):
    """
    Copy files from source folder to destination folder.

    Args:
        source_path (str): Path to the source folder.
        destination_path (str): Path to the destination folder.
    """

    files = os.listdir(source_path)
    for f in tqdm(files, desc="Copying files...", unit="file"):
        source_file_path = os.path.join(source_path, f)
        destination_file_path = os.path.join(destination_path, f)
        shutil.copy(source_file_path, destination_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reorganize folders for images and labels.")
    parser.add_argument("--source_folder", type=str, help="Path to the source folder (aboships)")
    parser.add_argument("--destination_folder", type=str, help="Path to the destination folder")

    args = parser.parse_args()

    reorganize_dataset(args.source_folder, args.destination_folder)
