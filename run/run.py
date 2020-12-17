import json
from funda.load_data import DataLoader
# important: for the above import to work, the package needs to be
# installed in the conda environment using e.g. pip install -e .
# from the package root, or python setup.py develop.
# See https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
# for a good guide to this

def main():
    # here goes the pipeline code
    with open('run/conf.json', 'r') as f:
        conf = json.load(f)
    data_loader = DataLoader(base_folder=conf['base_folder'])
    funda_2018 = data_loader.load_funda_data_2018()
    print(funda.head())


if __name__ == "__main__":
    # the main function above is called when the script is
    # called from command line
    main()