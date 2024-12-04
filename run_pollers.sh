#!/bin/sh
if [ ! -f /opt/taz/python_taz ]; then
    sudo mkdir -p /opt/taz
    sudo chown -R $(whoami) /opt/taz
    ln -sf $(which python) /opt/taz/python_taz
fi

export JOB_TYPE='poller'

export PYTHONPATH=$(pwd) 

tmux new-session -d -s taz_pollers
tmux send-keys "PYTHONPATH=${PYTHONPATH}; make run environment=development jobtype=poller scope=category generate_binary=false" C-m
tmux split-window -h
tmux send-keys "PYTHONPATH=${PYTHONPATH}; make run environment=development jobtype=poller scope=media generate_binary=false" C-m
tmux select-pane -t 0
tmux split-window -v
tmux send-keys "PYTHONPATH=${PYTHONPATH}; make run environment=development jobtype=poller scope=factsheet generate_binary=false" C-m
tmux select-pane -t 2
tmux split-window -v
tmux send-keys "PYTHONPATH=${PYTHONPATH}; make run environment=development jobtype=poller scope=price generate_binary=false" C-m
tmux select-pane -t 0
tmux split-window -h
tmux send-keys "PYTHONPATH=${PYTHONPATH}; make run environment=development jobtype=poller scope=product generate_binary=false" C-m
tmux select-pane -t 0
tmux -2 attach-session -t taz_pollers
tmux send-keys "PYTHONPATH=${PYTHONPATH}; make run environment=development jobtype=poller scope=video generate_binary=false" C-m
tmux select-pane -t 0
tmux -2 attach-session -t taz_pollers
