#!/usr/bin/env python
from setuptools import setup

setup(
    name='word_normalizer',
    version='0.1.0',
    description='Normalizing text data',
    url='https://bitbucket.org/mkaranasou/word_normalizer/',
    author='Maria Karanasou',
    author_email='karanasou@gmail.com',
    tests_require=[
        'httpretty',
        'nose'
    ],
    test_suite='nose.collector',
    requires=[
        # 'simplejson (>=3.2.0)',
        # 'redis'
    ],
    install_requires=[
        'enum==0.4.6',
        'nltk==3.2.1',
        'pyenchant>=1.6.6',
        'wheel==0.24.0',
    ],
    include_package_data=True,
    # package_dir={'': 'word_normalizer'},
    # data_files=[('', ['LICENSE.txt'])],
    package_data={
        "*.txt": ["word_normalizer/data/*.txt", ],
        "*.json": ["word_normalizer/data/*.json", ],
        "*.csv": ["word_normalizer/data/*.csv", ]
    },
    packages=[
        'word_normalizer',
        'word_normalizer.models',
        'word_normalizer.tests',
        'word_normalizer.utils',
        'word_normalizer.data',
    ]
)
