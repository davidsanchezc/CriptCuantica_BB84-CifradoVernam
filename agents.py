import random
import numpy as np

class Person:
    def __init__(self, name):
        #list storing all bits
        self.bit_array = []
        #list used to update bits through the different phases
        self.newBitArray = []
        #list storing all basis
        self.basis_array = []
        #Alice, Bob, or Eve 
        self.name = name

    def choose_basis(self):
        """return a basis at random"""
        if random.random()<0.5:
            return 0;
        else:
            return 1;

    def get_operator(self, basis):
        """return measurement operator according to basis""" 
        if basis==0:
            A = np.array([[1, 0], [0, -1]])
        else:
            A = np.array([[0,1],[1,0]])
        return A

    def get_density_matrix(self, bit, basis):
        """returns density matrix for qubit according to bit and basis"""
        if bit==0 and basis==0:
            rho = np.array([[1,0],[0,0]])
        elif bit==1 and basis==0:
            rho = np.array([[0,0],[0,1]])
        elif bit==0 and basis==1:
            rho = np.array([[0.5,0.5],[0.5,0.5]])
        else:
            rho = np.array([[0.5,-0.5],[-0.5,0.5]])
        return rho
    
    def measure(self,rho):
        """perform one measurement given one qubit and return resulting bit and chosen basis"""
        #first choose basis
        basis = self.choose_basis()
        #obtain measurement operator
        A = self.get_operator(basis)
        #perform measurement
        value = np.trace(np.matmul( A, rho))
        #determine resulting bit
        r = random.random()*2-1
        if r>value:
            result = 1
        else:
            result = 0
        #store values
        self.bit_array.append(result)
        self.basis_array.append(basis)
        return result, basis
    
    def create_qubit(self, bit_=None, basis_=None):
        """create qubit from optional input bit and basis or by randomly selecting bit and basis"""
        if bit_==None or basis_==None:
            #crea un bit y una base aleatorios
            if random.random()<0.5:
                bit = 0
            else:
                bit = 1
            self.bit_array.append(bit)
            basis = self.choose_basis()
            self.basis_array.append(basis)
        else:
            #guarda el bit y la base ingresados
            bit = bit_
            basis = basis_
        #retorna un qubit en una matriz
        return self.get_density_matrix(bit, basis)
    
    def getInfo(self, number):
        """return the bit and basis at a given index"""
        return self.bit_array[number], self.basis_array[number]
    
    def keepBit(self, index, value=True):
        """store a bit at a certain index or of a certain value in the new bit array"""
        if index!=-1:
            if value:
                #store value of old bit array at certain index 
                self.newBitArray.append(self.bit_array[index])
            else:
                #store value
                self.newBitArray.append(index)
        else:
            #store empty value denoted by -1
            self.newBitArray.append(-1)
            
   # def discardBit(self, index):
        
    #    self.newBitArray.pop(index)
    def getBits(self):
        """returns bit array"""
        return self.bit_array
    
    def getArrayLength(self):
        """returns array length of bit array"""
        return len(self.bit_array)
    
    def replaceKey(self):
        """replaces the old bit array by the new bit array"""
        self.bit_array = self.newBitArray
        self.newBitArray = []

    
class Bob(Person):
    def __init__(self):
        super().__init__("Bob")
        
    def one_step(self, rho):
        """one step in the transmission and measurement phase performed by Bob"""
        bit, basis = super().measure(rho)
        qubit = super().create_qubit(bit, basis)
        return qubit


class Alice(Person):
    def __init__(self):
        self.subset = []
        self.indices = []
        super().__init__("Alice")
        
    def one_step(self):
        """one step in the transmission and measurement phase performed by Alice"""
        return super().create_qubit()
    
    def getNewSubset(self, number, keepTrack=False):
        """return a subset of indices of the current bit array; size of subset specified by input number"""
        if keepTrack ==False:
            #determine subset without removing it from the array
            if number <= len(self.bit_array):
                self.subset = random.sample(list(range(len(self.bit_array))), number)
                return self.subset
        else:
            #determine subset and remove these indices from the array
            if number <= len(self.indices):
                self.subset = random.sample(self.indices, number)
                tmp = []
                for i in self.indices:
                    if i in self.subset:
                        pass
                    else:
                        tmp.append(i)
                self.indices = tmp
                return self.subset
        return None

class Eve(Person):
    def __init__(self, percentage):
        super().__init__("Eve")
        self.percentage = percentage
        
    def one_step(self, rho):
        """one step in the transmission and measurement phase performed by Eve"""
        #perform an intercept-resend attack with the probability self.percentage
        if random.random()< self.percentage:
            bit, basis = super().measure(rho)
            qubit = super().create_qubit(bit,basis)
            return qubit
        else:
            #store "empty" values
            self.bit_array.append(-1)
            self.basis_array.append(-1)
            return rho