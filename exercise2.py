#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"

import re
import datetime
import json

######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]

######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None


#####################
# HELPER FUNCTIONS ##
#####################
def is_more_than_x_years_ago(x, date_string):
    """
    Check if date is less than x years ago.

    :param x: int representing years
    :param date_string: a date string in format "YYYY-mm-dd"
    :return: True if date is less than x years ago; False otherwise.
    """

    now = datetime.datetime.now()
    x_years_ago = now.replace(year=now.year - x)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    return (date - x_years_ago).total_seconds() < 0


def decide(input_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """

    entries_file = open(input_file)
    entries_string = entries_file.read()
    entries_data = json.loads(entries_string)
    entries_file.close()

    file_of_countries = open(countries_file)
    countries_string = file_of_countries.read()
    global COUNTRIES
    COUNTRIES = json.loads(countries_string)
    file_of_countries.close()
    # create a decision list
    final_decision_list = []
    # check if the entry is in the dictionary
    for entry in entries_data:
        decision_list = []
        # check if the required fields are included
        if not check_required_fields(entry):
            decision_list.append("Reject")
        # check passport format
        if not valid_passport_format(entry['passport']):
            decision_list.append("Reject")
        # check birthday format
        if not valid_date_format(entry['birth_date']):
            decision_list.append("Reject")
        # check if the country is in the list
        if not known_location(entry['from']) or not known_location(entry['home']):
            decision_list.append("Reject")
        # check if there is a via in the entry
        if "via" in entry:
            if not known_location(entry["via"]):
                decision_list.append("Reject")
            if known_location(entry["via"]):
                decision_list.append("Quarantine")
        # check if the contry is Kanada
        if check_home(entry["home"]):
            decision_list.append("Accept")
        # check if it has medical advisory
        if check_quarantine(entry["from"]):
            decision_list.append("Quarantine")
        # check if the person needs visa
        if check_visa_requirement(entry["from"],entry["entry_reason"]):
            if "visa" not in entry:
                decision_list.append("Reject")
            else:
                # reject if the visa is not valid
                if not valid_date_format(entry["visa"]["date"]):
                    decision_list.append("Reject")
                else:
                    # check the visa date
                    if is_more_than_x_years_ago(2,entry["visa"]["date"]):
                        decision_list.append("Reject")
                    # check code format
                    if not valid_visa_format(entry["visa"]["code"]):
                        decision_list.append("Reject")
        # accept if all passed
        decision_list.append("Accept")
        # make the final decision
        final_decision = conflict_decision_resolver(decision_list)
        # add dicesion to the list
        final_decision_list.append(final_decision)


    return final_decision_list


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """

    # separate the passport number by dashes
    checklist = passport_number.split('-')

    # if total number of character groups is not five, the format is not valid
    if len(checklist) != 5:
        return False

    # check each group of character
    for i in range(5):

        # if total number of characters in each group is not five, the format is not valid
        if len(checklist[i]) != 5:
            return False

        # if a character is not alphanumeric, the format is not valid
        if not checklist[i].isalnum():
            return False

    # passed all checks, the format is valid
    return True


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """
    # separate the visa code by dashes
    checklist = visa_code.split('-')

    # if total number of character groups is not five, the format is not valid
    if len(checklist) != 5:
        return False

    # check each group of character
    for i in range(5):

        # if total number of characters in each group is not five, the format is not valid
        if len(checklist[i]) != 5:
            return False

        # if a character is not alphanumeric, the format is not valid
        if not checklist[i].isalnum():
            return False

    # passed all checks, the format is valid
    return True

def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    # separate the date string by dashes
    checklist = date_string.split('-')

    # if total number of character groups is not three, the format is not valid
    if len(checklist) != 3:
        return False

    # if the total number of digits in "year" is not 4 or they are not digits, the format is not valid
    if len(checklist[0]) != 4 or not checklist[0].isdigit():
        return False

    # if the total number of digits in "month" is not 2 or they are not digits, the format is not valid
    if len(checklist[1]) != 2 or not checklist[1].isdigit():
        return False

    # if the total number of digits in "day" is not 2 or they are not digits, the format is not valid
    if len(checklist[2]) != 2 or not checklist[2].isdigit():
        return False

    # passed all checks, the format is valid
    return True

def check_required_fields(single_entry):
    
    # check if there is one field missing
    for item in REQUIRED_FIELDS:
        if item not in single_entry:
            return False
    return True


def known_location(location):

    # check if the code is in the country list
    code = location["country"].upper()
    if code in COUNTRIES or code == "KAN":
        return True
    return False


def check_quarantine(location):

    # check if it needs medical advisory
    code = location["country"].upper()
    if code in COUNTRIES:
        if COUNTRIES[code]['medical_advisory'] != '':
            return True
    return False


def check_home(location):

    # check if the home is KAN
    code = location["country"].upper()
    return code == "KAN"


def check_visa_requirement(from_location, reason):

    # check if it needs visa
    code = from_location["country"].upper()
    if code in COUNTRIES:
        if COUNTRIES[code]['visitor_visa_required'] == '1' and reason == "visit":
            return True
    return False


def conflict_decision_resolver(list_of_decisions):

    # make decision if has conflict
    if "Quarantine" in list_of_decisions:
        return "Quarantine"
    elif "Reject" in list_of_decisions:
        return "Reject"
    else:
        return "Accept"


