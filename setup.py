import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'schemdraw',
    version = '0.16a1',
    description = 'Electrical circuit schematic drawing',
    author = 'Collin J. Delker',
    author_email = 'schemdraw@collindelker.com',
    url = 'https://schemdraw.readthedocs.io/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/cdelker/schemdraw',
    },
    python_requires='>=3.8',
    packages = ['schemdraw',
                'schemdraw.elements',
                'schemdraw.logic',
                'schemdraw.dsp',
                'schemdraw.flow',
                'schemdraw.backends',
                'schemdraw.parsing'
               ],
    package_dir={'schemdraw': 'schemdraw'},
    keywords = ['circuit', 'schematic', 'electrical', 'flowchart', 'logic'],
    install_requires=['typing_extensions; python_version<"3.8"'],
    extras_require={
        'matplotlib':  ['matplotlib>=3.4'],
        'svgmath': ['ziafont>=0.4', 'ziamath>=0.6', 'latex2mathml']
    },
    package_data = {'schemdraw': ['py.typed']},
    zip_safe=False,
    classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    ],
)
