from sys import path
import json, jsonpickle, random, re, os, math, collections
path.append(os.path.abspath("..") + "/2")
path.append(os.path.abspath("..") + "/3")
from hw_2 import *
from hw_3 import *
from the import *
from div2 import *
from hw6 import *
from hw7 import *
from utils import *
r= random.randint
seed=random.seed

class Hw9:
    def __init__(i, file_name):
        seed(1)
        i.file_c = cells(cols(rows(file(file_name))))
        i.t = Tbl()
        i.content()
        i.random_rows = i.random_rows()
        i.goals = i.get_goals()
        i.x = 0
        
    def printVal(i,fname):
        a = Tbl2()
        v = i.row_sort()
        c = [x.column_name for x in i.t.cols]
        print("For file: ", fname)
        for al in DIVISION_UTILS.alpha:
            a.same(al,i.x,fname)
            i.x+=1

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
    
    def call_me(i, fname):
        i.printVal(fname)

def dist(col1, col2, goals):
    d, n, p = 0, 0, 2
    for i, c in enumerate(goals):
        n += 1
        d0 = None
        if isinstance(c, Num):
            d0 = c.dist(col1.leaves[i].mu, col2.leaves[i].mu)
        else:
            d0 = c.dist(col1.leaves[i].mode, col2.leaves[i].mode)
        d += d0**p
    return d**(1/p) / n**(1/p)

def dominate(c1, c2, goals):
    z = 0.00001
    s1, s2, n = z,z,z+len(goals)
    for i, g in enumerate(goals):
        if isinstance(g, Num):
            a,b = c1.leaves[i].mu, c2.leaves[i].mu
            a,b = g.norm(a), g.norm(b)
            s1 -= 10**(g.weight * (a-b)/n)
            s2 -= 10**(g.weight * (b-a)/n)
    return (s1/n - s2/n)

def envy():
    a = hw7('xomo10000.csv')
    c = a.leaf_nodes
    ENMap, envyNodes = defaultdict(list), list()
    g = [a.tbl.cols[each] for each in a.tbl.col_info['goals']]
    for c1 in c:
        for c2 in c:
            if dominate(c1, c2, g) > 0:
                ENMap[c1].append(c2)
    for c1 in ENMap:
        mdist = float('inf')
        mEnvy = None
        for c2 in ENMap[c1]:
            d = dist(c1,c2,g)
            if d < mdist:
                mdist = d
                mEnvy = c2 
        envyNodes.append((c1, mEnvy))
    for val in envyNodes:
        tbl = Tbl()
        cols = [col.column_name for col in val[0].tbl.cols]
        cols.append('!$nwcls')
        tbl.addCol(cols)
        for e in val[0].tbl.rows:
            c = e.cells
            c.append(0)
            tbl.addRow(c)        
        for e in val[1].tbl.rows:
            c = e.cells
            c.append(1)
            tbl.addRow(c)
        tbl.tree()

hw = Hw9('xomo10000.csv') 
hw.call_me('xomo10000.csv')
hw = Hw9('pom310000.csv') 
hw.call_me('pom310000.csv')