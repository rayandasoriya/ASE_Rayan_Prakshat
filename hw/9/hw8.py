from sys import path
import random, os, math

path.append(os.path.abspath("../2"))

from hw_2 import *
from the import *
from div2 import *
from hw6 import *

r = random.randint
seed = random.seed

class hw8:
    def __init__(i, file_name):
        seed(1)
        i.file_c = cells(cols(rows(file(file_name))))
        i.t = Tbl()
        i.content()
        i.random_rows = i.random_rows()
        i.goals = i.get_goals()
        
    def printVal(i):
        v = i.row_sort()
        c = [x.column_name for x in i.t.cols]
        print ("\t" , end = "\t")
        for x in c:
            print (x, end= "\t")
        print()
        
        for x in v[-4:]:
            print("best", end = "\t")
            for val in x[1].cells:
                print(val, end = "\t")
            print()
        print()

        for x in v[:4]:
            print("worst", end = "\t")
            for val in x[1].cells:
                print (val, end = "\t")
            print()
        print()

    def row_sort(i):
        val = []
        for irw in i.random_rows:
            cnt = 0
            for jrw in i.random_rows:
                if irw.dominates(jrw, i.goals) < 0:
                    cnt += 1
            val.append((cnt, irw))
        val.sort(key = lambda x: x[0])
        return val

    def content(i):
        header = False
        for r in i.file_c:
            if not header:
                i.t.addCol(r)
                header = True
            else:
                i.t.addRow(r)
    
    def random_rows(i):
        return [i.t.rows[r(0, len(i.t.rows)-1)] for _ in range(100)]
    
    def get_goals(i):
        return [i.t.cols[each] for each in i.t.col_info['goals']]
    
    def call_me(i):
        i.printVal()

hw = hw8('auto.csv') 
hw.call_me()