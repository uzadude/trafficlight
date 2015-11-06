basedir=$(dirname $0)
now=`date +"%Y_%m_%d_%H-%M-%S"` 
export PYTHONPATH=/home/ohad/code/trafficlight/sumo-0.24.0/tools

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
	python runner.py --nogui --simulation=$sim --greentime=$greentime --seed=$seed --algo=$algo --pace_factor=$pace_factor > $log_file 2>&1
	cd logs
	grep "Totals" $log_file
	
done          
IFS=$old_IFS     # restore default field separator 


#cd $basedir 
#log_file=$basedir/logs/run_"$now".log
#./runner.py --nogui --algo=smartDelta "$@"> $log_file 2>&1
#cd logs
#grep "Totals" $log_file
#
#cd $basedir 
#log_file=$basedir/logs/run_"$now".log
#./runner.py --nogui --algo=smart "$@"> $log_file 2>&1
#cd logs
#grep "Totals" $log_file
#
# statics
#for t in {5,10,15,20,30}; do 
#	cd $basedir 
#	log_file=$basedir/logs/run_"$now".log
#	./runner.py --nogui --algo=static --greentime=$t "$@"> $log_file 2>&1
#	cd logs
#	grep "Totals" $log_file 
#done
