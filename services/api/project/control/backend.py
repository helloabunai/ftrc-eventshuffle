import datetime
from project.common.database import db
from flask import Flask, jsonify, request, abort
from project.control.models import Event, Date, Person, PersonDate
from project.common.exceptions import RecordNotFound
from sqlalchemy import and_

#####################################################
#####################################################
## The main app! 
## Created in the backend to prevent circular
## imports from app.py to elsewhere
shuffle_app = Flask(__name__)
shuffle_app.config.from_object("project.config.Config")
db.init_app(shuffle_app)

#####################################################
#####################################################
## CLI based functions
## Called from docker commands / makefile script
def create_db():

    """
    Drop entire DB if present
    Create fresh
    Called from CLI (i.e. docker command)
    """

    db.drop_all() #remove after dev
    db.create_all()
    db.session.commit()

def seed_db():

    """
    Populate the database with dummy data as
    seen in the assignment spec on github
    Called from CLI (i.e. docker command)
    """

    create_db()

    ######################################################
    ## Create the people!
    john_obj = Person(name = "John", email="john@email.com", phone_number='+358453250000')
    julia_obj = Person(name = "Julia", email="julia@email.com", phone_number='+358453250001')
    paul_obj = Person(name = "Paul", email="paul@email.com", phone_number='+358453250002')
    daisy_obj = Person(name = "Daisy", email="daisy@email.com", phone_number='+358453250003')
    dick_obj = Person(name = "Dick", email="dick@email.com", phone_number='+358453250004')
    people_to_add = [john_obj, julia_obj, paul_obj, daisy_obj, dick_obj]
    db.session.bulk_save_objects(people_to_add, return_defaults=True)
    db.session.commit()

    ######################################################
    ## Dummy event one : Jake's secret party
    event_jake_party = Event(name = "Jake's secret party")
    db.session.add(event_jake_party)
    db.session.commit() ## commit so we can get event ID from DB
    
    ## add dates before votes
    jake_jan1 = Date(date_value = datetime.date(2014,1,1), parent_event = event_jake_party.id)
    jake_jan5 = Date(date_value = datetime.date(2014,1,5), parent_event = event_jake_party.id)
    jake_jan12 = Date(date_value = datetime.date(2014,1,12), parent_event = event_jake_party.id)
    jake_dates = [jake_jan1, jake_jan5, jake_jan12]
    db.session.bulk_save_objects(jake_dates, return_defaults=True)
    db.session.commit() ## commit so we can get date ID from DB

    ## create person-date association
    jakeparty_votes = [
        ## voting for jan 1st for jake's party
        PersonDate(person_id = john_obj.id, date_id = jake_jan1.id),
        PersonDate(person_id = julia_obj.id, date_id = jake_jan1.id),
        PersonDate(person_id = paul_obj.id, date_id = jake_jan1.id),
        PersonDate(person_id = daisy_obj.id, date_id = jake_jan1.id),

        ## voting for jan 5th for jake's party
        PersonDate(person_id = john_obj.id, date_id = jake_jan5.id),
        PersonDate(person_id = daisy_obj.id, date_id = jake_jan5.id),

        ## voting for jan 12th for jake's party
        PersonDate(person_id = paul_obj.id, date_id = jake_jan12.id),
        PersonDate(person_id = daisy_obj.id, date_id = jake_jan12.id),
        PersonDate(person_id = dick_obj.id, date_id = jake_jan12.id)
    ]
    db.session.bulk_save_objects(jakeparty_votes, return_defaults=True)
    db.session.commit()

    ######################################################
    ## Dummy event two : Bowling night
    event_bowling = Event(name = "Bowling night")
    db.session.add(event_bowling)
    db.session.commit()

    ## add dates for bowling
    bowling_jan1 = Date(date_value = datetime.date(2014, 1, 1), parent_event = event_bowling.id)
    bowling_dec24 = Date(date_value = datetime.date(2022, 12, 24), parent_event = event_bowling.id)
    bowling_july31 = Date(date_value = datetime.date(2022, 7, 31), parent_event = event_bowling.id)
    bowling_dates = [bowling_jan1, bowling_dec24, bowling_july31]
    db.session.bulk_save_objects(bowling_dates, return_defaults=True)
    db.session.commit()

    ## votes for bowling
    bowling_votes = [
        PersonDate(person_id = paul_obj.id, date_id = bowling_dec24.id),
        PersonDate(person_id = dick_obj.id, date_id = bowling_july31.id),
    ]
    db.session.bulk_save_objects(bowling_votes, return_defaults=True)
    db.session.commit()

    ######################################################
    ## Dummy event three : Tabletop gaming
    event_tabletop = Event(name = "Tabletop gaming")
    db.session.add(event_tabletop)
    db.session.commit()

    ## add dates for bowling
    ## don't need objects as not creating votes here
    tabletop_oct31 = Date(date_value = datetime.date(1234, 10, 31), parent_event = event_tabletop.id)
    tabletop_nov18 = Date(date_value = datetime.date(2000, 11, 18), parent_event = event_tabletop.id)
    tabletop_dates = [tabletop_oct31, tabletop_nov18]
    db.session.bulk_save_objects(tabletop_dates, return_defaults=True)
    db.session.commit()

    ## votes for bowling
    tabletop_votes = [
        PersonDate(person_id = julia_obj.id, date_id = tabletop_oct31.id),
        PersonDate(person_id = daisy_obj.id, date_id = tabletop_oct31.id)
    ]
    db.session.bulk_save_objects(tabletop_votes, return_defaults=True)
    db.session.commit()

#####################################################
#####################################################
## Functions called by API endpoints
## Interact with database / etc
def handle_new_event(in_json):
    
    """
    Backend function called from the API endpoint
    for adding a new event to the PSQL database

    :param: json (pre-validated against schema)
    :type: dict / json
    :returns: dict / json (created Event object PSQL ID)
    """

    ## Create an event object, commit to DB
    ## It will already be checked against schema before reaching here
    ## so we can assume things are in place without issue
    event_object = Event(name = in_json['name'])
    db.session.add(event_object)
    db.session.commit()

    ## get the new Event object's PSQL ID
    ## used to assign as foreign key for each date object we make
    current_event_id = event_object.id
    requested_dates = in_json['dates']

    ## for all dates present in the JSON body
    ## cast the string to list of integers
    ## Create date object using datetime
    ## and assign the above Event's ID as parent_event
    ## send to DB
    for indv_date in requested_dates:
        casted_date = [int(s) for s in indv_date.split('-')]
        curr_date = Date(
            date_value = datetime.date(casted_date[0], casted_date[1], casted_date[2]),
            parent_event = current_event_id
        )
        db.session.add(curr_date)
        db.session.commit()

    ## return a JSON response back to the client
    return {'id':current_event_id}

def get_event_subsidiaries(event_id):

    """
    Backend function called from the API endpoint
    for getting an event object, and all associated data
    from date and person (i.e. from DatePerson for current event)

    :param: int event_id
    :type: integer
    :returns: dict / json
    """

    ## Get Event object + as dict
    requested_object = Event.query.get(event_id)
    event_values = requested_object.__dict__
    
    ## get dates associated with this event ID
    ## format to YYYY-MM-DD
    dates_for_event = db.session.query(Date).filter(Date.parent_event == event_id)
    dates_serialised = [x.__dict__ for x in dates_for_event]
    event_values['dates'] = [x['date_value'].strftime('%Y-%m-%d') for x in dates_serialised]

    ## get person <-relationship-> dates i.e. votes!
    votes_dicts = []
    for curr_date in dates_serialised:
        indv_vote_dict = {}
        ## we got dates, already filtered with Date.parent_event == event_id, so don't need to check event
        date_person_relations = db.session.query(PersonDate).filter(PersonDate.date_id == curr_date['id'])
        relations_serialised = [x.__dict__ for x in date_person_relations]
        voter_ids = [x['person_id'] for x in relations_serialised]
        
        ## if no votes for current date, don't return an entry, otherwise do (map person id to name)
        if not voter_ids:
            pass
        else:
            indv_vote_dict['date'] = str(curr_date['date_value'])
            indv_vote_dict['people'] = [Person.query.get(x).name for x in voter_ids]
            votes_dicts.append(indv_vote_dict)

    event_values['votes'] = votes_dicts

    ## create copy of output (just to be careful about mutability)
    ## remove sqlalchemy timestate for clean output
    pruned_copy = event_values 
    if "_sa_instance_state" in pruned_copy:
        pruned_copy.pop('_sa_instance_state', None)
    return pruned_copy

def add_event_votes(event_id, json_body):

    """
    Backend function called from the API endpoint
    for adding votes to an existing object.
    Already checked if event exists, before calling here.

    :param: int event_id
    :type: integer
    :returns: dict / json
    """

    ## requested dates from JSON body
    request_user = json_body['name']
    requested_dates = json_body['votes']

    ## Get Event object + as dict
    requested_object = Event.query.get(event_id)
    event_values = requested_object.__dict__
    
    ## get dates associated with this event ID
    ## format to YYYY-MM-DD
    dates_for_event = db.session.query(Date).filter(Date.parent_event == event_id)
    dates_serialised = [x.__dict__ for x in dates_for_event]
    event_values['dates'] = [x['date_value'].strftime('%Y-%m-%d') for x in dates_serialised]

    #######################################################
    ## for each date listed in the POST
    for vote in requested_dates:
        
        ## check if requested date exists for current event
        ## since there may be unknown dates here, must filter over all
        ## matching date ID + event ID
        present_dates = db.session.query(Date).filter(and_(
            Date.date_value == vote,
            Date.parent_event == event_id
            )
        )

        requested_votes = [] ## PersonDate i.e. vote objects
        ## if requested date doesn't exist, create
        if not [x.__dict__ for x in present_dates]:
            
            date_obj = datetime.datetime.strptime(vote, "%Y-%m-%d")
            current_missing_date = Date(
                date_value = date_obj, parent_event = event_id
            )
            db.session.add(current_missing_date)
            db.session.commit()

        ## now dates should be created if they didn't exist,
        ## or they existed anyway for this event
        ## and dates are unique PER EVENT, so proceed;
        
        ## Get the person requesting this vote!
        ## According to the instructions, the JSON body will contain "name" as an ident
        ## so... names have to be unique if that is the case (they are in this DB)

        ## Ensure the person + id exists, though..
        request_user_obj = db.session.query(Person).filter(Person.name==request_user)
        try: request_user_id = request_user_obj.first().__dict__['id']
        except AttributeError: return abort(500)

        ## get current date ID, since it will exist and be unique date for THIS event
        ## we can use first() as there will be one UNIQUE date per event
        request_date_id = present_dates.first().__dict__['id']

        ## Create the person-date association (i.e. a vote)
        requested_votes.append(
            PersonDate(person_id = request_user_id, date_id = request_date_id)
        )
        
        ## save to DB
        db.session.bulk_save_objects(requested_votes, return_defaults=True)
        db.session.commit()

    #######################################################
    ## OK! Votes are now saved along with relations to events/people
    ## Get information to return as per the specification
    ## This behaviour is identical to get_event_subsidiaries, so call that
    post_vote_values = get_event_subsidiaries(event_id)
    return post_vote_values

def calculate_best_date(event_id):

    """
    Backend function called from the API endpoint
    for determining the best date for ALL people.
    Already checked if event exists, before calling here.

    :param: int event_id
    :type: integer
    :returns: dict / json
    """

    ## Get Event object + as dict
    requested_object = Event.query.get(event_id)
    event_values = requested_object.__dict__

    ## get dates associated with this event ID
    ## format to YYYY-MM-DD
    dates_for_event = db.session.query(Date).filter(Date.parent_event == event_id)
    dates_serialised = [x.__dict__ for x in dates_for_event]
    event_values['dates'] = [x['date_value'].strftime('%Y-%m-%d') for x in dates_serialised]

    ## get all people that have voted for any date in this event
    event_all_voters = []; potential_dates = []
    for curr_date in dates_serialised:
        ## we got dates, already filtered with Date.parent_event == event_id, so don't need to check event
        date_person_relations = db.session.query(PersonDate).filter(PersonDate.date_id == curr_date['id'])
        relations_serialised = [x.__dict__ for x in date_person_relations]
        voter_ids = [x['person_id'] for x in relations_serialised]

        ## append potential date with voter amount 
        ## removes the need to loop over all event dates again
        ## outside of loop, we will only return events with len(voter_ids) == total_event_participants
        curr_potential_date = {
            'date': curr_date['date_value'].strftime('%Y-%m-%d'), ## need to reformat datetime object
            'voter_amount': len(voter_ids),
            'people': [Person.query.get(x).name for x in voter_ids]
        }
        potential_dates.append(curr_potential_date)

        ## append unique (for this event, out of all event dates) voter id
        for voter_id in voter_ids:
            if voter_id not in event_all_voters:
                event_all_voters.append(voter_id)

    ## determine total participants for this event
    ## i.e. amount of unique voter IDs, from all dates, for this event only
    total_event_participants = len(event_all_voters)

    ## List comprehension to only retain dicts with voter_amount == total_event_participants
    ## filter empty dicts that the comprehension creates, but does not populate
    ## from now valid+populated dict list, remove 'voter_amount' as not required/requested
    suitable_dates = [{k: v for k,v in x.items() if x['voter_amount'] == total_event_participants} for x in potential_dates]
    suitable_dates = list(filter(None, suitable_dates))
    suitable_dates = [{k: v for k,v in x.items() if k != 'voter_amount'} for x in suitable_dates]
    
    ## append the now formated/validated list of dicts to our main return object
    event_values['suitableDates'] = suitable_dates

    ## create copy of output (just to be careful about mutability and ORM persistance)
    ## remove sqlalchemy timestate for clean output
    pruned_copy = event_values 
    if "_sa_instance_state" in pruned_copy:
        pruned_copy.pop('_sa_instance_state', None)
    return pruned_copy