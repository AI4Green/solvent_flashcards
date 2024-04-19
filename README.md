# Solvent Guide
The solvent guide provides a visual interface for the comparison of
common laboratory solvents to encourage greener decision-making during reaction design. The data for each solvent was collected
from the [CHEM21 solvent guide](https://pubs.rsc.org/en/content/articlelanding/2016/gc/c5gc01008j) and is provided via a simple visual interface.

This software was first developed as part of [AI4Green](https://pubs.acs.org/doi/10.1021/acs.jcim.3c00306), a Machine-Learning powered Electronic 
Lab Notebook (ELN) that aims to facilitate greener choices at the laboratory level. It has been adapted as a standalone tool
in the hope that it may be useful outside the ELN.

## Installation

First, ensure you have installed the required dependencies:
```
pip install numpy>=1.26.0 pandas>=1.4.1 blinker>=1.6.2 flask>=2.3.2 plotly>=5.9.0 colorama>=0.4.6 python-dateutil>=2.8.2
```

Then, the package can be installed from pip using the following command:
```
pip install solvent-guide
```

## Run from command line

Once installed, the Solvent Guide can be launched from the command line with:

```
python -m solvent_guide.webapp
```


This should open a web browser and allow you to view the solvent guide.

_**This process runs on port 5000 by default. If other apps are running on this port then this can cause issues.**_

_**The port can be changed by setting the FLASK_RUN_PORT environment variable in the command line before running. For example, to run on port 80:**_

```
# Windows
set FLASK_RUN_PORT=80

# Linux/Mac
export FLASK_RUN_PORT=80
```

  
The process can be killed by entering:
```
Ctrl + C
```

### Adding new solvents
New solvents can be added to the Solvent Guide by running:

```
python -m solvent_guide.add_solvent
```

and following the prompts therein. If the information is not available, each prompt can be skipped by pressing enter.  

Upon rerunning the Solvent Guide, the new solvent will be included.

A summary of the information required is shown below.

___
**Enter PubChem ID (if known)** (*PubChemID to link solvent entry to PubChem*)  
**Enter CAS Number (if known)** (*CAS number of the solvent if available*)  
**Enter Solvent Family** (*the class the solvent belongs to (Halogenated, esters etc)*)  
**Enter Solvent Name**  (*the solvent name*)  
**Enter Alternative Solvent Name** (*an alternative name for the solvent if applicable*)  
**Enter Boiling Point** (*solvent boiling point*)  
**Enter Flash Point:** (*solvent flash point if applicable*)  
**Enter Worst H3xx statement** (*the most hazardous H3XX statement*)  
**H3_phrase** (*the phrase associated with the worst H3XX number. Only needed if H3xx statement was provided.*)   
**Enter Worst H4xx statement** (*the most hazardous H4XX statement*)  
**H4_phrase** (*the phrase associated with the worst H4XX number. Only provided if an H4xx statement was provided.*)  
**Enter CHEM21 Safety Score** (*CHEM21 safety score, can be skipped if not available*)  
**Enter CHEM21 Health Score** (*CHEM21 health score, can be skipped if not available*)  
**Env** (*CHEM21 environment score, can be skipped if not available*)  
**Select Ranking** (*Ranking to determine flashcard colour. Must be chosen from the provided options*)  
**Enter Replacement Issues** (*justification for replacements*)  
**Enter Possible Replacement 1** (*solvent to be used as substitute if applicable*)  
**Enter Replacement 2** (*str, solvent to be used as substitute is applicable*)
___

### Removing solvents
Solvents can be removed from the Solvent Guide by running: 

```
python -m solvent_guide.remove_solvent
```
and entering the corresponding CAS number.
  
  
All solvents can be removed by resetting the Solvent Guide. This can be done via:

```
python -m solvent_guide.reset_solvents
```

THIS WILL DELETE ALL ADDED SOLVENTS AND REMOVE ALL CHANGES MADE TO THE DATABASE SINCE INSTALLATION.
   
You will be prompted to confirm this:

```
CAUTION! Resetting the database will revert all changes made since installation. Are you sure? (y/n)
```

## Import as python package

It is also possible to run the solvent guide in python by importing the app_run() function.

```
from solvent_guide.webapp import app_run

app_run()
```
This will start running the Solvent Guide and should open up a new browser window.

### Adding Solvents
#### Adding individual solvents
Solvents can be added individually using the add_solvent() function and following the prompts.

Running:
```
from solvent_guide.add_solvent import add_solvent

add_solvent()
```

gives: 

```
Follow the prompts to add a flashcard for the new solvent. Prompts can be skipped by pressing Enter.
Enter PubChem ID (if known):
```

#### Adding multiple solvents

Data for multiple solvents can be added by using add_solvent_from_dataframe(). This function requires
the data to be organised in a pandas DataFrame with the following columns:
___
**PubChem ID** (*int, PubChemID to link to entry*)  
**CAS** (*str, CAS number fo the solvent if available*)  
**Family** (*str, the class the solvent belongs to (Halogenated, esters etc)*)  
**Solvent**  (*str,the solvent name*)  
**Solvent Alternative Name** (*str,an alternative name for the solvent is applicable*)  
**BP** (*int, solvent boiling point*)  
**FP** (*int, solvent flash point if applicable*)  
**Worst H3xx** (*str,the most hazardous H3XX statement*)  
**Worst H4xx** (*str,the most hazardous H4XX statement*)  
**Safety** (*int, CHEM21 safety score*)  
**Health** (*int, CHEM21 health score*)  
**Env** (*int, CHEM21 environment core*)  
**Ranking Default** (*str, CHEM21 default ranking*)  
**Ranking Discussion** (*str, CHEM21 final ranking*)  
**Replacement Issues** (*str, justification for replacements*)  
**Replacement 1** (*str, solvent to be used as substitute if applicable. Must be an existing solvent in the database.*)  
**Replacement 2** (*str, solvent to be used as substitute is applicable. Must be an existing solvent in the database.*)  
**H3_phrase** (*str, the phrase associated with the worst H3XX number*)  
**H4_phrase** (*str, the phrase associated with the worst H4XX number*)
___

For an example DataFrame containing data for solvents Example1, Example2 and Example3:

```
import pandas as pd

solvent_df = pd.DataFrame({
                'PubChem ID': [111, 222, 333],
                'CAS': ['1-1-1', '2-2-2', '3-3-3'],
                'Family': ['Ethers', 'Halogenated', 'Alcohols'],
                'Solvent': ['Example1', 'Example2', 'Example3'],
                'Solvent Alternative Name': ['alt1', 'alt2', 'alt3'],
                'BP': [40, 85, 100],
                'FP': [100, 130, 105],
                'Worst H3xx': ['H350', 'H314', 'H314'],
                'Worst H4xx': ['H411', None, None],
                'Safety': [1, 5, 9],
                'Health': [4, 7, 7],
                'Env': [9, 9, 9],
                'Ranking Default': ['Recommended', 'Problematic', 'Highly Hazardous'],
                'Ranking Discussion': ['Recommended', 'Problematic', 'Highly Hazardous'],
                'Replacement Issues': [None, None, 'Carcinogenic'],
                'Replacement 1': ['Acetonitrile', 'Acetone', None],
                'Replacement 2': [None, 'Ethyl Acetate', None],
                'Replacement 1 Number': [7, 6, None],
                'Replacement 2 Number': [None, 23, None],
                'H3_phrase': ['May cause cancer', 'Causes severe skin burns and eye damage', 'Causes severe skin burns and eye damage'],
                'H4_phrase': ['Toxic to aquatic life with long lasting effects', None, None]
              })
```

The data can be added by:

```
from solvent_guide.add_solvent import add_solvent_from_dataframe

add_solvent_from_dataframe(solvent_df)
```

### Removing solvents

Solvents can be removed using remove_solvent():

```
from solvent_guide.remove_solvent import remove_solvent

remove_solvent()
```

and following the prompt:
```
Please enter the CAS number for the solvent you wish to remove:
```
All added solvents can be removed by resetting the Solvent Guide. This can be done via:

```
from solvent_guide.reset_solvents import reset_solvents

reset_solvents()
```

THIS WILL DELETE ALL ADDED SOLVENTS AND REMOVE ALL CHANGES MADE TO THE DATABASE SINCE INSTALLATION.
   
You will be prompted to confirm this:

```
CAUTION! Resetting the database will revert all changes made since installation. Are you sure? (y/n)
```

## Troubleshooting

In some cases, running the solvent guide via the command line has resulted in permission errors. These can be overcome by 
running with admin / sudo privileges.

