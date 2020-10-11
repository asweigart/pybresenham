from setuptools import setup
import os
import re

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as fileObj:
    long_description = fileObj.read()

# Load version from module (without loading the whole module)
with open('pybresenham/__init__.py', 'r') as fileObj:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fileObj.read(), re.MULTILINE).group(1)


setup(
    name='PyBresenham',
    version=version,
    url='https://github.com/asweigart/pybresenham',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('A Python module of generators that generate x, y coordinates for various vector shapes such as lines, rectangles, etc. Named after Bresenham of line-algorithm fame.'),
    license='BSD',
    long_description=long_description,
    packages=['pybresenham'],
    test_suite='tests',
    install_requires=[],
    keywords="bresenham line circle drawing 2D geometry shapes vector bitmap rotate rotation vector2bitmap",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)