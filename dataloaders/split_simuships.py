import os
import shutil
import argparse
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def split_dataset(images_folder, labels_folder, output_folder, train_size, val_size, test_size):
    """
    Split images and labels into training, validation, and test sets.

    Args:
        images_folder (str): Path to the images folder.
        labels_folder (str): Path to the labels folder.
        output_folder (str): Path to the output folder.
        train_size (float): Percentage of data for training.
        val_size (float): Percentage of data for validation.
        test_size (float): Percentage of data for testing.
    """
    # Create output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, "train", "images"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "train", "labels"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "val", "images"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "val", "labels"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "test", "images"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "test", "labels"), exist_ok=True)

    # Get image and label file lists
    images = os.listdir(images_folder)
    labels = os.listdir(labels_folder)

    # Split the dataset
    images_train, images_temp, labels_train, labels_temp = train_test_split(
        images, labels, train_size=train_size, random_state=42
    )
    images_val, images_test, labels_val, labels_test = train_test_split(
        images_temp, labels_temp, test_size=test_size / (test_size + val_size), random_state=42
    )

    # Move files to appropriate folders
    copy_files(images_folder, images_train, os.path.join(output_folder, "train", "images"))
    copy_files(labels_folder, labels_train, os.path.join(output_folder, "train", "labels"))

    copy_files(images_folder, images_val, os.path.join(output_folder, "val", "images"))
    copy_files(labels_folder, labels_val, os.path.join(output_folder, "val", "labels"))

    copy_files(images_folder, images_test, os.path.join(output_folder, "test", "images"))
    copy_files(labels_folder, labels_test, os.path.join(output_folder, "test", "labels"))


def copy_files(source_folder, files, destination_folder):
    """
    Move files from source folder to destination folder.

    Args:
        source_folder (str): Path to the source folder.
        files (list): List of file names to move.
        destination_folder (str): Path to the destination folder.
    """
    for f in tqdm(files, desc="Copying files...", unit="file"):
        source_path = os.path.join(source_folder, f)
        destination_path = os.path.join(destination_folder, f)
        shutil.copy(source_path, destination_path)


if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Split images and labels into training, validation, and test sets.")
    parser.add_argument("--images_folder", type=str, help="Path to the images folder")
    parser.add_argument("--labels_folder", type=str, help="Path to the labels folder")
    parser.add_argument("--output_folder", type=str, help="Path to the output folder")
    parser.add_argument("--train_size", type=float, default=0.8, help="Percentage of data for training")
    parser.add_argument("--val_size", type=float, default=0.1, help="Percentage of data for validation")
    parser.add_argument("--test_size", type=float, default=0.1, help="Percentage of data for testing")

    args = parser.parse_args()

    # Split and organize the dataset
    split_dataset(args.images_folder, args.labels_folder, args.output_folder, args.train_size, args.val_size, args.test_size)
