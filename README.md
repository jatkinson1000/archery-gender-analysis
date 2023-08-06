# Archery Gender Analysis

![GitHub](https://img.shields.io/github/license/jatkinson1000/archery-gender-analysis)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Analysis of data from indoor archery competitions to examine gender differences.  
A research paper based on this analysis has been written.


## Usage
Usage is allowed under the [licensing specified]("LICENSE").
Whilst this repository is intended as a static data source and source code supporting a
research article, suitable contributions may be considered.  
Others are also welcome to build upon the code here, or any parts therein, for their own
research under the licensing specified.

If using any of this code, data, or its derivatives it is appreciated if visible credit
is given using the information provided in the [`CITATION.cff`]("Citation.cff") file.


### Installation

To install clone the repository, navigate to `/archery-gender-analysis`, and run:

    python3 -m pip install .

It is recommended to use a virtual environment.


### Getting Started

The data analysis can be performed using the jupyter notebook `analysis.ipynb`

This can be run from the main directory using:
```
    jupyter notebook examples.ipynb
```

The source code used to perform the data acquisition, analysis, and plotting can be found
in the source code directory [`archery-gender-analysis/`]("archery-gender-analysis/").
The downloaded datasets used in this paper can be found in [`data/`]("data/") and the
results of the analysis can be found in [`results`]("results/").  
These were generated using the script [`main.py`]("archery-gender-analysis/main.py").


### License
Copyright &copy; Jack Atkinson

This code is distributed under the
[MIT Licence](LICENSE).


### Authors and Acknowledgment
See [Contributors](https://github.com/jatkinson1000/archery-gender-analysis/graphs/contributors)
for a list of contributors towards this project.

If you use this software in your work, please provide visible credit/citation.
[CITATION.cff](CITATION.cff)
provides citation metadata, which can also be accessed from
[GitHub](https://github.com/jatkinson1000/archery-gender-analysis).


## Contributions
This repository is intended as a static data source and source code supporting a
research article.
However, suitable contributions may be considered in cases where there is a strong argument.

For bugs and clear suggestions for improvement please
[open an issue](https://github.com/jatkinson1000/archeryutils/archery-gender-analysis).


### Code of Conduct
Everyone participating in this project is expected to treat others
with respect and more generally to follow the guidelines articulated in the
[Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

