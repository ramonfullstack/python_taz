GENERATE_BIN=$4

PYTHONBIN=python

if [[ "$GENERATE_BIN" = "true" ]]; then
    sudo mkdir -p /opt/taz
    sudo chown -R $(whoami) /opt/taz
    ln -sf $(which python) /opt/taz/python_taz
    PYTHONBIN=/opt/taz/python_taz
fi

$PYTHONBIN taz/main.py ${JOB_TYPE} ${SCOPE}
