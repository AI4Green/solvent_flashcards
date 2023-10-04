import pandas as pd
import os
from sources.blueprints.solvent_guide.routes import get_radar_plot

try:
    chem21 = pd.read_csv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"), index_col=0)

except FileNotFoundError:
    chem21 = pd.read_csv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "sources/blueprints/solvent_guide/", "CHEM21_full.csv"), index_col=0)


def add_solvent_from_dataframe(dataframe_to_add):

    for idx, row in dataframe_to_add.iterrows():
        if row['CAS'] in chem21['CAS'].values:
            dataframe_to_add.drop(idx, inplace=True)
            print('CAS Number: %s already in database, skipping...' % row['CAS'])

        else:
            dataframe_to_add.at[idx, 'Number'] = max(chem21['Number']) + 1
            dataframe_to_add.at[idx, 'graph'] = get_radar_plot(row['Safety'], row['Health'], row['Env'])

    try:
        assert set(chem21.columns) == set(dataframe_to_add.columns)

    except AssertionError:
        raise AssertionError('Columns %s are not included in the CHEM21 dataframe. Columns should match %s'
                             % ([x for x in dataframe_to_add.columns if x not in chem21.columns], chem21.columns))

    chem21_updated = pd.concat([chem21, dataframe_to_add])
    chem21_updated.to_csv('sources/blueprints/solvent_guide/CHEM21_full_updated.csv')


def add_solvent():

    print('Follow the prompts to add a flashcard for the new solvent. Prompts can be skipped by pressing Enter.')

    solvent_data = {}

    solvent_data['Number'] = max(chem21['Number']) + 1
    solvent_data['PubChem ID'] = input("Enter PubChem ID (if known):")
    solvent_data['CAS'] = input("Enter CAS Number (if known):")
    if solvent_data['CAS'] in chem21['CAS'].values:
        print('CAS Number: %s already in database, aborting...' % solvent_data['CAS'])
        exit()
    solvent_data['Family'] = input("Enter Solvent Family:")
    solvent_data['Solvent'] = input('Enter Solvent Name:')
    solvent_data['Solvent Alternative Name'] = input('Enter Alternative Solvent Name:')
    solvent_data['BP'] = input('Enter Boiling Point:')
    solvent_data['FP'] = input('Enter Flash point:')
    solvent_data['Worst H3xx'] = input('Enter Worst H3xx Statement:')
    solvent_data['H3_phrase'] = input('Enter Associated H3xx Hazard Phrase:')
    solvent_data['Worst H4xx'] = input('Enter Worst H4xx Statement:')
    solvent_data['H4_phrase'] = input('Enter Associated H4xx Hazard Phrase:')

    s = 0
    h = 0
    e = 0

    safety = input('Enter CHEM21 Safety Score:')
    if safety == '':
        print('No safety score provided, proceeding...')
        solvent_data['Safety'] = 'Not Available'
    else:
        solvent_data['Safety'] = int(safety)
        s = int(safety)

    health = input('Enter CHEM21 Health Score:')
    if health == '':
        print('No health score provided, proceeding...')
        solvent_data['Health'] = 'Not Available'
    else:
        solvent_data['Health'] = int(health)
        h = int(health)

    env = input('Enter CHEM21 Environment Score:')
    if env == '':
        print('No health score provided, proceeding...')
        solvent_data['Env'] = 'Not Available'
    else:
        solvent_data['Env'] = int(env)
        e = int(env)

    valid_rank = False
    while not valid_rank:
        ranking = input('Select Ranking (Recommended, Problematic, Hazardous, Highly Hazardous):').title()

        if ranking in ['Recommended', 'Problematic', 'Hazardous', 'Highly Hazardous']:
            valid_rank = True
            solvent_data['Ranking Discussion'] = ranking
        else:
            print('Input not recognised! Please try again')

    solvent_data['Replacement Issues'] = input('Enter Replacement Issues:')
    solvent_data['Replacement 1'] = str(input('Enter Possible Replacement 1:').capitalize())
    solvent_data['Replacement 1 Number'] = chem21[chem21['Solvent'].str.contains(solvent_data['Replacement 1'])]['Number'].values[0]
    solvent_data['Replacement 2'] = input('Enter Possible Replacement 2:').capitalize()
    solvent_data['Replacement 2 Number'] = chem21[chem21['Solvent'].str.contains(solvent_data['Replacement 2'])]['Number'].values[0]

    solvent_data['graph'] = get_radar_plot(s, h, e)


    chem21_updated = pd.concat([chem21, pd.DataFrame(solvent_data, index=[0])])
    #chem21_updated = chem21.append(solvent_data, ignore_index=True)
    chem21_updated.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "./sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"))


add_solvent()
