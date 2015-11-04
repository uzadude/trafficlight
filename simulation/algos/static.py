from algos.smart import getProgramTransfer
from __builtin__ import int


class Static:
    
    def __init__(self, tlsID, programs, green_time_factor):
        self.programs = programs
        self.lastProgramPointer=0
        self.programPointer=1
        self.yellow_time = 3
        self.green_time_factor = green_time_factor
        self.green_time = self.programs[self.programPointer][1]
        self.counter=0
        self.tlsID=tlsID
    
    def getNextProgram(self):
        self.counter+=1
        
        if (self.counter % int(self.green_time*self.green_time_factor) == 0):
            self.counter=0
            self.lastProgramPointer = self.programPointer
            self.programPointer = (self.programPointer+1) % len(self.programs)
            self.green_time = self.programs[self.programPointer][1]
            print 'changing to program:', self.programs[self.programPointer]

        if (self.counter<self.yellow_time):
            return getProgramTransfer(self.programs, self.lastProgramPointer, self.programPointer)
        else:
            return self.programs[self.programPointer][0]
        