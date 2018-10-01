import os

from setuptools import setup, find_packages

from pycommon_error._version import __version__

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='pycommon_error',
    version=__version__,
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
            # Used to run tests
            'nose==1.3.7',
            # Used to provide testing help
            'pycommon-test==1.10.2',
        ]
    },
)
