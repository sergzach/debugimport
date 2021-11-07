import sys
from setuptools import setup

setup(
    name='testapp',        
    version='0.1.0',        
    description='A sample library to test by debugimport.',
    author='Sergey Zakharov',
    author_email='sergzach@gmail.com',
    packages=['testapp'],
    package_dir={'testapp': 'testapp'},
    python_requires='>=3.5',
    setup_requires=[],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)