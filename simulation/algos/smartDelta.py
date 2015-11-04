import traci
import math
from algos.smart import Smart
import sets

class SmartDelta(Smart):
    
    def getMinProgram(self):
        max_programs={}
        
        tl_cur_waiting_time = 0
        tl_cur_waiting_cars = 0
        
        # cars waiting times
        self.crossing_cars_waiting_times = {}
        for i in range(len(self.lanes_lst)):
            laneID = self.lanes_lst[i]
            for carID in self.lanes_cars_waiting_map[laneID]:
                self.crossing_cars_waiting_times[carID] = self.getCrossingTime(laneID, carID)
                tl_cur_waiting_time += self.lanes_cars_waiting_map[laneID][carID]
                tl_cur_waiting_cars += 1
        
        print 'current TL total waiting time:', tl_cur_waiting_time
        print 'current TL total waiting cars:', tl_cur_waiting_cars
        print 'raw waiting times:', [(l, sum(self.lanes_cars_waiting_map[l][c] for c in self.lanes_cars_waiting_map[l])) for l in self.lanes_cars_waiting_map.keys()], 'in details:',self.lanes_cars_waiting_map
        print 'crossing_cars_waiting_times:', [(l, sum(self.crossing_cars_waiting_times[c] for c in self.lanes_cars_waiting_map[l] if c in self.crossing_cars_waiting_times)) for l in self.lanes_cars_waiting_map.keys()], 'in details:', self.crossing_cars_waiting_times
        print 'raw waiting cars:', [(l, len(self.lanes_cars_waiting_map[l])) for l in self.lanes_cars_waiting_map.keys()]
        
        for j in range(len(self.programs)):
            program = self.programs[j][0]
            lanes = sets.Set()
            dT=[]
            for T in [3,5,10,15,20]:
                s = 0
                # going over lanes in this program 
                for i in range(len(program)):
                    if (program[i]=='G'):
                        laneID = self.lanes_lst[i]
                        lanes.add(laneID) 
                        for carID in self.lanes_cars_waiting_map[laneID]:
                            #delta += self.getDeltaWaitTimeVByT(laneID, carID, self.cycle_length, self.programs[self.lastProgramPointer][i]=='G')
                            s += self.getDeltaWaitTimeVByT(laneID, carID, T, self.programs[self.programPointer][0][i]=='G')
                dT.append((T,s))

            T,score = max(dT, key=lambda x:x[1])
            
            print program, 'lanes:', lanes,', score: ', T*score, 'time cycle:', T, 'score array:', dT
            
            max_programs[j] = (score, T)
        
        retProgram = max(max_programs, key=max_programs.get) 
        return retProgram, max_programs[retProgram][1] 

    def getDeltaWaitTimeVByT(self, laneID, carID, T, is_green_now):
        
        if (not is_green_now and T<self.yellow_time+self.min_green_time):
            return 0
        
        # car waiting time
        s = self.lanes_cars_waiting_map[laneID][carID]
        t = self.crossing_cars_waiting_times[carID]

        if is_green_now:
            T_fixed = T
        else:
            T_fixed = T - self.yellow_time

        if (t>T_fixed):
            return 0
        else:
            return (s+t)*1.0/T
            #return 1.0/T
        
                
    def getCrossingTime(self, laneID, carID):
               
        # calc evacuation time
        a = traci.vehicle.getAccel(carID)
        cur_v = traci.vehicle.getSpeed(carID)
        wanted_v = traci.vehicle.getAllowedSpeed(carID)
        posX,posY = traci.vehicle.getPosition(carID)
        
        # adding bias for junction's length
        x = math.sqrt((self.tls_x-posX)*(self.tls_x-posX)+(self.tls_y-posY)*(self.tls_y-posY)) + 5
        
        # time and distance to pickup speed from cur_speed to wanted_speed
        t1 = (wanted_v-cur_v)/a
        x1 = cur_v*t1 + 0.5*a*t1*t1
        
        if (x-x1)<0:
            # would still be in accel when crossing the signal
            t = (-cur_v + math.sqrt(cur_v*cur_v + 2*a*x))/a
        else:
            t = t1 + (x-x1)/wanted_v

        return t
              
        