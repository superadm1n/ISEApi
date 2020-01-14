#!/usr/bin/env python
from setuptools import setup
from ISEApi import __version__

description = '''A clear and comprehensive Python wrapper the follows the overall structure of the ERS API'''

setup(
    name='ISEApi',
    version=__version__,
    packages=['ISEApi'],
    keywords='Cisco ISE ERS API',
    url='https://github.com/superadm1n/ISEApi',
    license='MIT',
    author='Kyle Kowalczyk',
    author_email='kowalkyl@gmail.com',
    description='Python Wrapper for the Cisco ISE ERS API',
    long_description=description,
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)