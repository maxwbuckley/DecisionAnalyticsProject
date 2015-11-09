"""scoring functions for populating MCDA matrices"""
import math

def Linear(value, offset=3):
  return value + offset

def LinearPositiveOnly(value):
  if value >=0:
    return value
  else:
    return 0

def Quadratic(value, offset=2):
  return value**offset

def QuadraticBonus(value, offset=2):
  return max(value, 0)**2 + 3 + min(value, 0)

def ExponentialBonus(value):
  return math.exp(max(value, 0)) + 3 + min(value, 0)

def Reciprocal(value):
  if value >=0:
    return value
  else:
    return 1.0/abs(value)


