# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path

readme = Path('README.md')
if readme.is_file():
    readme = readme.read_text().replace('```', '')
else:
    readme = ''

setup(
    name='geminipy',
    version='0.0.6',
    packages=find_packages('geminipy'),
    url='https://github.com/pl0mo/geminipy',
    license='GNU GPL',
    author='Mike Marzigliano',
    author_email='marzig76@gmail.com',
    zip_safe=False,
    long_description=readme,
    description='API client for Gemini'
)
