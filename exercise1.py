#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = 'Yue Yang & Yuchen Jia'
__email__ = "yueyue.yang@mail.utoronto.ca"
__copyright__ = "2015 Yue Yang & Yuchen Jia"
__license__ = "MIT License"


#####################
# HELPER FUNCTIONS ##
#####################

def remove_duplicates(l):
    """
    Removes duplicates from l, where l is a List of Lists.
    :param l: a List
    """
    # create empty dictionary to store data
    data = {}
    # create a empty list to store keys
    result = []
    # use for loop to store data and remove duplicates
    for i in l:
        if tuple(i) not in data:
            result.append(i)
            data[tuple(i)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass

# create an exception list
EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]


def selection(t, f):
    """
    Perform select operation on table t that satisfy condition f.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """
    # create a header
    result = []
    result.append(t[0])
    # append employee information
    for i in t[1:]:
        if f(i):
            result.append(i)
    if len(result) <= 1:
        return None
    else:
        return remove_duplicates(result)


def projection(t, r):
    """
    Perform projection operation on table t
    using the attributes subset r.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """
    # create empty list to store data
    result = []
    index = []
    # test if there is an unknown attribute, then append attributes
    for attribute in r:
        if attribute not in t[0]:
            raise UnknownAttributeException("Unknown Attribute")
        else:
            index.append(t[0].index(attribute))
    # project employee information
    for row in t:
        temp = []
        for i in index:
            temp.append(row[i])
        result.append(temp)
    return result

#print projection(EMPLOYEES, ["Surname", "FirstName"])


def cross_product(t1, t2):
    """
    Return the cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]


    """
    # cross head
    result = []
    result.append(t1[0] + t2[0])
    # cross product employee information
    for i in t1[1:]:
        for j in t2[1:]:
            result.append(i+ j)
    # if there is no result, return none; otherwise return the result
    if len(result) <= 1:
        return None
    else:
        return result

