from flask import Flask
from multiping import multi_ping
from netmiko import ConnectHandler
import re

username = "root"
password = "T$2z-artek"

audag = {
    'device_type' : 'eltex',
    'ip':   '10.55.15.140',
    'username': username,
    'password': password, }

#получаем список точек в кластере делим их на строки и удаляем первые
#три ненужные строки
audag_cn_raw = ConnectHandler(**audag).send_command(
    '/splashbin/get  cluster-member location ip mac firmware-version').split('\n')[2:]

audag_cluster_nodes = []
node = {} 
for n in audag_cn_raw:
   (node['name'], node['ip'], node['mac'], node['firmver']) = n.split()
   audag_cluster_nodes.append(node)
   

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

