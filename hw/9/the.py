from sys import path
import os
from math import log
path.append(os.path.abspath("..") + "/2")
from hw_2 import Num,SYMBOLS

def last(arr):
    "Returns last element from given list"
    return arr[-1]

def first(arr):
    "Returns first element from given list"
    return arr[0]

def same(num):
    "Right now returns same number"
    return num

def ordered(num_list, key, index):
    "Sort elements in array at the same time ignore 'Skip' characters"
    return sorted(num_list, key = lambda x: x[index])
    
class DIVISION_UTILS:
    trivial = 1.025
    cohen = 0.3
    minimum = 0.5
    minObs = 4
    alpha = [0.5, 0.6, 0.7, 0.8, 0.9]