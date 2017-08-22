from codecs import open
from os import path

from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()


setup(
    name='croaring',
    version='0.0.2',

    description='Compressed integer sets based on Roaring bitmaps.',
    long_description=readme,
    url='https://github.com/zacharyvoase/croaring.py',

    author='Zachary Voase',
    author_email='zack@meat.io',
    license='UNLICENSE',

    packages=find_packages(exclude=['test']),

    setup_requires=[
        "cffi>=1.4.0",
        "six>=1.10.0",
    ],
    install_requires=[
        "cffi>=1.4.0",
        "six>=1.10.0",
    ],

    cffi_modules=["croaring_build.py:FFI_BUILDER"],
)
