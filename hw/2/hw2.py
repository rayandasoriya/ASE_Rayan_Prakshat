import re
import zipfile
from hw1 import Col, Num

class Tbl:
    def __init__(self, fname):
        self.fname = fname
        self.rows = []
        self.cols = []
    
    def dump(self, c):
        print("t.cols")
        
        for i in range(len(c.n)):
            print('|',i+1)
            print('| | add: Num1')
            print('| | col: ', i+1)
            print('| | hi: ', c.maxV[i])
            print('| | lo: ', c.minV[i])
            print('| | m2: ', c.m2[i])
            print('| | mu: ', c.mean[i])
            print('| | n: ', c.n[i])
            print('| | sd: ', c.sd[i])
            print('| | txt: ', self.rows[0][i])
            
        print("t.rows")
        for idx, rows in enumerate(self.rows):
            if idx>0:
                print('|',idx+1)
                print('| | cells')
                for i, row in enumerate(rows):
                    print('| | | ',i+1,': ',row)



class Row(Tbl):
    def __init__(self, file):
        Tbl.__init__(self, file)
    
    def compiler(self, x):
        try: int(x); return  int 
        except:
            try: float(x); return  float
            except ValueError: return str

    def string(self, s):
        for line in s.splitlines(): 
            yield line

    def file(self, fname):
        with open(fname) as fs:
            for line in fs: 
                yield line

    def zipped(self, archive,fname):
        with zipfile.ZipFile(archive) as z:
            with z.open(fname) as f:
                for line in f: yield line

    def row(self, src, 
            sep=     ",",
            doomed = r'([\n\t\r ]|#.*)'):
        for line in src:
            line = line.strip()
            line = re.sub(doomed, '', line)
            if line:
                yield line.split(sep)
            else:
                yield line

    question_check = []
    def cells(self, src):
        oks = None
        prev = 0
        for n,cells in enumerate(src):    
            if not cells:
                continue
            if not prev:
                prev = len(cells)
            if prev!= len(cells):
                print("E> Skipping line ", n+1)
                continue
            if n==0:
                for cell in range(len(cells)):
                    if '?' in cells[cell]:
                        self.question_check.append(cell)
                new_arr = []
                for i in range(len(cells)):
                    if i not in self.question_check:
                        new_arr.append(cells[i])
                yield new_arr
            else:
                new_arr = []
                for cell in range(len(cells)):
                    if '?' in cells[cell]:
                        cells[cell] = 0
                for i in range(len(cells)):
                    if i not in self.question_check:
                        new_arr.append(cells[i])  
                oks = oks or [self.compiler(cell) for cell in new_arr]
                yield [f(cell) for f,cell in zip(oks,new_arr)]

    def fromString(self):
        for lst in self.cells(self.row(self.string(self.fname))):
            self.rows.append(lst)
            yield lst


if __name__=="__main__":
    s="""$cloudCover, $temp, ?$humid, <wind,  $playHours
    100,        68,    80,    0,    3   # comments
    0,          85,    85,    0,    0

    0,          80,    90,    10,   0
    60,         83,    86,    0,    4
    100,        70,    96,    0,    3
    100,        65,    70,    20,   0
    70,         64,    65,    15,   5
    0,          72,    95,    0,    0
    0,          69,    70,    0,    4
    ?,          75,    80,    0,    ?
    0,          75,    70,    18,   4
    60,         72,
    40,         81,    75,    0,    2
    100,        71,    91,    15,   0
    """
    t = Row(s)
    for lst in t.fromString():
        print(lst)
    c = Col()
    t.cols = c.colInNum(t.rows)
    print(t.cols)
    num = Num()

    for column in t.cols:
        response = num.num1(column)
        c.mean.append(response[0])
        c.sd.append(response[1])
        c.m2.append(response[2])
        c.n.append(response[3])
        c.maxV.append(response[4])
        c.minV.append(response[5])
    t.dump(c)
    # print("\nMean")
    # print(c.mean)
    # print("\nsd")
    # print(c.sd)
    # print("\nM2")
    # print(c.m2)
    # print("\nN")
    # print(c.n)
    # print("\nMax")
    # print(c.maxV)
    # print("\nMin")
    # print(c.minV)