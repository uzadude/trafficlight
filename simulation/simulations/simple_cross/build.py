import random

def generate_routefile(seed, steps, pace_factor):
    random.seed(seed)  # make tests reproducible
    
    N = steps  # number of time steps
    # demand per second from different directions
    pace_factor = pace_factor*1.0/10
    pArr = [(1.*pace_factor, 'right'),(1.*pace_factor, 'left'),(1.*pace_factor, 'down'),(1.*pace_factor, 'up')]
    
    with open("simulations/simple_cross/gen/cross.rou.xml", "w") as routes:
        # <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        # <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="17" minGap="3" maxSpeed="25" guiShape="bus"/>
        print >> routes, """<routes>
        <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>

        <route id="right" edges="1i 2o" />
        <route id="left" edges="2i 1o" />
        <route id="up" edges="3i 4o" />
        <route id="down" edges="4i 3o" />
        
        """
        vehNr = 0
        for i in range(N):
            for pRoute in pArr:
                if random.uniform(0, 1) < pRoute[0]:
                    print >> routes, '<vehicle id="%s_%i" type="type1" route="%s" depart="%i" />' % (pRoute[1], vehNr, pRoute[1], i)
                    vehNr += 1
        print >> routes, "</routes>"
    
        
def getPossiblePrograms():
    return [("GrGr", 10), ("rGrG", 10)]         
        