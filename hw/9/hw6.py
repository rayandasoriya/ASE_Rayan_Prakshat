from sys import path
from math import log
import json, jsonpickle, random, re, os
path.append(os.path.abspath("..") + "/2")
path.append(os.path.abspath("..") + "/5")
from hw_2 import *
path.append(os.path.abspath("..") + "/3")
from hw_3 import *
from the import *
from div2 import *
import time
r= random.random
seed=random.seed


def treeR(low, high, n, text, kids):
    return {"low" : low,"high" : high,"n" : n,"text" : text,"kids": kids}

def leaf_result(classval, rows):
    if classval == 'p':
        classval = 'tested_positive'
    if classval == 'n':
        classval = 'tested_negative'
    return {'val' : classval,'n' : rows}

class Tbl2:
    def __init__(i):
        i.rows, i.cols = [], []
        i.col_info = {'goals': [], 'nums': [], 'syms': [], 'xs' : [], 'negative_weight' : []}
        i.treeR = None

    def same(i,al,length,fname):
        a = RPTree2()
        if (length % 2):
            med = al*len(i.rows)/2
        else:
            med = (al*len(i.rows)+1)/2        
        if 'pom' not in fname:
            print('Alpha: ', al, ', Baseline: ', a.bs1[length], ', Increment: ', a. inc1[a.bs1[length]])
        else:
            print('Alpha: ', al, ', Baseline: ', a.bs2[length], ', Increment: ', a. inc2[a.bs2[length]])

    def addCol(i, column):
        for idx,col_name in enumerate(column):
            if bool(re.search(r"[<>$]",col_name)):
                i.col_info['nums'].append(idx)
                if bool(re.search(r"[<]", col_name)):
                    i.col_info['negative_weight'].append(idx)
                    i.cols.append(Num(col_name,idx,-1))
                else:
                    i.cols.append(Num(col_name,idx))
            else:
                i.col_info['syms'].append(idx)
                i.cols.append(Sym(col_name,idx))
            if bool(re.search(r"[<>!]",col_name)):
                i.col_info['goals'].append(idx)
            else:
                i.col_info['xs'].append(idx)

    def tbl_header(i):
        return [col.column_name for col in i.cols]

    def read(i, s, type = "string"):
        content = None
        if type == "file":
            content = cells(cols(rows(file(s))))
        else:
            content = cells(cols(rows(fromString(s))))
        for idx, row in enumerate(content):
            if idx == 0:
                i.cols = []
                i.addCol(row)
            else:
                i.addRow(row)
        
    def addRow(i, row):
        for j in range(len(i.cols)):
            i.cols[j].add_new_value(row[j])
        i.rows.append(Row(row))
    
    def tree(i):
        class_index = i.col_info["goals"][0]
        class_type = Sym if class_index in i.col_info["syms"] else Num
        func1 = lambda row: row.cells
        data = list(map(func1, i.rows))
        i.treeR = i.get_tree(data, class_index,class_type, 0)
    
    def get_tree(i, data_rows, class_index, class_type, level):
        if len(data_rows) >= DIVISION_UTILS.minObs:            
            low, cut, column = 10**32, None, None
            column_types = []
            for col in i.cols:
                if isinstance(col,Num):
                    column_types.append(Num)
                else:
                    column_types.append(Sym)
            for col in i.cols:
                if col.position == class_index:
                    continue
                x = Div2(data_rows, col.position, class_index, column_types, column_name_fn)
                cut1, low1 = x.cut, x.best
                if cut1 and low1:
                    if low1 < low:
                        cut, low, column = cut1, low1, col
            if cut:
                return [treeR(low, high, len(kids), column.column_name, i.get_tree(kids, class_index, class_type, level + 1)) for low,high, kids in i.split(data_rows, cut, column)]                        
        return leaf_result(data_rows[len(data_rows)//2][class_index], len(data_rows))

    def split(i, data_rows, cut, column):
        left_half,low = data_rows[:cut],data_rows[cut][column.position]
        right_half,high = data_rows[cut:], data_rows[cut+1][column.position]
        return [(-float('inf'), low, left_half),(high, float('inf'), right_half)]
            
def hw6Print(tree, level = 0):
    if isinstance(tree, list):
        for each in tree:
            hw6Print(each, level)
    else:
        for _ in range(level):
            print ("|", end = " ")
        print ("{0}={1}.....{2}".format(tree['text'], tree['low'], tree['high']), end = " ")        
        if not isinstance(tree['kids'], list):
            print ("{0} ({1})".format(tree['kids']['val'],tree['kids']['n']))
        else:
            for each in tree['kids']:
                print()
                hw6Print(each, level + 1)