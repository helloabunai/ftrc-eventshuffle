import datetime

def test_new_event(test_new_event):
    """
    GIVEN:: Event model
    WHEN:: A new Event is created
    THEN:: Event.name field is set properly
    """
    assert test_new_event.name == 'FlaskTestEventName'

def test_new_date(test_new_date):
    """
    GIVEN:: Date model
    WHEN:: A new Date is created
    THEN:: Date.date_value field is set properly
    """

    assert test_new_date.date_value[0].strftime('%Y-%m-%d') == '1996-02-12'
    assert test_new_date.parent_event == 1

def test_new_person(test_new_person):
    """
    GIVEN:: Person model
    WHEN:: A new Person is created
    THEN:: Person fields are set properly
    """

    assert test_new_person.name == 'TestName'
    assert test_new_person.email == 'test@email.com'
    assert test_new_person.phone_number == '+358111119999'