from sys import path
import os, math, random
path.append(os.path.abspath("..") + "/2")
from hw_2 import *
from the import *
r= random.random
seed=random.seed

class Div2:
    def __init__(i,num_list, column_x, column_y, column_types, column_name_fn, key_fn = same):
        i.column_types = column_types
        i.column_name_fn = column_name_fn
        i.key_fn = key_fn    
        i.num_list = ordered(num_list, key = column_name_fn, index = column_x)
        i.b4 = [class_type(column_name_fn(idx),idx) for idx,class_type in enumerate(i.column_types)]
        for row in i.num_list:
            for idx, val in enumerate(row):
                i.b4[idx].add_new_value(val)
        i.x = column_x
        i.y = column_y
        i.step = int(len(i.num_list))**DIVISION_UTILS.mini
        i.gain = 0
        i.start = first(i.b4[i.y].all_values)
        i.stop = last(i.b4[i.y].all_values)
        i.ranges = []
        i.epsilon = i.b4[i.y].variety()
        i.epsilon *= DIVISION_UTILS.coh
        low = 1
        high = i.b4[i.y].n
        i.rank, i.cut, i.best = i.__split(1,low,high,i.b4)
        i.gain /= i.b4[i.y].n
    
    def __split(i,rank,low,high,b4):
        left = dict()
        right = dict()
        best = b4[i.y].variety()
        cut = None
        left[i.x] = i.column_types[i.x]()
        left[i.y] = i.column_types[i.y]()
        right[i.x] = i.column_types[i.x]()
        right[i.y] = i.column_types[i.y]()
        for each in range(low,high):
            right[i.x].add_new_value(i.b4[i.x].all_values[each])
            right[i.y].add_new_value(i.b4[i.y].all_values[each])
        
        for j in range(low, high):
            left[i.x].add_new_value(i.b4[i.x].all_values[j])
            left[i.y].add_new_value(i.b4[i.y].all_values[j])
            right[i.x].delete_value(i.b4[i.x].all_values[j])
            right[i.y].delete_value(i.b4[i.y].all_values[j])

            if left[i.y].n >= i.step:
                if right[i.y].n >= i.step:
                    now = i.key_fn(i.b4[i.y].all_values[j-1])
                    after = i.key_fn(i.b4[i.y].all_values[j])
                    if now == after: continue
                    xpect = None
                    if isinstance(i.b4[i.y],Sym):
                        if abs(ord(right[i.y].mode)-ord(left[i.y].mode)) >= i.epsilon:
                            if ord(after) - ord(i.start) >= i.epsilon:
                                if ord(i.stop) - ord(now) >= i.epsilon:
                                    xpect = left[i.y].xpect(right[i.y])
                    else:
                        if abs(right[i.y].mu-left[i.y].mu) >= i.epsilon:
                            if after - i.start >= i.epsilon:
                                if i.stop - now >= i.epsilon:
                                    xpect = left[i.y].xpect(right[i.y])
                    if xpect:
                        if xpect*DIVISION_UTILS.tri < best:
                            best,cut = xpect, j
        
        if cut:
            low_b4 = [class_type(i.column_name_fn(idx),idx) for idx,class_type in enumerate(i.column_types)]
            high_b4 = [class_type(i.column_name_fn(idx),idx) for idx,class_type in enumerate(i.column_types)]
            for each in range(len(low_b4)):
                for x in range(low,cut):
                    low_b4[each].add_new_value(i.b4[each].all_values[x])

            for each in range(len(high_b4)):
                for x in range(cut,high):
                    high_b4[each].add_new_value(i.b4[each].all_values[x])
            rank, c, b = i.__split(rank,low,cut,low_b4)
            rank += 1
            rank,_,_ = i.__split(rank,cut,high,high_b4)
        else:
            i.gain += b4[i.y].n*b4[i.y].variety()
            b4[i.x].rank = rank
            b4[i.y].rank = rank
            i.ranges.append(b4)
        return rank, cut, best

def num(i):
    if i<0.4: return [i,     r()*0.1]
    if i<0.6: return [i, 0.4+r()*0.1]
    return [i, 0.8+r()*0.1]

def xnum():
    return  [num(one) for one in x()]

def column_name_fn(x):
    return ""

def roundoff(x):
    return round(x,5)

def xsym():
    return  [sym(one) for one in x()] * 5

def sym(i):
    if i<0.4: return [i, "a"]
    if i<0.6: return [i, "b"]
    return [i, "c"]