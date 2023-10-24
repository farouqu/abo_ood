# 1 Out-of-Distribution (OOD) Detection

This workpackage has the following goals:

* Testing/developing state-of-the-art methods for OOD detection with respect to single- and two stage detectors
* Training a detector using simulated data, with and without data augmentation, and evaluating how well the detector
performs when using data from real cameras
  * In order to achieve this goal, we need to:
    * Generate training and validation data using the AiLiveSim simulator
    * Do 2-3 recordings, in different conditions (time of the day etc.), and label some of the data for testing purposes

## 1.1. Research Materials and Articles

* [Generalized Out-of-Distribution Detection: A Survey](https://arxiv.org/pdf/2110.11334.pdf)
  * This article brings together several concepts related to OOD and defines both taxonomy and mathematical definitions
  related to OOD
* [An Application of Out-of-Distribution Detection for Two-Stage Object Detection Networks](https://uwspace.uwaterloo.ca/bitstream/handle/10012/15646/Denouden_Taylor.pdf?sequence=1&isAllowed=y)
  * This MsC thesis concentrates on OOD in the case of two-stage detectors
* [Andrej Karpathy's YouTube lectures related to deep-learning](https://www.youtube.com/watch?v=VMj-3S1tku0)
  * If you need to refresh your memory regarding some concepts related to deep-learning, take a look at Andrej's fantastic lessons available at YouTube

## 1.2. Contents

* [conda](./conda/README.md): Python virtual environments
* [docs](./docs): GitHub templates

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

This code base use pre-commit git-hooks in order to check the code before it is committed to the repo. After
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

* [models](./models)
  * This directory contains all the different models
* [dataloaders](./dataloaders)
  * This directory contains dataloaders and related
* [utils](./utils)
  * This directory contains utils and related
