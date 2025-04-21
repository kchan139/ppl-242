# import math

# def gcd(a, b):
#     return math.gcd(a,b)

def gcd(a, b):
    if a < b:
        a, b = b, a # swap
        
    while b != 0:
        a, b = b, a % b
        
    return a