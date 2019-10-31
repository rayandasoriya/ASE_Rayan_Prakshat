import csv
from hw6 import *
from div import *
from decisionTree import decisionTree


def main():
    tbl = Tbl("diabetes.csv")
    rows = []
    for lst in tbl.fromString(False, "file"):
        rows.append(lst)
    c = Col()

    tbl.cols = c.colInNum(tbl.rows)
    # div2 = Div2(tbl.cols, "first", "last", "Num")
    # div2.xSplit()

    tbl.showt(tbl.decisionTree())



if __name__ == '__main__':
    main()
