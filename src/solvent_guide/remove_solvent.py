import pandas as pd
import os


def remove_solvent():

    cas_to_remove = input('Please enter the CAS number for the solvent you wish to remove:')

    try:
        chem21 = pd.read_csv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"), index_col=0)

    except FileNotFoundError:
        chem21 = pd.read_csv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "sources/blueprints/solvent_guide/", "CHEM21_full.csv"), index_col=0)

    if cas_to_remove in chem21['CAS'].values:
        chem21_updated = chem21[~chem21['CAS'].str.match(cas_to_remove)]
        chem21_updated.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"))
        print('Solvent with CAS: %s was removed' % cas_to_remove)

    else:
        print('CAS number: %s was not found in the database!' % cas_to_remove)


if __name__ == '__main__':
    remove_solvent()
