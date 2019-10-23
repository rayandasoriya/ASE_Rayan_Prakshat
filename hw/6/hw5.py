import operator
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
        self.count = []
        self.mean = []
        self.sd = []
        self.m2 = []
        self.maxV = []
        self.minV = []
        self.mode = []
        self.sd = []
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
        self.count = 0
        self.numList = []
        self.lo = 10 ** 32
        self.hi = -1 * self.lo

    # Function to calculate the SD using variance
    def _numSd(self, count):
        if count == 1:
            self.sd = 0
        else:
            self.sd = (self.m2 / (count - 1)) ** 0.5

    def _numSd2(self):
        if self.count == 1:
            self.sd = 0
        else:
            self.sd = (self.m2 / (self.count - 1)) ** 0.5

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

    def num2(self, val):
        self.lo = self.lo if self.lo<val else val
        self.hi = self.hi if self.hi> val else val
        self.numList.append(val)
        if val > self.maxV:
            self.maxV = val
        if val < self.minV:
            self.minV = val
        self.count += 1
        delta = val - self.mu
        self.mu += (delta / self.count)
        delta2 = val - self.mu
        # Calculation of square mean distance
        self.m2 += delta * delta2
        self._numSd2()

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

    def numLess2(self, index):
        if self.count < 2:
            self.sd = 0
            return

        self.count -= 1
        value = self.numList[index]
        self.numList.pop(index)
        delta = value - self.mu
        self.mu -= delta / self.count
        self.m2 -= delta * (value - self.mu)
        if self.m2 < 0 or self.count < 2:
            self.sd = 0
        else:
            self._numSd2()

    def numLike(self, x, m, cls):
        var = self.sd ** 2
        denom = math.sqrt(math.pi * 2 * var)
        num = (2.71828 ** (-(x - self.mu) ** 2) / (2 * var + 0.0001))
        if m == cls:
            self.num2(x)
        return num / (denom + 10 ** (-64)) + 10 ** (-64)

    def xpect(self, other):
        n = self.count + other.count
        return (self.count / n * self.sd) + (other.count / n * other.sd)


class Sym(Col):
    def __init__(self):
        self.mode = ""
        self.most = 0
        self.cnt = collections.defaultdict(int)
        self.sd = 0
        self.count = 0
        self.column = []
        self.symList = []

    def Sym1(self, column):
        self.__init__()
        for element in column:
            self.count += 1
            self.cnt[element] += 1
            tmp = self.cnt[element]
            if tmp > self.most:
                self.most = tmp
                self.mode = element
        self.sd = self.calculateEntropy(len(column))
        return self.sd

    def calculateEntropy(self, n):
        entropy = 0
        for element in self.cnt:
            p = self.cnt[element] / n
            entropy -= p * (math.log(p) / math.log(2))
        return entropy

    def Sym2(self, val):
        self.symList.append(val)
        self.count += 1
        self.cnt[val] += 1
        tmp = self.cnt[val]
        if tmp > self.most:
            self.most = tmp
            self.mode = val
        self.column.append(val)
        self.sd = self.calculateEntropy2()
        return self.sd

    def xpect(self, other):
        n = self.count + other.count
        return (self.count / n * self.sd) + (other.count / n * other.sd)

    def calculateEntropy2(self):
        entropy = 0
        for element in self.cnt:
            p = self.cnt[element] / len(self.column)
            if p:
                entropy -= p * (math.log(p) / math.log(2))
        return entropy

    def symLike(self, x, prior, m, l, cls):
        f = self.cnt[x]
        if cls == l:
            self.Sym2(x)
        return (f + m * prior) / (self.count + m)

    def symLess(self, v):
        self.count -= 1
        self.cnt[v] -= 1
        if not self.cnt[v]:
            del self.cnt[v]
        if self.cnt:
            self.mode = max(self.cnt.items(), key=operator.itemgetter(1))[0]
            self.most = self.cnt[self.mode]
            self.symList.remove(v)


class ZeroR():
    def __init__(self):
        self.minimumData = 2
        self.entries = 0
        self.gols = []
        self.symo = Sym()
        self.abo = Abcd()

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


class NB:
    def __init__(self, tbl, wait):
        self.tbl = tbl
        self.wait = wait
        self.n = -1
        self.k = 1
        self.m = 2
        self.lst = []
        self.count = 0
        self.abo = Abcd()
        self.tablelist = collections.defaultdict(list)
        self.cols = collections.defaultdict(list)

    def train(self, t, lines):
        for idx, row in enumerate(lines):
            self.n += 1
            if idx == 0:
                continue
            if row[-1] not in self.cols:
                for rowIdx, _ in enumerate(row[:-1]):
                    if self.tbl.indexKeeper[rowIdx] in self.tbl.syms:
                        self.cols[row[-1]].append(Sym())
                    elif self.tbl.indexKeeper[rowIdx] in self.tbl.nums:
                        self.cols[row[-1]].append(Num())
            if idx <= self.wait:
                for c in range(len(row) - 1):
                    if self.tbl.indexKeeper[c] in self.tbl.syms:
                        self.cols[row[-1]][c].Sym2(row[c])
                    elif self.tbl.indexKeeper[c] in self.tbl.nums:
                        self.cols[row[-1]][c].num2(row[c])
            if idx > self.wait:
                expected = row[-1]
                result = self.classify(row, "")
                self.abo.abcd1(expected, result)
            self.tablelist[row[-1]].append(row)
            self.count += 1
            self.lst.append(row)

    def classify(self, line, guess):
        most = float('-inf')
        for cls, row in self.tablelist.items():
            guess = cls if not guess else guess
            like = self.bayesThm(line, row, cls)
            if like > most:
                most = like
                guess = cls
        return guess

    def bayesThm(self, line, tbl, cls):
        like = prior = ((len(tbl) + self.k) / (self.n + self.k * len(self.tablelist)))
        like = math.log(like)
        for c in range(len(line) - 1):
            if self.tbl.indexKeeper[c] in self.tbl.nums:
                like += math.log(self.cols[cls][c].numLike(line[c], line[-1], cls))
            elif self.tbl.indexKeeper[c] in self.tbl.syms:
                like += math.log(self.cols[cls][c].symLike(line[c], prior, self.m, line[-1], cls))
        return like

    def dump(self):
        self.abo.report()


if __name__ == "__main__":

    print("#---zerorok-----------------------")
    t = Row("weathernon.csv")
    rows = []
    for lst in t.fromString(False, "file"):
        rows.append(lst)

    c = Col()
    t = c.colInNum(t.rows)

    zeror = ZeroR()
    zeror.train(t, rows)
    print("\nweathernon")
    zeror.dump()

    t = Row("diabetes.csv")
    rows = []
    for lst in t.fromString(False, "file"):
        rows.append(lst)

    c = Col()
    t = c.colInNum(t.rows)

    zeror = ZeroR()
    zeror.train(t, rows)
    print("\ndiabetes")
    zeror.dump()

    print("\n\n\n#---Nbok-----------------------")
    tbl = Row("weathernon.csv")
    rows = []
    for lst in tbl.fromString(False, "file"):
        rows.append(lst)
    c = Col()
    num = Num()
    sym = Sym()
    tbl.cols = c.colInNum(tbl.rows)
    abcd = Abcd()
    nb = NB(tbl, 3)
    nb.train(tbl, rows)
    print("\nweathernon")
    nb.dump()

    print()
    tbl = Row("diabetes.csv")
    rows = []
    for lst in tbl.fromString(False, "file"):
        rows.append(lst)
    c = Col()

    tbl.cols = c.colInNum(tbl.rows)
    abcd = Abcd()
    nb = NB(tbl, 19)
    nb.train(tbl, rows)
    print("\ndiabetes")
    nb.dump()
