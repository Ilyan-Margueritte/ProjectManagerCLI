import os
from setuptools import setup, find_packages

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="projectmcli",
    version="1.5.0",
    description="Project Manager CLI - Ultimate Developer Productivity Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ilyan Margueritte",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pmcli=pmcli.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
