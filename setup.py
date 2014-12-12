from setuptools import setup  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='drf_haystack',

    version='0.0.1',

    description='A small library for django-haystack and django-rest-framework integration.',
    long_description=long_description,

    url='https://github.com/szelga/drf-haystack',

    author='Wasil W Siargiejczyk',
    author_email='szelga.wws@gmail.com',

    license='BSD',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
    ],

    keywords='development api search django',

    packages=['drf_haystack'],

    install_requires=[
        'django-haystack>=2',
        'djangorestframework>=2.4<3.0',
    ],

    extras_require = {
        #'test': ['coverage'],
    },
)
