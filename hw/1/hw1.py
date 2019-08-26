# Code developed by Rayan Dasoriya(rdasori) and Prakshatkumar Shah(pmshah) for ASE HW1.

import random
class Col:
    def __init__(self):
        self.array = []
        self.old_count = 0

    # Generate an array of 100 random numbers
    def generateArray(self):
        for _ in range(100):
            self.array.append(random.randint(1,101))

class Num(Col):
    def __init__(self):
        Col.__init__(self)
        self.old_mean = 0
        self.old_m2 = 0
        self.old_sd = 0
        self.add_mean = []
        self.subtract_mean = []
        self.add_sd = []
        self.subtract_sd = []

    # Function to calculate the SD using variance
    def _numSd(self):
        if self.old_count == 1:
            self.old_sd = 0
        else:
            self.old_sd = (self.old_m2/(self.old_count-1))**0.5

    # Method to incrementally update mean and standard deviation
    def numAdd(self):
        for i in range(100):
            self.old_count+=1
            delta = self.array[i]-self.old_mean
            self.old_mean += (delta/self.old_count)
            delta2 = self.array[i]-self.old_mean
            # Calculation of square mean distance
            self.old_m2+=delta*delta2
            self._numSd()
            # Adding the mean and sd to a list after 10 elements
            if (i+1)%10==0:
                self.add_mean.append(round(self.old_mean,2))
                self.add_sd.append(round(self.old_sd,2))
            
    # Method to remove the element and update mean and standard deviation
    def numRemove(self):
        for _ in range(99,9,-1):
            self.old_count-=1
            deleteValue = self.array.pop()
            delta = deleteValue-self.old_mean
            self.old_mean-=delta/self.old_count
            self.old_m2-=delta*(deleteValue-self.old_mean)
            self._numSd()
            # Adding the mean and sd to a list after removing 10 elements
            if self.old_count%10==0:
                self.subtract_mean.append(round(self.old_mean,2))
                self.subtract_sd.append(round(self.old_sd,2))

    def printData(self):
        # Since the size of the array is 100, the size of add_mean and add_sd should be 10(10,20, ..,100).
        # But the size of subtract_mean and subtract_sd should be 9 because we are initially removing the 
        # first element, which makes the size as 99. Hence, we are not considering the mean and sd at that point. 
        # So, the list will contain the mean and sd for (90,80,..,10) elements in the list.

        print("Mean after adding and removing elements: ")
        print("add_mean: ", self.add_mean)
        print("subtract_mean: ", self.subtract_mean)
        
        print("Standard Deviation after adding and removing elements: ")
        print("add_sd: ", self.add_sd)
        print("subtract_sd: ", self.subtract_sd)

class Sym(Col):
    pass

class Some(Col):
    pass

col = Num()
col.generateArray()
col.numAdd()
col.numRemove()
col.printData()