# Code developed by Rayan Dasoriya(rdasori) and Prakshatkumar Shah(pmshah) for ASE HW1.
import random

class Col():

    def __init__(self):
        # Change in array
        self.n = []
        self.mean = []
        self.sd = []
        self.m2 = []
        self.maxV = []
        self.minV = []
    
    def colInNum(self, rows):
        numCols = len(rows[0])
        cols = [[-1 for _ in range(len(rows))] for _ in range(len(rows[0]))]
        for i in range(1,len(rows)):
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
        self.maxV =-1*10**32
        self.minV = 1*10**32

    # Function to calculate the SD using variance
    def _numSd(self, count):
        if count == 1:
            self.sd = 0
        else:
            self.sd = (self.m2/(count-1))**0.5

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
        return round(self.mu,2), round(self.sd,2), round(self.m2,2), count, self.maxV, self.minV
    
    # Method to remove the element and update mean and standard deviation
    def numLess(self, array):
        subtract_mean = []
        subtract_sd = []
        count = len(array)-1
        for _ in range(len(array)-1, 0, -1):
            if count % 10 == 0:
                subtract_mean.append(round(self.mu, 2))
                subtract_sd.append(round(self.sd, 2))
            count -= 1
            deleteValue = array.pop()
            delta = deleteValue-self.mu
            self.mu -= delta/count
            self.m2 -= delta*(deleteValue-self.mu)
            self._numSd(count)
        return subtract_mean, subtract_sd
    
class Sym(Col):
    pass


class Some(Col):
    pass


if __name__ == "__main__":
    num = Num()

    # Generating an array of length 100 with random integers
    array = []
    for _ in range(100):
        array.append(random.randint(1, 101))

    add_mean, add_sd = num.num1(array)
    print("Mean & SD after adding elements: ")
    print("add_mean: ", add_mean)
    print("add_sd: ", add_sd)

    subtract_mean, subtract_sd = num.numLess(array)

    print()
    print("Mean and Standard Deviation after removing elements: ")
    print("subtract_mean: ", subtract_mean)
    print("subtract_sd: ", subtract_sd)
