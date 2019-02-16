from flask import Flask, jsonify, send_from_directory, request
from multiping import multi_ping
from netmiko import ConnectHandler
from pprint import pprint
import re
import time

username = "admin"
password = "T$2z-artek"


clusters = {
    'audag': {
        'ip' : '10.55.15.140',
        'nodes': [],
    },
    'guest': {
        'ip' : '10.55.13.111',
        'nodes': [],
    },
    'boss': {
        'ip' : '172.16.13.222',
        'nodes': [],
    }
}


def parse_clusternodes(ip):
    cluster = {
        'device_type' : 'eltex',
        'ip':   ip,
        'username': username,
        'password': password, }
    
    raw_cn = ConnectHandler(**cluster).send_command(
    'get cluster-member detail').split('Property            Value\n''-------------------------------------\n')[1:]
    cluster_nodes = []
    node = {}
    for n in raw_cn:
        for params in n.split('\n'):
            p = params.split()
            if(len(p) > 1):
                node[p[0]] = p[1]
        cluster_nodes.append(node)
        node = {}
    return cluster_nodes

for key in clusters:
    clusters[key]['nodes'] = parse_clusternodes(clusters[key]['ip'])



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

@app.route('/<name>')
def get_cluster_nodes(name):
    nodes = clusters[name]['nodes'].copy()
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
    some_node = {
        'device_type' : 'eltex',
        'ip':   r["ip"],
        'username': username,
        'password': password, }
    raw_nodes = ConnectHandler(**some_node).send_command(
        'get association detail').split('Property               Value\n-----------------------------------------------\n')[1:]
    client_nodes = []
    node = {}
    for n in raw_nodes:
        for params in n.split('\n'):
            p = params.split()
            if(len(p) > 1):
                node[p[0]] = p[1]
        client_nodes.append(node)
        node = {}
    return jsonify(client_nodes)
