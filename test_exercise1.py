#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"

from exercise1 import selection, projection, cross_product


###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]

STUDENTS = [["FirstName", "Surname", "Age"],
            ["Yueyue", "Yang", 25],
            ["Yuchen", "Jia", 23],
            ["Xike", "Wang", 25],
            ["Ming", "Fu", 31],
            ["Black", "Whiten", 66]]

TEACHER = [["FirstName", "Surname", "Age"],
           ["Susan", "Sim", 40],
           ["Eric", "Yu", 60]]

COURSES = [["Course"],
           ["Inf1340"],
           ["Inf1341"]]

#####################
# HELPER FUNCTIONS ##
#####################
def is_equal(t1, t2):

    t1.sort()
    t2.sort()

    return t1 == t2


#####################
# FILTER FUNCTIONS ##
#####################
def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 30 and row[-1] > 3500


def filter_students(row):
    return row[-1] <= 35

###################
# TEST FUNCTIONS ##
###################


def test_selection():
    """
    Test select operation.
    """

    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]

    assert is_equal(result, selection(EMPLOYEES, filter_employees))


def test_projection():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]

    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))


def test_cross_product():
    """
    Test cross product operation.
    """

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mori"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mori"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mori"],
              ["White", "production", "sales", "Brown"]]

    assert is_equal(result, cross_product(R1, R2))


def test_selection_student():
    # Test selection
    result = [["FirstName", "Surname", "Age"],
              ["Yueyue", "Yang", 25],
              ["Yuchen", "Jia", 23],
              ["Xike", "Wang", 25],
              ["Ming", "Fu", 31]]

    assert is_equal(result, selection(STUDENTS, filter_students))


def test_projection_student():
    # Test projection
    result = [["Surname", "Age"],
              ["Yang", 25],
              ["Jia", 23],
              ["Wang", 25],
              ["Fu", 31],
              ["Whiten", 66]]

    assert is_equal(result, projection(STUDENTS, ["Surname", "Age"]))


def test_cross_product_student():
    # Test cross product
    result = [["FirstName", "Surname", "Age", "Course"],
              ["Susan", "Sim", 40, "Inf1340"],
              ["Susan", "Sim", 40, "Inf1341"],
              ["Eric", "Yu", 60, "Inf1340"],
              ["Eric", "Yu", 60, "Inf1341"]]

    assert is_equal(result, cross_product(TEACHER, COURSES))


def test_selection_returns_nothing():
    # Test if selection is none
    t = [["Name", "Age"],
         ["Bob", 47],
         ["Mary", 65],
         ["Carla", 54]]

    def f(r):
        return r[-1] < 35

    assert selection(t, f) is None


def test_projection_returns_error():
    # Test if projection has error
    try:
        projection(STUDENTS, ["Age", "Surname"])
    except AttributeError:
        assert True


def test_cross_product_returns_nothing():
    # Test if cross product is none
    t1 = [["Teacher", "Age"],
         ["Susan", 47],
         ["Eric", 65]]
    t2 = [["Teacher", "Age"]]

    assert cross_product(t1, t2) is None



