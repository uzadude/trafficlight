import traci
import math
from __builtin__ import int

def getProgramTransfer(programs, lastProgramPointer, curProgramPointer):
    return ''.join(['y' if programs[lastProgramPointer][0][i]=='G' and programs[curProgramPointer][0][i]=='r' else programs[lastProgramPointer][0][i] for i in range(len(programs[curProgramPointer][0])) ])



class Smart:
    
    def __init__(self, tlsID, programs, min_green_time):
        self.min_green_time = min_green_time
        self.yellow_time = 3
        
        self.tlsID=tlsID
        self.programs = programs
        self.programPointer=1
        self.lastProgramPointer=0
        self.in_yellow=0
        self.green=0
        self.lanes_lst=[]
        self.lanes_cars_waiting_map={}
        
    def getNextProgram(self):
        
        if not self.lanes_lst:
            self.lanes_lst = traci.trafficlights.getControlledLanes(self.tlsID)
            self.tls_x, self.tls_y = traci.junction.getPosition(self.tlsID)
        
        self.updateCars()
        
        if self.in_yellow>1:
            self.in_yellow-=1
            print "YELLOW"
            #return self.programs[self.lastProgramPointer].replace('G','y')
            return self.getProgramTransfer()
        elif self.green>0:
            self.green-=1
            return self.programs[self.programPointer][0]
        
        # !main function!
        pointer, T = self.getMinProgram()
        
        print 'current program:',pointer, 'time: ', T
        if (self.programPointer==pointer):
            self.green=T
            print "not changing traffic light program!"
            return self.programs[self.programPointer][0]
        else:
            self.lastProgramPointer=self.programPointer
            self.programPointer=pointer
            self.in_yellow=self.yellow_time
            self.green = max(T-self.yellow_time, self.min_green_time) 
            print "changing traffic light program to:",self.programs[self.programPointer][0]
            #return self.programs[self.lastProgramPointer].replace('G','y')
            # change to yellow only if TL changes from Green to Red
            print 'ProgramTransfer:', self.getProgramTransfer()
            return self.getProgramTransfer()
    
    def getProgramTransfer(self):
        return getProgramTransfer(self.programs, self.lastProgramPointer, self.programPointer)
    
    def updateCars(self):
        for laneID in self.lanes_lst:
            if not laneID in self.lanes_cars_waiting_map.keys():
                self.lanes_cars_waiting_map[laneID]={}
                
            cars_in_lane_lst = traci.lane.getLastStepVehicleIDs(laneID)
            
            #remove cars not in lane
            unwanted_cars = set(self.lanes_cars_waiting_map[laneID].keys()) - set(cars_in_lane_lst)
            for unwanted_car in unwanted_cars: 
                del self.lanes_cars_waiting_map[laneID][unwanted_car]
            
            for car in cars_in_lane_lst:
                # the event that starts counting waiting time
                #w = traci.vehicle.getWaitingTime(car)
                if not car in self.lanes_cars_waiting_map[laneID]:
                    #if w>0.01 and not car in self.lanes_cars_waiting_map[laneID]:
                    x,y = traci.vehicle.getPosition(car)
                    #w = traci.vehicle.getgetWaitingTime(car)
                    if ((self.tls_x-x)*(self.tls_x-x)+(self.tls_y-y)*(self.tls_y-y)<100*100):
                        self.lanes_cars_waiting_map[laneID][car]=0
                    
                # update the waiting time
                if car in self.lanes_cars_waiting_map[laneID]:
                    self.lanes_cars_waiting_map[laneID][car]+=1

class SmartTL(Smart):
    
    def getMinProgram(self):
        min_sum=99999999
        min_program=-1
        
        # cars waiting times
        car_crossing_times = {}
        for i in range(len(self.lanes_lst)):
            laneID = self.lanes_lst[i]
            for carID in self.lanes_cars_waiting_map[laneID]:
                #car_waiting_times[carID] = self.getExpectedWaitingTime(laneID,carID, self.cycle_length, self.programs[self.lastProgramPointer][i]=='G')
                car_crossing_times[carID] = self.getCrossingTime(laneID,carID)
        
        print 'car_waiting_times:', car_crossing_times
        
        for j in range(len(self.programs)):
            program = self.programs[j]
            s = 0
            # going over lanes in this program 
            for i in range(len(program)):
                if (program[i]=='G'):
                    for car in self.lanes_cars_waiting_map[self.lanes_lst[i]]:
                        t=0
                        if not self.programs[self.programPointer][i]=='G':
                            t=self.yellow_time
                        #if (program[i]=='r'):
                        #    s += car_waiting_times[car][0]
                        #elif (program[i]=='G'):
                        #    s += car_waiting_times[car][1]
                        s = max(s, t+car_crossing_times[car])
            
            print program, s, [self.lanes_cars_waiting_map[self.lanes_lst[i]] for i in range(len(program)) if program[i]=='G']
            if min_sum>=s and s>0:
                min_sum=s
                min_program=j
                
        return min_program, 2
                    
    
    def getCrossingTime(self, laneID, carID):
        # calc evacuation time
        a = traci.vehicle.getAccel(carID)
        cur_v = traci.vehicle.getSpeed(carID)
        wanted_v = traci.vehicle.getAllowedSpeed(carID)
        posX,posY = traci.vehicle.getPosition(carID)
        
        if ((self.tls_x-posX)*(self.tls_x-posX)+(self.tls_y-posY)*(self.tls_y-posY)>10*10):
            return 0
        
        
        x = math.sqrt((self.tls_x-posX)*(self.tls_x-posX)+(self.tls_y-posY)*(self.tls_y-posY)) + 5
        
        
        # time and distance to pickup speed from cur_speed to wanted_speed
        t1 = (wanted_v-cur_v)/a
        x1 = cur_v*t1 + 0.5*a*t1*t1
        
        
        if (x-x1)<0:
            # would still be in accel when crossing the signal
            ret = (-cur_v + math.sqrt(cur_v*cur_v + 2*a*x))/a
        else:
            ret = t1 + (x-x1)/wanted_v

        return ret
        
                
    def getExpectedWaitingTime(self, laneID, carID, T, is_green_now):
        
        sg, sr = self.getHeadway(laneID, carID, T, is_green_now)

        return sr,sg

    
    def getHeadway(self, laneID, carID, T, is_green_now):
        
        # current waiting time
        #s = self.lanes_cars_waiting_map[laneID][carID]
        #s=0
        
        #if signal=='r':
        #    return s+T
        

        # calc evacuation time
        a = traci.vehicle.getAccel(carID)
        cur_v = traci.vehicle.getSpeed(carID)
        wanted_v = traci.vehicle.getAllowedSpeed(carID)
        posX,posY = traci.vehicle.getPosition(carID)
        
        x = math.sqrt((self.tls_x-posX)*(self.tls_x-posX)+(self.tls_y-posY)*(self.tls_y-posY))
        
        
        # time and distance to pickup speed from cur_speed to wanted_speed
        t1 = (wanted_v-cur_v)/a
        x1 = cur_v*t1 + 0.5*a*t1*t1
        
        
        if (x-x1)<0:
            # would still be in accel when crossing the signal
            ret = (-cur_v + math.sqrt(cur_v*cur_v + 2*a*x))/a
        else:
            ret = t1 + (x-x1)/wanted_v


        return ret, (int(ret/T)+1)*T
        
        
              
        