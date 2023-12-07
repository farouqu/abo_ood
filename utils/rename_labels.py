import os
import argparse


def remap_labels(input_directory, label_map):
    """
    Remap class labels in label files based on the provided label map.

    Args:
        input_directory (str): Directory containing label files.
        label_map (dict): Mapping of old labels to new labels.
    """
    for label_file in os.listdir(input_directory):
        if "ailivesim" not in label_file:
            file_path = os.path.join(input_directory, label_file)

            with open(file_path, "r") as file:
                lines = file.readlines()

            with open(file_path, "w") as file:
                for line in lines:
                    values = line.strip().split(" ")
                    class_label = values[0]

                    new_class_label = label_map.get(class_label, class_label)

                    values[0] = str(new_class_label)

                    file.write(" ".join(values))
                    file.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remap class labels in label files.")
    parser.add_argument("--input_directory", type=str, help="Directory containing label files")

    args = parser.parse_args()

    label_map = {
        "1": "0",
        "2": "0",
        "3": "0",
        "4": "0",
        "5": "0",
        "6": "0",
        "8": "0",
        "9": "0",
        "10": "0",
        "7": "1",
        "11": "1",
    }

    remap_labels(args.input_directory, label_map)
