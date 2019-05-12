#!/usr/bin/python

import types

something = input ("Please type something ")

if type(something) is types.IntType:
   print "The input was an integer"
elif type(something) is types.FloatType:
   print "The input was a real number"
elif type(something) is types.StringType:
   print "The input was a string"

