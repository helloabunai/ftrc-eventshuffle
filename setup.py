###############################
## Futurice EventShuffle API ##
##     Install script        ##
###############################

## Imports
from os import path
from codecs import open
from setuptools import setup, find_packages

## Get the long description from the relevant file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

##
## Begin the installation process
setup(
    name='ftrc-eventshuffle',

    version='0.1.0', #maj.min.patch

    description='EventShuffle API',
    long_description=long_description,
	long_description_content_type='text/markdown',
	python_requires='>=3.8',
    # The project's main homepage.
    url='https://github.com/helloabunai/ftrc-eventshuffle',

    # Author details
    author='Alastair Maxwell',
    author_email='alastairm@gmail.com',

    # License to ship the package with
    license='GPLv3',
    # additional information
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
		'Intended Audience :: End Users/Desktop',

        # Classifier matching license flag from above
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

		# Specific version of the python interpreter(s) that are supported
		# by this package.
        'Programming Language :: Python :: 3.8',

		## And so on
        'Environment :: Console',
		'Operating System :: POSIX'
    ],

    # What does the project relate to?
    keywords='hire-me-thank-you',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['input',
									'lib',
									'ftrc-eventshuffle.egg-info',
									'build',
									'dist',
									'logs',
                                    'tests',
									]),

    # List run-time/third party dependencies here.
    install_requires=[
        'Flask',
        'pandas',
    ],

    # Data to include with the software
    package_data={'ftrc-shuffle': ['data/initial_data.csv']},
	include_package_data=True,

	# Interpretation targets
    entry_points={
        'console_scripts': ['shuffleboard=ftrc-eventshuffle.entrypoint:main',],
    },
)