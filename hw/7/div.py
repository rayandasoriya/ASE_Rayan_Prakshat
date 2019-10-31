from lib import *
import hw6
from hw6 import *

class Div2(Pretty):

    def __init__(i, lst, x=0, y=6, yis="Num"):
        i.yis = yis
        i.x_lst, i.y_lst = i.getObjects(sorted(lst, key=lambda xyz: xyz[6]), yis)
        i.b4 = i.y_lst
        i._lst = i.y_lst.numList if i.yis == "Num" else i.y_lst.symList
        i.gain = 0
        i.step = int(i.y_lst.count ** THE.div.min)
        i.stop = last(i._lst)
        i.start = first(i._lst)
        i.ranges = []
        i.xranges = []
        i.epsilon = i.b4.sd * THE.div.cohen
        i.rank, i.cut, i.best = i.__divide(x, y, i.b4, 1)
        i.gain /= len(i._lst)

    def getObjects(i, data, yis):
        x_lst = hw6.Num()
        if yis == "Num":
            y_lst = hw6.Num()
        else:
            y_lst =hw6. Sym()
        for i in data:
            x_lst.num2(i[0])
            if yis == "Num":
                y_lst.num2(i[1])
            else:
                y_lst.Sym2(i[1])
        return x_lst, y_lst

    def xis(i, lst):
        num = hw6.Num()
        for i in lst:
            num.num2(i)
        return num

    def yis1(i, lst, key):
        sym = hw6.Sym()
        for row in lst:
            sym.Sym2(row[key])
        return sym

    def symSplit(i, lst):
        sym = hw6.Sym()
        for i in lst:
            sym.Sym2(i)
        return sym

    def xSplit(i):
        start = 0
        for j in i.ranges:
            i.xranges.append(i.xis(i.x_lst.numList[start:start + j.count]))
            start += j.count

    def printSplits(i):
        if i.yis == "Num":
            print("\nPart 1:")
            for k in range(len(i.ranges)):
                x = i.xranges[k]
                y = i.ranges[k]
                print(k + 1,"  x.n\t" + str(x.count) + " | x.lo \t" + str(
                    round(x.lo, 5)) + " | x.hi \t" + str(
                    round(x.hi, 5)) + " | y.lo \t" + str(round(y.lo, 5)) + " | y.hi \t" + str(round(y.hi, 5)))
        else:
            print("\nPart 2:")
            for k in range(len(i.ranges)):
                x = i.xranges[k]
                y = i.ranges[k]
                print(k + 1, "  x.n\t" + str(x.count) + " | x.lo \t" + str(
                    round(x.lo, 5)) + " | x.hi \t" + str(
                    round(x.hi, 5)) + "  | y.mode \t" + str(y.mode) + " | y.ent \t " + str(round(y.sd, 5)))

    def __divide(i, lo, hi, b4, rank):

        "Find a split between lo and hi, then recurse on each split."

        if i.yis == "Num":
            l = i.xis([])
            r = i.xis(i._lst[lo:hi])
            i.stop = last(b4.numList)
            i.start = first(b4.numList)
        else:
            l = i.symSplit([])
            print(l)
            r = i.symSplit(i._lst[lo:hi])
            i.stop = last(b4.symList)
            i.start = first(b4.symList)
        i.epsilon = b4.sd * THE.div.cohen
        best = b4.sd
        cut = None
        for j in range(lo, hi):
            if i.yis == "Num":
                print(i._lst[j])
                l.num2(i._lst[j])
                r.numLess2(0)
                # print(r.numList)
            else:
                l.Sym2(i._lst[j])
                r.symLess(i._lst[j])

            if l.count >= i.step:
                if r.count >= i.step:
                    now = i._lst[j - 1]
                    after = i._lst[j]
                    if now == after: continue
                    if i.yis == "Num":
                        if abs(r.mu - l.mu) >= i.epsilon:
                            if after - i.start >= i.epsilon:
                                if i.stop - now >= i.epsilon:
                                    xpect = l.xpect(r)
                                    if xpect * THE.div.trivial < best:
                                        best, cut = xpect, j
                    else:
                        if abs(ord(l.mode) - ord(r.mode)) >= i.epsilon:
                            if ord(after) - ord(i.start) >= i.epsilon:
                                if ord(i.stop) - ord(now) >= i.epsilon:
                                    xpect = l.xpect(r)
                                    if xpect * THE.div.trivial < best:
                                        best, cut = xpect, j
        if cut:
            ls, rs = i._lst[lo:cut], i._lst[cut:hi]
            if i.yis == "Num":
                rank = i.__divide(lo, cut, i.xis(ls), rank)[0] + 1
                rank = i.__divide(cut, hi, i.xis(rs), rank)[0]
            else:
                rank = i.__divide(lo, cut, i.symSplit(ls), rank)[0] + 1
                rank = i.__divide(cut, hi, i.symSplit(rs), rank)[0]
        else:
            i.gain += b4.count * b4.sd
            b4.rank = rank
            i.ranges += [b4]
        return rank, cut, best
