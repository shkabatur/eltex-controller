from flask import Flask, jsonify, send_from_directory
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
   node = {}
   

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
   return send_from_directory('templates', 'index.html')


@app.route('/audag')
def hello_world():
    return jsonify(audag_cluster_nodes)

