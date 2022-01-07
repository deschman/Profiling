# -*- coding: utf-8 -*-
"""Set up Profiling package."""


# %% Imports
from setuptools import setup, find_packages


# %% Script
setup(name='profiling',
      version="0.9.0",
      description="Automatically profile table by full name, source database type, and DSN.",
      author="Dan Eschman",
      author_email="deschman007@gmail.com",
      python_requires='>=3.8',
      install_requires=['pytest',
                        'sqlalchemy',
                        'pyodbc',
                        'pandas',
                        'dask[distributed]',
                        'modin',
                        'pandas_profiling'],
      packages=find_packages(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Database'])
