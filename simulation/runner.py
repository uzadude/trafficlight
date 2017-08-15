#!/usr/bin/env python
"""
@file    runner.py
@author  Lena Kalleske
@author  Daniel Krajzewicz
@author  Michael Behrisch
@author  Jakob Erdmann
@date    2009-03-26
@version $Id: runner.py 18096 2015-03-17 09:50:59Z behrisch $

Tutorial for traffic light control via the TraCI interface.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2009-2015 DLR/TS, Germany

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import os
import sys
import optparse
import subprocess
import random

# we need to import python modules from the $SUMO_HOME/tools directory
# try:
# sys.path.append(os.path.join(os.path.dirname(
#     __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
# sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
#     os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
sumo_home = os.environ.get("SUMO_HOME")
a = os.path.join(sumo_home, "tools")
sys.path.append(a)

# except ImportError:
#     sys.exit(
#         "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

from algos import static, smart
from sumolib import checkBinary

import traci
import sets
from algos.smartDelta import SmartDelta

# from simulations.simple_cross import build
# import simulations
# the port used for communicating with your sumo instance
PORT = 8873


def run(options, simulation):
    """execute the TraCI control loop"""
    traci.init(PORT)

    possible_programs = simulation.getPossiblePrograms()

    if options.algo == 'static':
        algo = static.Static("0", possible_programs, options.greentime)
        title = 'static-' + str(options.greentime)
    elif options.algo == 'smart':
        algo = smart.SmartTL("0", possible_programs, options.greentime)
        title = 'smart-' + str(options.greentime)
    elif options.algo == 'smartDelta':
        algo = SmartDelta("0", possible_programs, options.greentime)
        title = 'smartDelta-' + str(options.greentime)

    step = 0
    cars_lst = {}
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print '========================================================================================================================================================'
        print 'step', step
        stepWaitingTime = 0
        cnt_waiting_cars = 0
        cnt_cars = 0
        id_list = traci.vehicle.getIDList()
        for car in id_list:
            w = traci.vehicle.getWaitingTime(car)
            cnt_cars += 1
            if not car in cars_lst:
                cars_lst[car] = 0
            if w > 0.01:
                # print 'car: ' + car, 'wait time:' + str(w)
                cnt_waiting_cars += 1
                stepWaitingTime += w
                cars_lst[car] += 1
        print 'XX step:', step, 'stepWaitingTime:', stepWaitingTime, 'cnt_waiting_cars:', cnt_waiting_cars, 'avgWaitingTime:', stepWaitingTime / (
        cnt_cars + 0.001), 'cnt_cars:', cnt_cars

        traci.trafficlights.setRedYellowGreenState("0", algo.getNextProgram())
        step += 1

    # print 'YY seed:',options.seed,'title:',title,'Totals steps:', step, 'totalWaitingTime:',sum([cars_lst[x] for x in cars_lst.keys()]),'total_cnt_waiting_cars:',sum([1 for x in cars_lst.keys() if cars_lst[x]>0.01]),'total_cnt_cars:',len(cars_lst)
    print(
    "YY simulation: %-20s pace_factor: %2d seed: %d algo: %-16s Totals steps: %5d totalWaitingTime: %5d total_cnt_waiting_cars: %5d total_cnt_cars: %5d" % (
    options.simulation, options.pace_factor, options.seed, title, step, sum([cars_lst[x] for x in cars_lst.keys()]),
    sum([1 for x in cars_lst.keys() if cars_lst[x] > 0.01]), len(cars_lst)))
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    optParser.add_option("--algo", action="store", type="string", dest="algo", default='smartDelta')
    optParser.add_option("--greentime", action="store", type="float", dest="greentime", default=5)
    optParser.add_option("--seed", action="store", type="int", dest="seed", default=42)
    optParser.add_option("--steps", action="store", type="int", dest="steps", default=1000)
    optParser.add_option("--pace_factor", action="store", type="float", dest="pace_factor", default=1.0)
    optParser.add_option("--simulation", action="store", type="string", dest="simulation", default='simple_cross')
    options, args = optParser.parse_args()
    print options
    print args
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    print sumoBinary

    simulation = __import__("simulations.%s.build" % options.simulation,
                            fromlist=["simulations.%s" % options.simulation])

    # first, generate the route file for this simulation
    simulation.generate_routefile(options.seed, options.steps, options.pace_factor)

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    process_args = [sumoBinary, "-c", "simulations/%s/cross.sumocfg" % options.simulation, "--remote-port",
                    str(PORT)]
    print "Running SUMO:", " ".join(process_args)
    sumoProcess = subprocess.Popen(
        process_args, stdout=sys.stdout, stderr=sys.stderr)

    run(options, simulation)
    sumoProcess.wait()
