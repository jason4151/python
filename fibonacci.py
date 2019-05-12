#!/usr/bin/python -tt

def fib(n):
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b
 
# Get input from user
number = input("Input a number for Fibonacci series: ")

# Call function using user input
fib(number)

