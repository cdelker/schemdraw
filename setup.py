import setuptools

with open('README.txt', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'SchemDraw',
    version = '0.7a1',
    description = 'Electrical circuit schematic drawing',
    author = 'Collin J. Delker',
    author_email = 'developer@collindelker.com',
    url = 'https://schemdraw.readthedocs.io/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = ['schemdraw', 'SchemDraw'],
    package_dir={'schemdraw': 'schemdraw', 'SchemDraw': 'schemdraw'},
    keywords = ['circuit', 'schematic', 'electrical', 'flowchart', 'logic'],
    install_requires=['numpy', 'matplotlib'],
    classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    ],
)
