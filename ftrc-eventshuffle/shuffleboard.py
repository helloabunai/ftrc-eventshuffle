__version__ = '0.1.0'
__author__ = 'alastairm@gmail.com'

#################################################
## ShuffleBoard! The Futurice EventShuffle API ##
#################################################

## imports
import os
import sys
import argparse
import pkg_resources
import logging as log

## submodules
from . import api

## control logic
class shuffleBoard:
    def __init__(self):
        
        """
        This is ShuffleBoard, the futurice EventShuffle API in Flask.

        :param self: self (ha!) explanatory
        :return: None
        :raises: None
        """

        ##
        ## Package Data
        self.seed_data = pkg_resources.resource_filename(__name__, 'data/placeholder.csv')
        
        ##
        ## Argument parser (i.e. launch server OR interact via CLI)
        ## Check args are present or not; print help/exit
        self.parser = argparse.ArgumentParser(prog='shuffleboard', description='Shuffleboard: EventShuffle API implementation')
        mode_group = self.parser.add_mutually_exclusive_group()
        mode_group.add_argument('-l', '--launch', help="Launch the Flask API server!", action='store_true')
        mode_group.add_argument('-i', '--input', help="Open the CLI to interact with the backend.", action='store_true')
        if len(sys.argv) < 2: self.parser.print_help(); sys.exit(1)
        self.args = self.parser.parse_args()

        ##
        ## connect to database server

        ##
        ## check if data is present

        ##
        ## if not, use included CSV to populate

        ##
        ## Flask API Server
        if self.args.launch:
            api.shuffleAPI()


## entrypoint from terminal
def main():
    try:
        shuffleBoard()
    except KeyboardInterrupt:
        log.error("{}{}".format('SHUF::', ' Keyboard Interrupt detected! Goodbye :)'))
        sys.exit(2)