import csv
from hw6 import *
from div import *
from decisionTree import decisionTree


def main():
    tbl = Tbl("xomo10000.csv")
    rows = []
    for lst in tbl.fromString(False, "file"):
        if lst[-1] == 'tested_negative':
            lst[-1] = 'b'
        else:
            lst[-1] = 'a'
        rows.append(lst)
    c = Col()
    tbl.cols = c.colInNum(tbl.rows)
    tbl.decisionTree()


if __name__ == '__main__':
    main()
