from sys import path
import json, jsonpickle, random, re, os, math
path.append(os.path.abspath("..") + "/2")
from hw_2 import Row, Col, Num, Sym, cells, cols, rows, file, fromString
from the import same, first, last, ordered, DIVISION_UTILS
from div2 import Div2, column_name_fn
r= random.random
seed=random.seed

def tree_result(low, high, n, text, kids):
    return {"low" : low,"high" : high,"n" : n,"text" : text,"kids": kids}

def leaf_result(classval, rows):
    if classval == 'p':
        classval = 'tested_positive'
    if classval == 'n':
        classval = 'tested_negative'
    return {'val' : classval,'n' : rows}

class Tbl:
    def __init__(i):
        i.rows = list() 
        i.cols = list() 
        i.col_info = {'goals': [], 'nums': [], 'syms': [], 'xs' : [], 'negative_weight' : []}
        i.tree_result = None

    def dump(i):
        print(json.dumps(json.loads(jsonpickle.encode(i)), indent=4, sort_keys=True))

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
    
    def addRow(self, row):
        for i in range(len(self.cols)):
            self.cols[i].add_new_value(row[i])
        self.rows.append(Row(row))

    def tree(i):
        class_index = i.col_info["goals"][0]
        class_type = Sym if class_index in i.col_info["syms"] else Num
        func1 = lambda row: row.cells
        data = list(map(func1, i.rows))
        i.tree_result = i.get_tree(data, class_index,class_type, 0)
    
    def get_tree(i, data_rows, class_index, class_type, level):
        if len(data_rows) >= DIVISION_UTILS.minO:
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
                func = lambda row: row.cells
                return [tree_result(low, high, len(kids), column.column_name, i.get_tree(kids, class_index, class_type, level + 1)) for low,high, kids in i.split(data_rows, cut, column)]                        
        return leaf_result(data_rows[len(data_rows)//2][class_index], len(data_rows))

    def split(i, data_rows, cut, column):
        left_half,low = data_rows[:cut],data_rows[cut][column.position]
        right_half,high = data_rows[cut:], data_rows[cut+1][column.position]
        return [(-float('inf'), low, left_half),(high, float('inf'), right_half)]
