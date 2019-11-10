import copy


class decisionTree:
    def __init__(i):
        i.MIN_ROWS = 9

    def createDecisionTree(i, tbl, labeltype):
        s = set()
        finalDT = i.recurse(tbl, s, 1, labeltype)
        finalDT.setLevel(0)
        finalDT.makeRoot()
        if labeltype == 'sym':
            finalDT.pruneTree(finalDT)
            finalDT.printTree(finalDT, labeltype, 0)
        else:
            finalDT.printTree(finalDT, labeltype, 0)

    def recurse(i, tbl, rows, level, labeltype):
        newtbl = copy.deepcopy(tbl)
        i, adj = 0, 0
        count = len(newtbl.rows)
        while i < count:
            if rows:
                if i not in rows:
                    newtbl.deleteRow(i - adj)
                    adj += 1
            i += 1
        if labeltype == 'sym':
            labelsym = Sym()
            labelsym.Sym1(newtbl.cols[-1])
            if len(newtbl.rows) > i.MIN_ROWS and labelsym.most < len(newtbl.rows):
                node = decisionTree(labeltype)
                div2 = Div2(sym, "first", "last", labeltype)
                div2.xSplit()
                bestInformationGain = 0
                bestFeature = ''
                # for j in range(len(newtbl.cols)-1):
