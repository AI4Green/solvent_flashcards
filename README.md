# Solvent Guide
The solvent guide provides a visual interface for the comparison of
common laboratory solvents to encourage greener decision-making during reaction design. The data for each solvent was collected
from the [CHEM21 solvent guide](https://pubs.rsc.org/en/content/articlelanding/2016/gc/c5gc01008j) and is provide via a simple visual interface.

This software was first developed as part of [AI4Green](https://pubs.acs.org/doi/10.1021/acs.jcim.3c00306), a Machine-Learning powered Electronic 
Lab Notebook (ELN) that aims to facilitate greener choices at the laboratory level. It has been adapted as a standalone tool
in the hope that it may be useful outside of the ELN.

## Installation
First install the required dependencies:
numpy
plotly
blinker
flask
python-dateutils
colorama



Then, the package can be installed from pip using the following command:
```
pip install solvent_guide
```

## Run from command line

Once installed, the solvent guide can be launched from the command line with:

```
python -m solvent_guide.webapp
```

## Import as python package

It is also possible to run the solvent guide in python by importing the app_run() function.

