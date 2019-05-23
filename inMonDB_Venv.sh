#! /bin/bash
cd /home/logicalis/IP-Utilization-Monitor
source IP-Utilization-Monitor/bin/activate

# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

echo "開始執行 ./inMonDB.py" >> ./LOGS/IP-Utilization-Monitor.$(date +"%Y%m%d").log
python -u ./inMonDB.py >> ./LOGS/IP-Utilization-Monitor.$(date +"%Y%m%d").log
deactivate