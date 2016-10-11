"""
sharpspringclient
"""
import sys
from setuptools import setup, find_packages

install_requires = [
    'requests'
]

# get the version information
exec(open('sharpspringclient/version.py').read())

setup(
    name = 'gizmo',
    packages = find_packages(),
    version = __version__,
    description = 'Python client for the SharpSpring API',
    url = 'https://github.com/oneilinteractive/SharpSpring-Client',
    author = "O'Neill Interactive",
    author_email = 'dev@oneilinteractive.com',
    long_description = __doc__,
    install_requires = install_requires,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Environment :: Web Environment',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
    ],
)
