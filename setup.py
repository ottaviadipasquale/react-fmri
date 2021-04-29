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
    description='A Python package that implements REACT: Receptor-enriched '
                'analysis of ...',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['nibabel', 'numpy', 'scikit-learn', 'scipy'],
    name='react-fmri',
    packages=['react'],
    python_requires='>=3',
    scripts=['script/react', 'script/react_mask'],
    url='',
    version=version,
    project_urls={
        'Source': '',
        'Bug Reports': '',
        'Documentation': '',
    },
)
