import pandas as pd
import os

def reset_solvents():

    confirm = input('CAUTION! Resetting the database will revert all changes made since installation. THIS IS NOT RECOVERABLE. Are you sure? (y/n)')

    if confirm == 'y':

        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "./sources/blueprints/solvent_guide/", "CHEM21_full_updated.csv"))

        print('Database has been reset!')

    else:
        print('Aborting...')


if __name__ == '__main__':
    reset_solvents()
