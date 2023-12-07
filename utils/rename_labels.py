import os
import re

train_labels = "data/aboships/train/labels"
val_labels = "data/aboships/val/labels"
test_labels = "data/aboships/test/labels"

boat_labels = [1, 2, 3, 4, 5, 6, 8, 9, 10]
obs_labels = [7, 11]

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

# label_file = '201806260750_001.txt'

for label_file in os.listdir(val_labels):
    if "ailivesim" not in label_file:
        with open(f"{val_labels}/{label_file}", "r") as file:
            lines = file.readlines()

        with open(f"{val_labels}/{label_file}", "w") as file:
            for line in lines:
                values = line.strip().split(" ")
                class_label = values[0]

                new_class_label = label_map.get(class_label)

                values[0] = str(new_class_label)

                file.write(" ".join(values))
                file.write("\n")
