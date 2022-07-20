from glob import glob
import os

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

# Read the version from the main package.
with open('react/__init__.py') as f:
    for line in f:
        if '__version__' in line:
            _, version, _ = line.split("'")
            break

# Read the requirements from the file
requirements = [
    "numpy>=1.15",
    "scipy>=0.19.1",
    "nibabel>=3.0.0",
    "scikit-learn>=0.22"
]

setup(
    author='Ottavia Dipasquale, Matteo Frigo',
    author_email='ottavia.dipasquale@kcl.ac.uk',
    license='MIT',
    classifiers=[
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
    description='A Python package that implements REACT: Receptor-Enriched '
                'Analysis of Functional Connectivity by Targets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    name='react-fmri',
    packages=['react'],
    python_requires='>=3',
    scripts=glob('script/*'),
    url='https://github.com/ottaviadipasquale/react-fmri/',
    version=version,
    project_urls={
        'Source': 'https://github.com/ottaviadipasquale/react-fmri',
        'Bug Reports': 'https://github.com/ottaviadipasquale/react-fmri/issues',
        'Documentation': 'https://github.com/ottaviadipasquale/react-fmri/'
                         'blob/main/README.md',
    },
)
