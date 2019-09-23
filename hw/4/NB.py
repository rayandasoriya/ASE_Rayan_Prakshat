import re
import zipfile
import random
import math
from abcd import Abcd
import collections


class Tbl:
    def __init__(self, fname):
        self.fname = fname
        self.rows = []
        self.cols = []
        self.oid = 1
        self.goals = []
        self.xs = []
        self.syms = []
        self.nums = []
        self.question = []
        self.w = {}
        self.indexKeeper = {}

    def dump(self, c):
        columns = self.cols
        print("t.cols")
        symVar = 0
        numVar = 0
        for i, col in enumerate(columns):
            self.oid += 1
            if str(col[0]).isnumeric():
                print('|', self.indexKeeper.get(i))
                print('| | add: Num1')
                print('| | col:', self.indexKeeper.get(i))
                print('| | hi:', c.maxV[numVar])
                print('| | lo:', c.minV[numVar])
                print('| | m2:', c.m2[numVar])
                print('| | mu:', c.mean[numVar])
                print('| | n:', c.n[numVar])
                print('| | oid:', self.oid)
                print('| | sd:', c.sd[numVar])
                print('| | txt:', self.rows[0][i])
                numVar += 1
            else:
                print('|', self.indexKeeper.get(i))
                print('| | add: Sym1')
                print('| | cnt')
                for key, value in c.dictValues[symVar].items():
                    print('| | | ', key, ': ', value)
                print('| | col:', self.indexKeeper.get(i))
                print('| | mode:', c.mode[symVar])
                print('| | most:', c.most[symVar])
                print('| | n:', c.n[symVar])
                print('| | oid:', self.oid)
                print('| | txt:', self.rows[0][i])
                symVar += 1

        xnums = list(set(self.nums).intersection(set(self.xs)))
        xsyms = list(set(self.syms).intersection(set(self.xs)))
        print("t.my")
        print("| class: ", len(self.question) + len(self.syms) + len(self.nums))
        print("| goals ")
        for i in self.goals:
            print("| | ", i)
        print("| nums ")
        for i in self.nums:
            print("| | ", i)
        print("| syms ")
        for i in self.syms:
            print("| | ", i)
        print("| w ")
        for key, value in self.w.items():
            print("| | ", key, ": ", value)
        print("| xs ")
        for i in self.xs:
            print("| | ", i)
        print("| xnums ")
        for i in xnums:
            print("| | ", i)
        print("| xsyms ")
        for i in xsyms:
            print("| | ", i)


class Row(Tbl):
    def __init__(self, file):
        Tbl.__init__(self, file)

    def compiler(self, x):
        try:
            int(x)
            return int
        except:
            try:
                float(x)
                return float
            except ValueError:
                return str

    def string(self, s):
        for line in s.splitlines():
            yield line

    def file(self, fname):
        with open(fname) as fs:
            for line in fs:
                yield line

    def zipped(self, archive, fname):
        with zipfile.ZipFile(archive) as z:
            with z.open(fname) as f:
                for line in f: yield line

    def row(self, src,
            sep=",",
            doomed=r'([\n\t\r ]|#.*)'):
        for line in src:
            line = line.strip()
            line = re.sub(doomed, '', line)
            if line:
                yield line.split(sep)
            else:
                yield line

    def cells(self, src):
        oks = None
        prev = 0
        for n, cells in enumerate(src):
            if not cells:
                continue
            if not prev:
                prev = len(cells)
            if prev != len(cells):
                print("E> Skipping line ", n + 1)
                continue
            if n == 0:
                self.identifyColType(cells)
                new_arr = []
                keep = 0
                for i in range(len(cells)):
                    if i not in self.question:
                        new_arr.append(cells[i])
                        self.indexKeeper.update({keep: i + 1})
                        keep += 1
                yield new_arr
            else:
                new_arr = []
                for cell in range(len(cells)):
                    if '?' in cells[cell]:
                        cells[cell] = 0
                for i in range(len(cells)):
                    if i not in self.question:
                        new_arr.append(cells[i])
                oks = [self.compiler(cell) for cell in new_arr]
                yield [f(cell) for f, cell in zip(oks, new_arr)]

    def identifyColType(self, cells):
        SKIPCOL = "\\?"
        NUMCOL = "[<>\\$]"
        GOALCOL = "[<>!]"

        for idx, col in enumerate(cells):
            if re.findall(SKIPCOL, col):
                self.question.append(idx)
                continue
            if re.findall(NUMCOL, col):
                self.nums.append(idx + 1)
            else:
                self.syms.append(idx + 1)
            if re.findall(GOALCOL, col):
                self.goals.append(idx + 1)
            else:
                self.xs.append(idx + 1)

        for idx, col in enumerate(cells):
            if '<' in col:
                self.w[idx + 1] = -1
            elif '>' in col:
                self.w[idx + 1] = 1

    def fromString(self, part, type):
        if not part:
            if type == 'file':
                for lst in self.cells(self.row(self.file(self.fname))):
                    self.rows.append(lst)
                    yield lst
            else:
                for lst in self.cells(self.row(self.string(self.fname))):
                    self.rows.append(lst)
                    yield lst


class Col(Tbl):

    def __init__(self):
        # Change in array
        self.n = []
        self.mean = []
        self.sd = []
        self.m2 = []
        self.maxV = []
        self.minV = []
        self.mode = []
        self.entropy = []
        self.most = []
        self.indexKeeper = {}
        self.dictValues = []

    def colInNum(self, rows):
        numCols = len(rows[0])
        cols = [[-1 for _ in range(len(rows))] for _ in range(len(rows[0]))]
        for i in range(1, len(rows)):
            for j in range(numCols):
                cols[j][i] = rows[i][j]
        ans = []
        for col in cols:
            ans.append(col[1:])
        return ans


class Num(Col):
    def __init__(self):
        Col.__init__(self)
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.maxV = -1 * 10 ** 32
        self.minV = 1 * 10 ** 32

    # Function to calculate the SD using variance
    def _numSd(self, count):
        if count == 1:
            self.sd = 0
        else:
            self.sd = (self.m2 / (count - 1)) ** 0.5

    # Method to incrementally update mean and standard deviation
    def num1(self, array):
        count = 0
        for i in range(len(array)):
            if array[i] > self.maxV:
                self.maxV = array[i]
            if array[i] < self.minV:
                self.minV = array[i]
            count += 1
            delta = array[i] - self.mu
            self.mu += (delta / count)
            delta2 = array[i] - self.mu
            # Calculation of square mean distance
            self.m2 += delta * delta2
            self._numSd(count)
        return round(self.mu, 2), round(self.sd, 2), round(self.m2, 2), count, self.maxV, self.minV

    # Method to remove the element and update mean and standard deviation
    def numLess(self, array):
        subtract_mean = []
        subtract_sd = []
        count = len(array) - 1
        for _ in range(len(array) - 1, 0, -1):
            if count % 10 == 0:
                subtract_mean.append(round(self.mu, 2))
                subtract_sd.append(round(self.sd, 2))
            count -= 1
            deleteValue = array.pop()
            delta = deleteValue - self.mu
            self.mu -= delta / count
            self.m2 -= delta * (deleteValue - self.mu)
            self._numSd(count)
        return subtract_mean, subtract_sd


class Sym(Col):
    def __init__(self):
        self.mode = ""
        self.most = 0
        self.cnt = {}
        self.entropy = 0

    def Sym1(self, column):
        self.__init__()
        for element in column:
            if element in self.cnt:
                self.cnt.update({element: self.cnt.get(element) + 1})
            else:
                self.cnt.update({element: 1})
            tmp = self.cnt.get(element)
            if tmp > self.most:
                self.most = tmp
                self.mode = element
        self.entropy = self.calculateEntropy(column, len(column))
        return self.entropy

    def calculateEntropy(self, column, n):
        entropy = 0
        for element in self.cnt:
            p = self.cnt[element] / n
            entropy -= p * (math.log(p) / math.log(2))
        return entropy


class NB(object):
    def __init__(self):
        self.minimumData = 2
        self.entries = 0
        self.gols = []
        self.symo = Sym()
        self.abo = Abcd()
        self.fullTable = []
        self.tablelist = collections.defaultdict(list)

    def train(self, t, rows):
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            if idx > 2:
                expected = row[len(row) - 1]
                self.symo.Sym1(self.gols)
                result = self.classify()
                self.abo.abcd1(expected, result)
            self.gols.append(t[-1][idx - 1])

    def classify(self):
        return self.symo.mode

    def dump(self):
        self.abo.report()

    def createClasses(self, rows, columns):
        # totaltables = len(set(columns[len(columns)-1]))

        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            else:
                self.tablelist[row[-1]].append(row)



if __name__ == "__main__":
    print("#---zerorok-----------------------")
    t = Row("weathernon.csv")
    rows = []
    for lst in t.fromString(False, "file"):
        rows.append(lst)

    # for idx, row in rows:

    c = Col()
    allrows = t.rows
    allcolumns = c.colInNum(t.rows)
    # zeror = ZeroR()
    # zeror.train(t, rows)
    # print("\nweathernon")
    # zeror.dump()
    #
    # t = Row("diabetes.csv")
    # rows = []
    # for lst in t.fromString(False, "file"):
    #     rows.append(lst)
    #
    # c = Col()
    # t = c.colInNum(t.rows)
    #
    # zeror = ZeroR()
    # zeror.train(t, rows)
    # print("\ndiabetes")
    # zeror.dump()

