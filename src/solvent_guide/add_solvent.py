import pandas as pd
import os
from .sources.blueprints.solvent_guide.routes import get_radar_plot

try:
    chem21 = pd.read_csv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"), index_col=0)

except FileNotFoundError:
    chem21 = pd.read_csv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "sources/blueprints/solvent_guide/", "CHEM21_full.csv"), index_col=0)

chem21 = chem21.fillna("")

def check_CHEM21_she(SHE):

    while True:
        try:
            inp = input('Enter CHEM21 ' + SHE + ' Score:')

            if inp == '':
                print('No ' + SHE + ' score provided, proceeding...')
                inp = -404
            else:
                inp = int(inp)

        except ValueError:
            print('Please insert CHEM21 ' + SHE + ' score as an integer!')

        else:
            break

    return inp


def add_solvent_from_dataframe(dataframe_to_add):

    new_data = False
    num = 0

    for idx, row in dataframe_to_add.iterrows():
        num = num + 1
        if row['CAS'] in chem21['CAS'].values:
            dataframe_to_add.drop(idx, inplace=True)
            print('CAS Number: %s already in database, skipping...' % row['CAS'])

        else:
            dataframe_to_add.at[idx, 'Number'] = max(chem21['Number']) + num
            dataframe_to_add.at[idx, 'graph'] = get_radar_plot(row['Safety'], row['Health'], row['Env'])

            if row['Replacement 1'] is not None:
                dataframe_to_add.at[idx, 'Replacement 1 Number'] = \
                chem21.loc[chem21['Solvent'] == row['Replacement 1'].capitalize(), 'Number'].values[0]

            if row['Replacement 2'] is not None:
                dataframe_to_add.at[idx, 'Replacement 2 Number'] = \
                chem21.loc[chem21['Solvent'] == row['Replacement 2'].capitalize(), 'Number'].values[0]

            new_data = True

    if new_data:
        try:
            assert set(chem21.columns) == set(dataframe_to_add.columns)

        except AssertionError:

            raise AssertionError('Columns %s are not included in the CHEM21 dataframe. Columns should match %s'
                                 % ([x for x in dataframe_to_add.columns if x not in chem21.columns], chem21.columns))

        chem21_updated = pd.concat([chem21, dataframe_to_add], ignore_index=False)
        chem21_updated.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"))

        print('Data successfully added!')


def add_solvent():

    print('Follow the prompts to add a flashcard for the new solvent. Prompts can be skipped by pressing Enter. For more '
          'detail about these prompts, please see the documentation: https://pypi.org/project/solvent-guide/')

    solvent_data = {}

    solvent_data['Number'] = max(chem21['Number']) + 1
    solvent_data['PubChem ID'] = input("Enter PubChem ID (if known):")
    solvent_data['CAS'] = input("Enter CAS Number (if known):")
    if solvent_data['CAS'] in chem21['CAS'].values:
        print('CAS Number: %s already in database, aborting...' % solvent_data['CAS'])
        exit()
    solvent_data['Family'] = input("Enter Solvent Family:").capitalize()
    solvent_data['Solvent'] = input('Enter Solvent Name:')
    solvent_data['Solvent Alternative Name'] = input('Enter Alternative Solvent Name:')
    solvent_data['BP'] = input('Enter Boiling Point:')
    solvent_data['FP'] = input('Enter Flash point:')
    solvent_data['Worst H3xx'] = input('Enter Worst H3xx Statement:')

    if solvent_data['Worst H3xx'] == '':
        solvent_data['H3_phrase'] = 'None'

    else:
        solvent_data['H3_phrase'] = input('Enter Associated H3xx Hazard Phrase:')

    solvent_data['Worst H4xx'] = input('Enter Worst H4xx Statement:')

    if solvent_data['Worst H4xx'] == '':
        solvent_data['H4_phrase'] = 'None'

    else:
        solvent_data['H4_phrase'] = input('Enter Associated H4xx Hazard Phrase:')

    s = check_CHEM21_she('Safety')
    h = check_CHEM21_she('Health')
    e = check_CHEM21_she('Env')

    solvent_data['Safety'] = s
    solvent_data['Health'] = h
    solvent_data['Env'] = e

    valid_rank = False
    while not valid_rank:
        ranking = input('Select Ranking (Recommended, Problematic, Hazardous, Highly Hazardous):').title()

        if ranking in ['Recommended', 'Problematic', 'Hazardous', 'Highly Hazardous']:
            valid_rank = True
            solvent_data['Ranking Discussion'] = ranking
        else:
            print('Input not recognised! Please try again')

    solvent_data['Replacement Issues'] = input('Enter Replacement Issues:')

    replacement_1 = input('Enter Possible Replacement 1 (please ensure this matches an existing solvent in the database):').lower()

    solvent_data['Replacement 1'] = replacement_1.capitalize()

    solvent_names = [x.lower() for x in chem21['Solvent'].values]
    alternative_solvent_names = [x.lower() for x in chem21['Solvent Alternative Name'].values]

    if replacement_1 in solvent_names:
        solvent_data['Replacement 1 Number'] = chem21.iloc[solvent_names.index(replacement_1)].Number

    elif replacement_1 in alternative_solvent_names:
        solvent_data['Replacement 1 Number'] = chem21.iloc[alternative_solvent_names.index(replacement_1)].Number

    else:
        solvent_data['Replacement 1 Number'] = ""

    replacement_2 = input('Enter Possible Replacement 2 (please ensure this matches an existing solvent in the database):').lower()
    solvent_data['Replacement 2'] = replacement_2.capitalize()

    if replacement_2 in solvent_names:
        solvent_data['Replacement 2 Number'] = chem21.iloc[solvent_names.index(replacement_2)].Number

    elif replacement_2 in alternative_solvent_names:
        solvent_data['Replacement 2 Number'] = chem21.iloc[alternative_solvent_names.index(replacement_2)].Number

    else:
        solvent_data['Replacement 2 Number'] = ""

    solvent_data['graph'] = get_radar_plot(s, h, e)

    chem21_updated = pd.concat([chem21, pd.DataFrame(solvent_data, index=[0])])

    chem21_updated.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"))


if __name__ == '__main__':
    add_solvent()