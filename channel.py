from agents import *

class Channel:
    def __init__(self, eavesdroppingRate):
        #store eavesdropping rate; if 0, no eavesdropper present
        self.eavesdroppingRate = eavesdroppingRate
        #initialize bob, alice, and if an eavesdropper is present, eve object
        self.b = Bob()
        self.a = Alice()
        if self.eavesdroppingRate > 0:
            self.e = Eve(eavesdroppingRate)
            self.peopleList = [self.a, self.e, self.b]
        else:
            self.e = None
            self.peopleList = [self.a, self.b]
    
    
    def simulate_one_cycle(self, i):
        """perform the operations of one cycle"""
        #transmission of qubit by Alice
        self.qubit = self.a.one_step()
        tmp, tmp1 = self.a.getInfo(i)
        if self.e!=None:
            #eavesdropping by Eve
            self.qubit = self.e.one_step(self.qubit)
            tmp2, tmp3 = self.e.getInfo(i)
        #measurement by Bob
        result = self.b.one_step(self.qubit)
        tmp4, tmp5 = self.b.getInfo(i)
        #return info relevant for plotting
        if self.e!=None:
            return [[tmp, tmp1], [tmp2, tmp3], [tmp4, tmp5]]
        else:
            return [[tmp, tmp1], [tmp4, tmp5]]


    def compareBasis(self, number):  
        """compare the basis of Alice and Bob at index number; keep bit if they are the same"""
        if self.a.basis_array[number]==self.b.basis_array[number]:
            for person in self.peopleList:
                if person.name!="Eve" or self.compareBasisE(number):
                    person.keepBit(number)
                else:
                    person.keepBit(-1)
            return True
        else:
            return False


    def compareBasisE(self, number):
        """compare the basis of Alice and Eve at index number to determine whether Eve should keep bit; returns True or False"""
        if self.e !=None:
            if self.a.basis_array[number]==self.e.basis_array[number] and self.e.bit_array[number]!=-1:
                return True
            else:
                return False


    def replaceKey(self):
        """replaces the old bit array by the new bit array for every person"""
        for person in self.peopleList:
            person.replaceKey()


    def compareBit(self, number):
        """compares bit of Alice and Bob at index "number" and returns True or False accordingly"""
        if self.a.bit_array[number]==self.b.bit_array[number]:
            return True
        else:
            return False
            
    
    def getBits(self):
        """returns list of list of bits of every person"""
        returnList = []
        for person in self.peopleList:
            returnList.append(person.getBits())
        return returnList


    def getSubset(self, number, keepTrack=False):
        """returns subset of indices of bit array"""
        return self.a.getNewSubset(number, keepTrack)
    
    def forgetIndices(self):
        """forget bits at subset indices and prepare a postprocessing step"""
        subset = self.a.subset
        #keep only bits which are not in subset
        for i in range(len(self.a.bit_array)):
            if i in subset:
                pass
            else:
                for person in self.peopleList:
                    person.keepBit(i)
        #replace bit arrays and update indices list
        self.preparePostprocessing()


    def preparePostprocessing(self):
        """replace the old bitarray by the new bit array and create a list of 
        indices required for a postprocessing step"""
        for person in self.peopleList:
            person.replaceKey()
        self.a.indices = list(range(len(self.a.bit_array)))


    def compareFinalKeys(self):
        """return if the final keys are shared among Alice and Bob and if they 
        are private, meaning that Eve does not have any knowledge about it"""
        shared = True
        private = True
        for index in range(self.a.getArrayLength()):
            if not (self.compareBit(index)):
                shared = False
            if self.e!=None:

                private = False
        return [shared, private]