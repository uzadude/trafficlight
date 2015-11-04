import random

def getNextAvgTime(a):
    r = random.uniform(0, 1)
    return a/2+r*a

def generate_routefile(seed, steps, pace_factor):
    random.seed(seed)  # make tests reproducible
    
    N = steps  # number of time steps
    # demand per second from different directions
    pace_factor = 1.0*pace_factor*10
    
    pArr = [(1./getNextAvgTime(pace_factor), 'right'),(1./getNextAvgTime(pace_factor), 'left'),(1./getNextAvgTime(pace_factor), 'down'),(1./getNextAvgTime(pace_factor), 'up'),
            (1./getNextAvgTime(pace_factor), 'right_left'),(1./getNextAvgTime(pace_factor), 'left_left'),(1./getNextAvgTime(pace_factor), 'down_left'),(1./getNextAvgTime(pace_factor), 'up_left')]
    
    with open("simulations/simple_cross_with_left/gen/cross.rou.xml", "w") as routes:
        # <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        # <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="17" minGap="3" maxSpeed="25" guiShape="bus"/>
        print >> routes, """<routes>
        <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>

        <route id="right" edges="1i 2o" />
        <route id="right_left" edges="1i 4o" />
        <route id="left" edges="2i 1o" />
        <route id="left_left" edges="2i 3o" />
        <route id="up" edges="3i 4o" />
        <route id="up_left" edges="3i 1o" />
        <route id="down" edges="4i 3o" />
        <route id="down_left" edges="4i 2o" />
        
        """
        vehNr = 0
        for i in range(N):
            for pRoute in pArr:
                if random.uniform(0, 1) < pRoute[0]:
                    print >> routes, '<vehicle id="%s_%i" type="type1" route="%s" depart="%i" />' % (pRoute[1], vehNr, pRoute[1], i)
                    vehNr += 1
        print >> routes, "</routes>"
    
        
def getPossiblePrograms():
    return [("GrrrGrrr", 10), ("rGrrrGrr", 10), ("rrGrrrGr", 10), ("rrrGrrrG", 10)] # 5157 
    #return ["GGrrrrrr", "rrGGrrrr", "rrrrGGrr", "rrrrrrGG"] # 4783
    #return [("GGrrrrrr", 10), ("rrGGrrrr", 10), ("rrrrGGrr", 10), ("rrrrrrGG", 10), ("GrrrGrrr", 10), ("rGrrrGrr", 10), ("rrGrrrGr", 10), ("rrrGrrrG", 10)] # 4178
    
        