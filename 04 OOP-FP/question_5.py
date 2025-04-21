"""
Let lst be a list of a list of element, use list comprehension approach
to write function flatten(lst) that returns the list of all elements
"""

def flatten(lst):
    return [element for sublist in lst for element in sublist]