# 1 Out-of-Distribution (OOD) Detection

This workpackage has the following goals:

- Testing/developing state-of-the-art methods for OOD detection with respect to single- and two stage detectors
  - The idea is to use the KPI to detect if the deep-learning model thinks that the given input image is within
    the distribution that was seeing during training. This then allows to use this KPI to predict behviour of the detector
    when real images are used for inference
  - This OOD detection KPI should be compared against the typical detector KPIs, for labeled images, in order to verify
    if the KPI is good at predicting how well the detector will work with a given input image
- Training a detector using simulated data, with and without data augmentation, and evaluating how well the detector
  performs when using data from real cameras
  - In order to achieve this goal, we need to:
    - Generate training and validation data using the AiLiveSim simulator
    - Train detector(s) using the training- and validation data
    - Do 2-3 recordings, in different conditions (time of the day etc.), and label some of the data for testing purposes
    - Compare how well the detectors perform with respect to the validation (simulated) and test (real) images using
      well known KPIs for detectors

## 1.1. Research Materials and Articles

- [Generalized Out-of-Distribution Detection: A Survey](https://arxiv.org/pdf/2110.11334.pdf)
  - This article brings together several concepts related to OOD and defines both taxonomy and mathematical definitions
    related to OOD
- [An Application of Out-of-Distribution Detection for Two-Stage Object Detection Networks](https://uwspace.uwaterloo.ca/bitstream/handle/10012/15646/Denouden_Taylor.pdf?sequence=1&isAllowed=y)
  - This MsC thesis concentrates on OOD in the case of two-stage detectors
- [Andrej Karpathy's YouTube lectures related to deep-learning](https://www.youtube.com/watch?v=VMj-3S1tku0)
  - If you need to refresh your memory regarding some concepts related to deep-learning, take a look at Andrej's fantastic lessons available at YouTube
- [Improving Object Localization with Fitness NMS and Bounded IoU Loss](https://arxiv.org/pdf/1711.00164.pdf)
  - A research paper regarding object detection KPIs
- [Common Objects in Context](https://cocodataset.org/#home)
  - COCO is a large-scale object detection, segmentation, and captioning dataset.

## 1.2. Contents

- [conda](./conda/README.md): Python virtual environments
- [docs](./docs): GitHub templates

## 1.3. Creating a Virtual Environment

In order to avoid compatibility issues between Python packages, CUDA drivers and such, typically it is a good idea to
use virtual environments that install only those packages that are required for the task at hand. One such tool
for creating virtual environments is Conda. You can create a virtual environment using Anaconda/Miniconda
as per these [instructions](./conda/README.md). You can create new environments as required, and push
these to the [conda](./conda) directory. Another possibility is to use Python requirements-file, so that the user
can install these packages to the virtual environment of his/her choice.

In a complex code base it is polite to mention somewhere, either on a directory or code level, which
requirements.txt file or Conda environment to use, so that the user of the code does not need to second guess
what packages are required.

## 1.4. Submitting Code

### 1.4.1. Pre-commit

This code base uses pre-commit git-hooks in order to check the code before it is committed to the repo. After
you have cloned the repo, install pre-commit package:

```shell
pip install pre-commit
```

and then install the pre-commit checks:

```shell
pre-commit install
```

Pre-commit needs to be installed only once after cloning the repo. Pre-commit is run automatically every time you commit code,
but you can run it manually as follows:

```shell
pre-commit run --all-files
```

When you run the above command, you will get a list of things that need to be fixed before committing.

### 1.4.2. Branching

Always create a new branch for anything that you want to merge to the main-branch, and then create a pull request (PR)
in GitHub when you are ready to submit the code. Before submitting the code, please make sure that it's PEP8 compliant.

### 1.4.3. Documenting Code

All the code needs to be commented before submitting it, so that the input parameters and return values of functions are
clearly commented. For documenting code, we use the [Numpy style](https://numpydoc.readthedocs.io/en/latest/format.html). Following
is an example regarding what the documented code should look like:

```python
def get_spreadsheet_cols(file_loc, print_cols=False):
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    file_loc : str
        The file location of the spreadsheet
    print_cols : bool, optional
        A flag used to print the columns to the console (default is
        False)

    Returns
    -------
    list
        a list of strings used that are the header columns
    """

    file_data = pd.read_excel(file_loc)
    col_headers = list(file_data.columns.values)

    if print_cols:
        print("\n".join(col_headers))

    return col_headers
```

### 1.4.4. Code Structure

The code should be structured so that the different models and the training code are in separeted files / directories.
[RetinaFace repo](https://github.com/biubug6/Pytorch_Retinaface) shows what a typical deep-learning repo could look like.
To this end, we have created the following directories that should be used:

- [dataloaders](./dataloaders)
  - This directory contains dataloaders and related
- [jupyter](./jupyter)
  - This directory contains jupyter notebooks and related
- [models](./models)
  - This directory contains all the different models
- [utils](./utils)
  - This directory contains utils and related

### 1.4.5. Pushing Large Binaries to the Repository

Git repos are meant for tracking source code, i.e. text, and large binary files like images should not be pushed, in large quantities, to the repo.
You can add images to the repo, as examples or link them to the README.md files. Following filetypes have been included in `.gitignore`

```
*.whl
*.jpeg
*.jpg
*.png
*.bmp
*.png
*.bmp
```

, so if you want to include images, you need to exclude that particular image from `.gitignore`.

## Object Detection Model Training Report

In this project, we train a YOLOv8 model on two datasets: a real dataset of maritime environment and a simulated dataset. The details of the datasets are explained in details [here](#dataset).

## Model Architecture

YOLOv8 (You Only Look Once version 8) is a single-shot object detection model, known for its efficiency in real-time detection tasks. As a single-state detector, YOLOv8 processes the entire image in a single forward pass, predicting bounding boxes and class probabilities directly. This design enables YOLOv8 to achieve impressive speed and accuracy in object detection, making it well-suited for applications requiring real-time inference, such as autonomous vehicles which falls under our domain of application.

Below is an image of the YOLOv8 architecture. Check out this [link](https://github.com/ultralytics/ultralytics) to learn more about YOLO.

![YOLOv8](https://blog.roboflow.com/content/images/size/w1600/2023/01/image-16.png "YOLOv8 Architecture")

## Dataset

In this project, we employed two publicly available maritime datasets - SimuShips and AboShips-PLUS

### [SimuShips](https://arxiv.org/abs/2211.05237)

The dataset consists of 9471 high-resolution (1920x1080) simulated images using the [AILiveSim simulator](https://www.ailivesim.com/) which include a wide range of obstacle types, atmospheric and illumination conditions along with occlusion, scale and visible proportion variations. The dataset annotations were provided in the form of bounding boxes based on the YOLO format.

"table summary of dataset"

### [AboShips](https://research.abo.fi/en/datasets/aboships-plus)

This dataset includes 9,880 images capturing maritime scenes, showcasing various types of maritime objects such as powerboats, ships, sailboats, and stationary objects. Detailed category definitions and images can be found in the associated reference paper. In total, ABOships-PLUS contains 33,227 annotated objects across these categories, including four types of ships.

The dataset annotations and labels were provided in the COCO format. To integrate with our workflow, we had to covert them to appropriate YOLO bounding box formats.

"table summary of dataset"

### Converting dataset

Download the dataset from the public repository and ensure you have a folder structure similar to this:

- aboships
  - images
  - labels

Then run the provided script to generate the appropriate labels:

```bash

make aboships-dataset

```

This will generate the appropriate accompanying *.txt files for all respective images.

Run the provided script to finalize the folder structure for training the model:

```bash

make split-datasets

```

Your folder structure should now look something similar to this:

- aboships
  - images
  - labels
  - train
    - images
    - labels
  - test
    - images
    - labels
  - val
    - images
    - labels

Also the same for **simuships**.

To train the model on the combination of both datasets, run the following script to create a combined directory:

```bash

make combined-dataset

```

**NB**: You can train the model on either the aboships, simuships or both datasets depending on the configuration file specified in the training parameters.

## Training

### Training Configuration

The initial model trained on both datasets was achieved using the following parameters:

Hardware Configuration:

- NVIDIA RTX 3070 with 8GB VRAM

Software Configuration:

- Dataset: Both [here](./dataloaders/ships.yaml)
- Model: Pretrained YOLO medium
- Epochs: 30
- Batch Size: 16
- Optimizer: adam
- Learning Rate: 1E-3

### Results

Results from first model....

## Model Evaluation

### Validation Set

Validation set results....

### Test Set

Test set results.....

## Inference

Making inference on the model.....

## Future Work

Next steps and improvements....
