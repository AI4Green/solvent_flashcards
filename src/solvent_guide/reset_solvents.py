import pandas as pd
import os

def reset_solvents():

    confirm = input('CAUTION! Resetting the database will revert all changes made since installation. Are you sure? (y/n)')

    if confirm == 'y':

        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "./sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"))

    else:
        print('Aborting...')


reset_solvents()
