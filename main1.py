from flask import Flask, jsonify, send_from_directory, request
from multiping import multi_ping
from netmiko import ConnectHandler
from pprint import pprint
import re
import time

username = "admin"
password = "T$2z-artek"

audag = {
    'device_type' : 'eltex',
    'ip':   '10.55.15.140',
    'username': username,
    'password': password, }

guest = {
   'device_type' : 'eltex',
   'ip':   '10.55.13.111',
   'username': username,
   'password': password, }

#получаем список точек в кластере делим их на строки и удаляем первые
#три ненужные строки


guest_cn_raw = ConnectHandler(**guest).send_command(
   'get cluster-member location ip mac firmware-version').split('\n')[2:]


audag_cn_raw = ConnectHandler(**audag).send_command(
   'get cluster-member location ip mac firmware-version compat').split('\n')[2:]



audag_cluster_nodes = []
guest_cluster_nodes = []

node = {} 
for n in guest_cn_raw:
   node['name'], node['ip'], node['mac'], node['firmver'] = n.split()
   guest_cluster_nodes.append(node)
   node = {}

node = {} 
for n in audag_cn_raw:
   node['name'], node['ip'], node['mac'], node['firmver'], node['model'] = n.split()
   audag_cluster_nodes.append(node)
   node = {}
pprint(guest_cluster_nodes)
   

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
   return send_from_directory('templates', 'index.html')

@app.route('/reboot', methods=['POST'])
def reboot():
   r = request.get_json()
   print("reboot this node: ",r)
   node_to_reboot = {
      'device_type' : 'eltex',
      'ip': r['ip'],
      'username' : username,
      'password' : password,
   }
   connect_handler = ConnectHandler(**node_to_reboot).send_command('reboot')
   return str(r)

@app.route('/audag')
def get_audag():
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

@app.route('/guest')
def get_guest():
    #копируем в переменную nodes точки в кластере 
    nodes = guest_cluster_nodes.copy()
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

@app.route('/detail',methods=['POST'])
def get_detail():
   r = request.get_json()
   node = {
   'device_type' : 'eltex',
   'ip':   r["ip"],
   'username': username,
   'password': password, }
   print(r["ip"])
   return jsonify({"ip":r["ip"]})
