running in the docker container:


ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
xhost + $ip
docker rm -f $(docker ps -aq)
docker run -it --name sumo -e DISPLAY=$ip:0 --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v /Users/oraviv/git/trafficlight/simulation:/opt/sumo-sim docker-sumo

running sumo examples:

python2.7 /opt/sumo-sim/runner.py --nogui --simulation=raul_valenberg_habarzel --greentime=1.0 --seed=42 --algo=static --pace_factor=1
/opt/sumo/bin/sumo-gui -c /opt/sumo-sim/simulations/raul_valenberg_habarzel/cross.sumocfg --remote-port 8873
