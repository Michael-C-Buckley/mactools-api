# MacTools API Setup

# Python Modules
from setuptools import setup, find_packages

# Local Modules
from app import __version__

DESCRIPTION = 'MacTools API Server Expansion Module',

with open('README.md', 'r', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='MacTools API',
    author='Michael Buckley',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'mactools',
        'fastapi',
        'slowapi',
        'uvicorn'
    ],
    keywords=['python','networking','network','mac','oui','ieee','api']
)