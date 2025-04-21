"""
Let lst be a list of integer and n be an integer, use recursive approach to write 
function lessThan(lst,n) that returns the list of all numbers in lst less than n.
"""

def lessThan(lst, n):
    if not lst:
        return []
    else:
        if lst[0] < n:
            return [lst[0]] + lessThan(lst[1:], n)
        else:
            return lessThan(lst[1:], n)