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
    '/splashbin/get  cluster-member location ip mac firmware-version compat').split('\n')[3:]

audag_cluster_nodes = []
node = {} 
for n in audag_cn_raw:
   print(n.split)
   node['name'], node['ip'], node['mac'], node['firmver'], node['model'] = n.split()
   audag_cluster_nodes.append(node)
   node = {}
   

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
   return send_from_directory('templates', 'index.html')


@app.route('/audag')
def hello_world():
    #копируем в переменную nodes точки в кластере 
    nodes = audag_cluster_nodes.copy()
    #создаем массив с ip'шниками для multi_ping
    ips = [ n['ip'] for n in nodes]
    resp, no_resp = multi_ping(ips, timeout=2, retry=3)
    for n in nodes:
       if n['ip'] in resp:
          n['ping'] = resp[n['ip']] * 1000
          n['status'] = True
       else:
          n['ping'] = 9999
          n['status'] = False
    return jsonify(nodes)

