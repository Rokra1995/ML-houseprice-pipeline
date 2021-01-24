from setuptools import setup, find_packages

setup(
    name='funda',
    version='1.0',
    description='ML Pipeline to train Random Forest and Neural Network for houespriceprediction based on funda dataset',
    packages=find_packages(include=['funda']),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        'pyarrow',
        'geopandas',
        'descartes'
    ],
    python_requires="==3.8.5"
)