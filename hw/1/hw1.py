# Code developed by Rayan Dasoriya(rdasori) and Prakshatkumar Shah(pmshah) for ASE HW1.
import random


class Col:
    def __init__(self):
        # Change in array
        self.n = 0


class Num(Col):
    def __init__(self):
        Col.__init__(self)
        self.mu = 0
        self.m2 = 0
        self.sd = 0

    # Function to calculate the SD using variance
    def _numSd(self):
        if self.n == 1:
            self.sd = 0
        else:
            self.sd = (self.m2/(self.n-1))**0.5

    # Method to incrementally update mean and standard deviation
    def num1(self, array):
        add_mean = []
        add_sd = []
        for i in range(len(array)):
            self.n += 1
            delta = array[i] - self.mu
            self.mu += (delta / self.n)
            delta2 = array[i] - self.mu
            # Calculation of square mean distance
            self.m2 += delta * delta2
            self._numSd()
            # Adding the mean and sd to a list after 10 elements
            if (i+1) % 10 == 0:
                add_mean.append(round(self.mu, 2))
                add_sd.append(round(self.sd, 2))
        return add_mean, add_sd

    # Method to remove the element and update mean and standard deviation
    def numLess(self, array):
        subtract_mean = []
        subtract_sd = []
        for _ in range(len(array)-1, 0, -1):
            if self.n % 10 == 0:
                subtract_mean.append(round(self.mu, 2))
                subtract_sd.append(round(self.sd, 2))
            self.n -= 1
            deleteValue = array.pop()
            delta = deleteValue-self.mu
            self.mu -= delta/self.n
            self.m2 -= delta*(deleteValue-self.mu)
            self._numSd()
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
