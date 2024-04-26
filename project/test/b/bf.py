import os
import sys

print(os.path.realpath(__file__))
print(os.path.dirname(os.path.realpath(__file__)))

def bf_print():
    print("I am bf file")
