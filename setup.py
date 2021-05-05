from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()


# Read the version from the main package.
with open('react/__init__.py') as f:
    for line in f:
        if '__version__' in line:
            _, version, _ = line.split("'")
            break


setup(
    author='Ottavia Dipasquale, Matteo Frigo',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
    description='A Python package that implements REACT: Receptor-Enriched '
                'Analysis of Functional Connectivity by Targets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['nibabel>=3.0.0', 'numpy', 'scikit-learn>=0.22', 'scipy'],
    name='react-fmri',
    packages=['react'],
    python_requires='>=3',
    scripts=['script/react', 'script/react_masks', 'script/react_normalize'],
    url='https://github.com/ottaviadipasquale/react-fmri/',
    version=version,
    project_urls={
        'Source': 'https://github.com/ottaviadipasquale/react-fmri',
        'Bug Reports': 'https://github.com/ottaviadipasquale/react-fmri/issues',
        'Documentation': 'https://github.com/ottaviadipasquale/react-fmri/'
                         'blob/main/README.md',
    },
)
