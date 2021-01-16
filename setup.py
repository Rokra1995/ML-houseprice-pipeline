from setuptools import setup, find_packages

setup(
    name='funda',
    version='0.1.1',
    description='Example package for ML pipeline',
    packages=find_packages(include=['funda']),
    install_requires=[
        "pandas",
        "numpy",
        "plotnine",
        "scikit-learn",
        "matplotlib",
        'pyarrow',
        'nltk',
        'geopandas'
    ],
    python_requires="==3.8.5"
)