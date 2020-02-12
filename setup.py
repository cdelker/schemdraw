import setuptools

with open('README.txt', 'r') as f:
	long_description = f.read()

setuptools.setup(
    name = 'SchemDraw',
    version = '0.6.0',
    description = 'Electrical circuit schematic drawing',
    author = 'Collin J. Delker',
    author_email = 'developer@collindelker.com',
    url = 'https://schemdraw.readthedocs.io/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = setuptools.find_packages(),
    keywords = ['circuit', 'schematic', 'electrical'],
    install_requires=['numpy', 'matplotlib'],
    classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    ],
)
