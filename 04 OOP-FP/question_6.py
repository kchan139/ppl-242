"""
Use high-order function approach to write function lstSquare(n:Int) 
to return a list of i square for i from 1 to n?
"""

def lstSquare(n):
    return list(map(lambda x: x**2, range(1, n+1)))