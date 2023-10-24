from pathlib import Path
from datetime import datetime

from setuptools import find_packages, setup

this_directory = Path(__file__).parent

setup(
    name="ailivesim-out-of-distribution",
    version="1.0.0",
    packages=find_packages(),
    company="AiLiveSim",
    author="AiLiveSim",
    author_email="jarno@ailivesim.com",
    description="Out of distribution detection related functionality",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Simulator :: Weather Parameters :: Deep Learning",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["torch", "torchvision", "scikit-learn", "einops", "albumentations", "matplotlib"],
)
