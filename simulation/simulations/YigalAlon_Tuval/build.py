import random

def generate_routefile(seed, steps, pace_factor):
    random.seed(seed)  # make tests reproducible
    
    N = steps  # number of time steps
    # demand per second from different directions
    c = 1.0*pace_factor/60.0
    
    #pArr = [(25*c, 'right'), (44*c, 'left'), (4*c, 'left_left'), (3*c, 'up_left')]
    pArr = [(44*c, 'left'), (4*c, 'left_left'), (3*c, 'up_left')]
    
    with open("simulations/YigalAlon_Tuval/gen/cross.rou.xml", "w") as routes:
        # <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        # <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="17" minGap="3" maxSpeed="25" guiShape="bus"/>
        print >> routes, """<routes>
        <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>

        <route id="right" edges="1i 2o" />
        <route id="left" edges="2i 1o" />
        <route id="left_left" edges="2i 3o" />
        <route id="up_left" edges="3i 1o" />
        
        """
        vehNr = 0
        for i in range(N):
            for pRoute in pArr:
                if random.uniform(0, 1) < pRoute[0]:
                    print >> routes, '<vehicle id="%s_%i" type="type1" route="%s" depart="%i" />' % (pRoute[1], vehNr, pRoute[1], i)
                    vehNr += 1
            # for non-uniform right going vehicles
            if random.uniform(0, 1) < 50*c and i%90>60:
                print >> routes, '<vehicle id="%s_%i" type="type1" route="%s" depart="%i" />' % ('right', vehNr, 'right', i)
                vehNr += 1
        print >> routes, "</routes>"
    
        
def getPossiblePrograms():
    #return ["GGGrrrrr","rrrGGrrr","rrrrrGGG"]
    return [("GGGrrrrr", 20), ("GGrrrGGG", 70), ("rrrGGrrr", 20)]

    
        