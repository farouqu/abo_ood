import argparse
import xml.etree.ElementTree as ET
import random
import os
import cv2
import json
import shutil
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np


def map_color_palette(xml_file: str):
    """Maps the object categories to the color id

    Parameters
    ----------
    xml_file : str
        The xml file containing the color mappings e.g GroundTruthColorMappings.xml

    Returns
    -------
    (dict, list)
        a tuple containing the dictonary of color mappings and list of ordered categories
    """

    mytree = ET.parse(xml_file)
    myroot = mytree.getroot()

    categories_to_colors = {}
    ordered_categories = []
    for i in range(256):
        ordered_categories.append("Unknown")

    for rule in myroot.iter("Rule"):
        colorID = rule.attrib.get("colorID")
        colorRange = rule.attrib.get("colorRange")
        color_start = color_end = 0
        if colorID:
            color_start = color_end = int(colorID)
        if colorRange:
            color_start = int(colorRange.split(":")[0])
            color_end = int(colorRange.split(":")[1])
        while color_start <= color_end:
            category = rule.attrib.get("category")
            if not category:
                print("error, no categry found in the rule: ", rule)
                continue
            ordered_categories[color_start] = category
            if categories_to_colors.get(category):
                if color_start not in categories_to_colors[category]:
                    categories_to_colors[category].append(color_start)
            else:
                categories_to_colors[category] = [color_start]
            color_start += 1
    return categories_to_colors, ordered_categories


def get_categories_mappings(categories_to_colors):
    """Returns a dictonary of the color mappings

    Parameters
    ----------
    categories_to_colors : str
        The dict containing the mappings

    Returns
    -------
    str
        a dictionary mapping the class id to a textual name
    """

    categories_text = {}
    for i, cat in enumerate(categories_to_colors):
        if cat == "default":
            continue
        categories_text[i] = cat
    return categories_text


def plot_bounding_box(image_file, annotation_file, annotation_map, output_dir):
    """Plots the bounding boxes on the image file based on the annotation file

    Parameters
    ----------
    image_file : str
        The path to the image file

    annotation_file : str
        The path to the annotation file

    output_dir : str
        The directory to save the result

    Returns
    -------
    None
    """

    # Generate annotation list
    annotation_list = []
    with open(annotation_file, "r") as file:
        annotation_list = file.read().split("\n")
        annotation_list = [x.split(" ") for x in annotation_list if x]
        annotation_list = [[float(y) for y in x] for x in annotation_list]

    # Load the image
    image = Image.open(image_file)

    boats = 0
    obstacles = 0

    annotations = np.array(annotation_list)
    w, h = image.size

    plotted_image = ImageDraw.Draw(image)
    transformed_annotations = np.copy(annotations)
    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h
    transformed_annotations[:, 2] += 0

    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
    transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
    transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        font = ImageFont.truetype("data/SimuShips/arial.ttf", 30)
        plotted_image.rectangle((x0, y0, x0 + 120, y0 + 40), fill=(255, 255, 255, 255))
        plotted_image.text((x0, y0), annotation_map[(int(obj_cls))], font=font, fill=(255, 0, 0, 255))
        plotted_image.rectangle(((x0, y0), (x1, y1)), outline="yellow", width=3)
        if obj_cls == 0:
            boats += 1
        if obj_cls == 1:
            obstacles += 1

    print("The images has {0} boats and {1} obstacles".format(boats, obstacles))
    fig = plt.figure(figsize=(w / 50, h / 50))
    plt.imshow(np.array(image))
    plt.axis("off")

    # File name with extension
    file_name = os.path.basename(image_file)
    file_name = os.path.splitext(file_name)[0]
    fig.savefig(f"{output_dir}/{file_name}-annot.png", bbox_inches="tight", pad_inches=0)


def generate_simuships_annot_images(num):
    """Plots the bounding boxes for images on the SimuShips dataset

    Parameters
    ----------
    num : int
        The number of images to generate

    Returns
    -------
    None
    """

    MIN = 0
    MAX = 9470

    color_mappings_xml = "data/SimuShips/GroundTruthColorMapping.xml"
    class_to_categories, ordered_categories = map_color_palette(color_mappings_xml)
    annotation_map = get_categories_mappings(class_to_categories)

    output_dir = "data/SimuShips/images-annot"

    indices = random.sample(range(MIN, MAX), num)

    for index in indices:
        image_file = f"data/SimuShips/images/{index}-ailivesim.png"
        annotation_file = f"data/SimuShips/labels/{index}-ailivesim.txt"

        plot_bounding_box(image_file, annotation_file, annotation_map, output_dir)


def generate_aboships_annot_images(num):
    """Plots the bounding boxes for images on the SimuShips dataset

    Parameters
    ----------
    num : int
        The number of images to generate

    Returns
    -------
    None
    """

    # Get the annotation map
    annot_file_path = "data/aboships/annotation_map.json"

    with open(annot_file_path, "r") as read_file:
        annot_map = json.load(read_file)

    annotation_map = {int(key): value for key, value in annot_map.items()}
    output_dir = "data/aboships/images-annot/val"

    # Plot for random images (based on user's input)
    folder_path = "data/aboships/images/val"
    images_list = os.listdir(folder_path)
    selected_images = random.sample(images_list, num)

    for image in selected_images:
        image_name = os.path.basename(image)
        image_name = os.path.splitext(image_name)[0]

        image_file = f"data/aboships/images/val/{image_name}.png"
        annotation_file = f"data/aboships/labels/val/{image_name}.txt"

        plot_bounding_box(image_file, annotation_file, annotation_map, output_dir)


if __name__ == "__main__":
    argP = argparse.ArgumentParser()

    argP.add_argument("-d", "--dataset", help="Dataset to plot annotations: simuships or aboships", required=True)
    argP.add_argument("-n", "--num", help="Number of images to plot annotations", required=True)

    args = argP.parse_args()

    dataset = str(args.dataset)
    num = int(args.num)

    if dataset == "simuships":
        generate_simuships_annot_images(num)
    elif dataset == "aboships":
        generate_aboships_annot_images(num)
    else:
        print("Unknown dataset. Available options: simuships, aboships")
