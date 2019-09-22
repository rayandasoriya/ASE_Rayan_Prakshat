import collections


class Abcd():
    def __init__(self, rx='rx', data='data'):
        self.known = collections.defaultdict(int)
        self.aMap = collections.defaultdict(int)
        self.bMap = collections.defaultdict(int)
        self.cMap = collections.defaultdict(int)
        self.dMap = collections.defaultdict(int)
        self.rx = rx
        self.data = data
        self.yes = 0
        self.no = 0

    def abcd1(self, actual, predicted):
        self.known[actual] += 1
        if self.known[actual] == 1:
            self.aMap[actual] = self.yes + self.no

        self.known[predicted] += 1
        if self.known[predicted] == 1:
            self.aMap[predicted] = self.yes + self.no

        if actual == predicted:
            self.yes += 1
        else:
            self.no += 1

        for x in self.known:
            if actual == x:
                if actual == predicted:
                    self.dMap[x] += 1
                else:
                    self.bMap[x] += 1
            else:
                if x == predicted:
                    self.cMap[x] += 1
                else:
                    self.aMap[x] += 1

    def report(self):
        """ print the Abcd report """
        bar = "---------"

        print(
            "db        |rx         |num        |a          | b         | c         | d         | acc       | pre       | pd        | pf        | f         | g         | class")
        print("%5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s | %5s" % (
            bar, bar, bar, bar, bar, bar, bar, bar, bar, bar, bar, bar, bar, "----"))

        # iterate through symbol dictionary
        for sym in self.known:
            pd = pf = pn = prec = g = f = acc = 0
            a = self.aMap[sym]
            b = self.bMap[sym]
            c = self.cMap[sym]
            d = self.dMap[sym]

            if (b + d) > 0:
                pd = float(d / (b + d))
            if (a + c) > 0:
                pf = float(c / (a + c))
            if (a + c) > 0:
                pn = (b + d) / (a + c)
            if (c + d) > 0:
                prec = float(d / (c + d))
            if (1 - pf + pd) > 0 and prec + pd > 0:
                f = float((2 * prec * pd) / (prec + pd))
            else:
                f = 0
            if (prec + pd) > 0 and (1 - pf + pd) > 0:
                g = float(2 * (1 - pf) * pd / (1 - pf + pd))
            else:
                g = 0
            acc = float(self.yes / (self.yes + self.no))

            print(
                "%5s     |%5s      |%5s      |%5s      | %5s     | %5s     | %5s     | %5s     | %5s     | %5s     | %5s     | %5s     | %5s     | %5s    " % (
                    "data", "rx", self.yes + self.no, a, b, c, d, round(acc, 2), round(prec, 2), round(pd, 2),
                    round(pf, 2),
                    round(f, 2), round(g, 2), sym))
