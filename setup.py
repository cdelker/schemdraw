import setuptools

with open('README.txt', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'SchemDraw',
    version = '0.7.1',
    description = 'Electrical circuit schematic drawing',
    author = 'Collin J. Delker',
    author_email = 'developer@collindelker.com',
    url = 'https://schemdraw.readthedocs.io/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    packages = ['schemdraw', 'SchemDraw',
                'schemdraw.elements',
                'schemdraw.logic',
                'schemdraw.dsp',
                'schemdraw.flow',
                'schemdraw.backends',
                'SchemDraw.elements',
                'SchemDraw.logic',
                'SchemDraw.dsp',
                'SchemDraw.flow',
                'SchemDraw.backends'],
    package_dir={'schemdraw': 'schemdraw',
                 'SchemDraw': 'schemdraw',
                 },
    keywords = ['circuit', 'schematic', 'electrical', 'flowchart', 'logic'],
    install_requires=['numpy', 'matplotlib'],
    classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    ],
)
