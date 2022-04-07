#############################
## EventShuffle API Server ##
#############################

## imports
from collections import defaultdict
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

## Temporary data
placeholder_data = {'data': {
    'eventID': {
        0: 'event0',
        1: 'event1',
        2: 'event2',
        3: 'event3'
        },
    'eventName': {
        0: 'eventName0',
        1: 'eventName1',
        2: 'eventName2',
        3: 'eventName3'
        },
    'eventLocation': {
        0: 'eventLoc0',
        1: 'eventLoc1',
        2: 'eventLoc2',
        3: 'eventLoc3'
        }
    }
}

## Endpoints for API
class Event(Resource):

    def get(self):
        """
        Connect to the PSQL database, retreive Event entries
        JSONify and return with OK code (200)
        If exception, return with error code (500, i guess for now)
        """
        return (placeholder_data, 200)

    def post(self):
        """
        Connect to the PSQL database, add Event entry
        Flask ReqParse takes in data to be added.
        """

        ## incoming data from POST request
        post_data = request.args.to_dict()

        ## Check if any EVENTID (i.e. primary key) already exists in the dictionary
        if post_data['eventID'] in placeholder_data['data']['eventID'].values():
            return {
            'message': 'EventID {} already exists, sorry.'.format(post_data['eventID'])
        }, 401

        ## Temporary function while working with dictionary
        ## For each sub-dictionary in data, get highest IDX key value
        ## iterate on that, then place the same sub-dict (from POST) value as new entry
        for subkey, subdict in placeholder_data['data'].items():
            idx_target = max(k for k, v in subdict.items() if k != 0)
            idx_place = idx_target + 1
            subdict[idx_place] = post_data[subkey]

        ## return all data, demonstrating POST success
        return (placeholder_data, 200)

## Handler class to create Flask and instantiate endpoints + associated classes
class shuffleAPI:
    def __init__(self):

        """
        This is shuffleAPI, the module responsible for launching the API server.

        :param self: self (ha!) explanatory
        :return: None
        :raises: None
        """
    
        ## set up API
        self.shuffleAPP = Flask(__name__)
        self.shuffleAPI = Api(self.shuffleAPP)
 
        ## add Event endpoint
        self.shuffleAPI.add_resource(Event, '/api/v1/event/')

        ## run the Flask
        self.shuffleAPP.run()
