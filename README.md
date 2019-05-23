# IP-Utilization-Monitor 說明

## 執行環境 Python3.6 virtualenv
sudo yum install centos-release-scl
sudo yum install rh-python36
scl enable rh-python36 bash
mkdir /home/logicalis/IP-Utilization-Monitor/
mkdir /home/logicalis/IP-Utilization-Monitor/IP-Utilization-Monitor/
python -m venv /home/logicalis/IP-Utilization-Monitor/IP-Utilization-Monitor/
source /home/logicalis/IP-Utilization-Monitor/IP-Utilization-Monitor/bin/activate

pip install --upgrade pip
pip install pandas tqdm requests lxml