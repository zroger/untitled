# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Untitled',
    version='0.1',
    description='Find available project names.',
    url='http://github.com/zroger/untitled',
    author='Roger López',
    license='BSD',
    py_modules=['untitled'],
    entry_points={
        'console_scripts': [
            'untitled = untitled:main'
        ]
    },
)
