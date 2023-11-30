import os
import shutil
import random
import argparse


def split_dataset(data_dir, labels_dir, train_size=0.7):
    """Splits a folder path into training and test images

    Parameters
    ----------
    data_dir : str
        Path of the images
    labels_dir : str
        Path of the images labels

    train_size: num
        Ratio of training size

    Returns
    -------
    None
    """

    file_paths = os.listdir(data_dir)
    label_paths = os.listdir(labels_dir)

    all_paths = list(zip(file_paths, label_paths))

    # Shuffle the file paths
    random.shuffle(all_paths)

    file_paths, label_paths = zip(*all_paths)

    # Split the file paths into training and test sets
    train_size = int(len(file_paths) * train_size)
    train_paths = file_paths[:train_size]
    val_paths = file_paths[train_size:]

    # train_label_size = int(len(label_paths) * train_size)
    train_label_paths = label_paths[:train_size]
    val_label_paths = label_paths[train_size:]

    # Create training and test directories if they don't exist
    if not os.path.exists("data/simuships/train/images"):
        os.makedirs("data/simuships/train/images")
    if not os.path.exists("data/simuships/val/images"):
        os.makedirs("data/simuships/val/images")
    if not os.path.exists("data/simuships/train/labels"):
        os.makedirs("data/simuships/train/labels")
    if not os.path.exists("data/simuships/val/labels"):
        os.makedirs("data/simuships/val/labels")

    # Move training files to the training directory
    for path in train_paths:
        shutil.copy(os.path.join(data_dir, path), os.path.join("data/simuships/train/images", path))

    # Move training files to the training directory
    for path in train_label_paths:
        shutil.copy(os.path.join(labels_dir, path), os.path.join("data/simuships/train/labels", path))

    # Move test files to the test directory
    for path in val_paths:
        shutil.copy(os.path.join(data_dir, path), os.path.join("data/simuships/val/images", path))

    # Move test files to the test directory
    for path in val_label_paths:
        shutil.copy(os.path.join(labels_dir, path), os.path.join("data/simuships/val/labels", path))


if __name__ == "__main__":
    argP = argparse.ArgumentParser()

    argP.add_argument("-p", "--folder_path", help="Parent folder of images", required=True)
    argP.add_argument("-l", "--labels_path", help="Parent folder of labels", required=True)
    argP.add_argument("-t", "--train_size", help="Training ratio of the images e.g 0.7(70%)", required=True)

    args = argP.parse_args()

    fp = str(args.folder_path)
    lp = str(args.labels_path)
    t = float(args.train_size)

    split_dataset(fp, lp, train_size=t)
