#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
import os
from exercise2 import decide

DIR = "test_jsons/"
os.chdir(DIR)


def test_returning():
    """
    Travellers are returning to KAN.
    """
    assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]

def test_basic():

    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]

    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]

    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_lowercase.json", "watchlist.json", "countries.json") == ["Accept"]

    assert decide("test_raises_all_flags.json", "watchlist.json", "countries.json") == ["Quarantine"]

def test_files():

    with pytest.raises(FileNotFoundError):

        decide("test_returning_citizen.json", "", "countries.json")

        decide("", "watchlist.json", "countries.json")

        decide("test_returning_citizen.json", "watchlist.json", "")

def test_empty():

    assert decide("test_empty_fname.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_empty_lname.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_emptycountry.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_nopassport.json", "watchlist.json", "countries.json") == ["Reject"]


def test_wronginput():

    assert decide("test_wrongpassport.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_wrongformat.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_nonexistent_country.json", "watchlist.json", "countries.json") == ["Reject"]


def test_wrongvisa():

    assert decide("test_wrongvisa.json", "watchlist.json", "countries.json") == ["Reject"]


def test_compromised_citizen():

    assert decide("test_returning_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_returning_watchlisted.json", "watchlist.json", "countries.json") == ["Secondary"]





