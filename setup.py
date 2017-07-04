try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'SchemDraw',
    packages = ['SchemDraw'],
    version = '0.3.1a',
    description = 'Electrical circuit schematic drawing',
    author = 'Collin J. Delker',
    author_email = 'developer@collindelker.com',
    url = 'http://cdelker.bitbucket.io/SchemDraw',
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
