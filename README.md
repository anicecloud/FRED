


# FRED with NCBI search

Introduction 
------------

This is a fork of the [FRED](https://github.com/loosolab/FRED) repository, extended under its MIT license. The original project was developed by:
>Walter, J., Kuenne, C., Knoppik, N., Goymann, P., & Looso, M. (2026). FRED enables standardized FAIR metadata generation and management for omics research. Scientific Reports. https://doi.org/10.1038/s41598-026-61886-9

For more information about FRED, please see the original project [documentation](https://loosolab.pages.gwdg.de/software/metadata-organizer/).

The aim of this extension is to provide the capacity of searching for organisms not present in the pre-configured whitelists in the NCBI Datasets. To provide this function, the project depends on the ncbi-datsets-cli tool.

This project was developed by Tendero Delicado, C. for the [Institute of Agrochemistry and Food Technology](https://iata.csic.es/). 

# How to install

Since the project depends on the ncbi-datasets-cli tool, it is recommended that the installation is made in a conda environment. You can install FRED directly from the repository with the following commands:

1. Create a Conda environment with NCBI datasets, Python 3.14+ and pip

```
conda create -n metadata-env -c conda-forge ncbi-datasets-cli "python>=3.14" pip
```

2. Activate the environment

```
conda activate metadata-env
```

3. Clone the repository 

```
git clone https://github.com/anicecloud/FRED.git
```

4. (Optional) Check the pip path points to the environment
```
which pip
```
If the command does not return a path pointing to the environment's bin folder, use the environment's absolute path for the last step.

5. Install the package

```
pip install FRED
```

