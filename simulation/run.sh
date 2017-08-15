#!/usr/bin/env bash

basedir=$( cd $(dirname $0) ; pwd -P )
now=`date +"%Y_%m_%d_%H-%M-%S"`
#export PYTHONPATH=~/sumo/sumo-svn/tools
export SUMO_HOME=~/sumo/sumo-svn

cd $basedir
old_IFS=$IFS
IFS=$'\n'     # new field separator, the end of line           
for line in $(cat simulations.txt | grep -v "#")          
do          
	sim=$(echo $line | cut -f1)
	pace_factor=$(echo $line | cut -f2)
	algo=$(echo $line | cut -f3)
	greentime=$(echo $line | cut -f4)
	seed=$(echo $line | cut -f5)
	
	cd $basedir 
	mkdir -p $basedir/logs
	log_file=$basedir/logs/"$sim"_"$algo"_seed_"$seed"_time_"$now".log
#    echo python runner.py --simulation=$sim --greentime=$greentime --seed=$seed --algo=$algo --pace_factor=$pace_factor
	python runner.py --nogui --simulation=$sim --greentime=$greentime --seed=$seed --algo=$algo --pace_factor=$pace_factor > $log_file 2>&1
#	python runner.py --simulation=$sim --greentime=$greentime --seed=$seed --algo=$algo --pace_factor=$pace_factor > $log_file 2>&1
	grep "Totals" $log_file
	
done          
IFS=$old_IFS     # restore default field separator 

