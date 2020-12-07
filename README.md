# CS 533 HCI Bibliography Demo

This Git repository demonstrates a basic multi-file project with scripts and notebooks.

It uses data from the [HCI Bibliography][hcibib].

[hcibib]: http://hcibib.org

## Environment Setup

This repository includes a Conda environment file (`environment.yml`) to install all required packages.
You can initialize and use this environment with:

    conda env create -f environment.yml
    conda activate cs533-bib

A Conda *environment* is an isolated environment that contains a particular set of packages.
It is useful for keeping projects isolated from each other, and for ensuring that you have a complete list of the software required to run a project.

After you have created and activated the environment, you can run Jupyter with `jupyter notebook`.

I have also provided a `requirements.txt` file if you would prefer to use a Python virtual environment instead of a Conda environment.
I recommend using Conda environments.

## Components

This repository consists of several pieces:

- The `fetch-bibdata.py` script downloads bibliographic data from hcibib.org and saves it in a local directory.
- The `parse-bibdata.py` script parses downloaded bibliography files and converts them into a CSV file you can load from Pandas.
- The notebooks perform analyses on this data.

The scripts contain usage information in their docstrings.
Review those for information on their options.

## Re-running Analysis

The notebooks are based on downloading the CHI papers to the directory `chi-papers`.
You can run everything by:

1.  Download data:

        python fetch-bibdata.py -d chi-papers -m '^CHI\d'

2.  Parse data:

        python parse-bibdata.py chi-papers

3.  Run the notebooks (they have no dependencies between each other, so they can be run in either order).