from algos.smart import Smart

# according to:
# http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1343&context=eeng_fac
class SmartYu(Smart):
    
    def getMinProgram(self):
        min_sum=99999999
        min_program=-1
        
        for j in range(len(self.programs)):
            program = self.programs[j]
            s = 0
            # going over lanes in this program
            print program 
            for i in range(len(program)):
                laneID = self.lanes_lst[i]
                st = self.getLaneExpectedWaitingTime(laneID, self.min_green_time + self.yellow_time, program[i], program[i]==self.programs[self.lastProgramPointer][i])
                s += sum([st[x] for x in st.keys()])
                print laneID, st
            
            print 'total: ', s
            #print program, s, [self.lanes_cars_waiting_map[self.lanes_lst[i]] for i in range(len(program)) if program[i]=='G']
            if min_sum>=s:
                min_sum=s
                min_program=j
                
        return min_program
                    
                
    def getLaneExpectedWaitingTime(self, laneID, T, signal, is_green_now):
        
        hw = 4
        q = len(self.lanes_cars_waiting_map[laneID])
        q_out = min([q , 1+int(T/hw)])
        
        if (q==0):
            return {}
        
        s={}
        
        #up-to-now waiting time
        s['wait'] = self.getLaneWaitingTime(laneID)

        # compensate for the time it takes to move to green - my term
        if signal=='G' and not is_green_now:
            T -= self.yellow_time
            s['yellow_change'] = q*self.yellow_time

        
        if signal=='G' and T>=(q-1)*hw:
            # 1st term - evacuation time
            s['G all evac'] = q*(q+1)/2*hw
            
            # 2nd term - up-to-now waiting time

            # 3rd and 4th terms TBD
            
            return s
        
        elif signal=='G':
            # 1st term - evacuation time
            s['G more evac'] = q_out*(q_out+1)/2*hw
            
            # 2nd term - up-to-now waiting time

            # 3rd term - waiting time of cars not released in this step
            s['G more others'] = (q-q_out)*T
            
            # 4th term TBD
            
            return s
        
        elif signal=='r':
            
            # 1st term - all waiting time
            s['red'] = q*T
            
            # 2nd term - up-to-now waiting time
            
            # 3rd term TBD
            
            
            return s
        

    def getLaneWaitingTime(self, laneID):
        map_lst = self.lanes_cars_waiting_map[laneID]
        return sum(map_lst[car] for car in map_lst.keys())
    