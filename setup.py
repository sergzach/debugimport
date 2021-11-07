import sys
from setuptools import setup

setup(
    name='debugimport',        
    version='0.1.0',        
    description='A library to import a module or a package from source '
        '`python` code when `debug=True` or import normally otherwise.'
    author='Sergey Zakharov',
    author_email='sergzach@gmail.com',
    packages=['debugimport'],
    package_dir={'debugimport': 'debugimport'},
    python_requires='>=3.5',
    setup_requires=['pytest-runner'],
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
