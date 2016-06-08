#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='dockerrun',
      version='0.1.0',
      description='A dead simple Python library for running Docker commands',
      author='Ben Firshman',
      author_email='ben@firshman.co.uk',
      url='https://github.com/bfirsh/dockerrun',
      packages=find_packages(exclude=['tests.*', 'tests']),
      install_requires=['docker-py'],
     )
