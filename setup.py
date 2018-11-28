import os

from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='pycommon_error',
    version=open("pycommon_error/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    description="Thin wrapper for pycommon-database and pycommon-server error handling",
    long_description=long_description,
    packages=find_packages(exclude=[
        'test',
    ]),
    install_requires=[
        # Used to manage fields
        'flask-restplus==0.12.1',
    ],
    extras_require={
        'testing': [
            # Used to provide testing help
            'pycommon-test==3.0.2',
        ]
    },
)
