#! /bin/bash
# gunicorn 開機啟動
cd /home/logicalis/IP-Utilization-Monitor
source IP-Utilization-Monitor/bin/activate
gunicorn -w 2 -b 0.0.0.0:9016 Search_Host:app -D