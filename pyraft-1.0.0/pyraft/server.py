import threading
from flask import Flask, request, jsonify
from pyraft import raft
import sys
import json
import time
import uuid

# Flask app initialization
app = Flask(__name__)

# call raft api to do one of set/get/del operations
def handleCreate(node, data):

    response = {}

    metatype = data.get('name', [])


    #only tow fields that need to be generated by server
    if(metatype=="RegisterBrokerRecord"):
        data['fields']['internalUUID'] = str(uuid.uuid4())

    if(metatype=="TopicRecord"):
        data['fields']['topicUUID'] = str(uuid.uuid4())

    data['timestamp'] = str(time.time())


    try:
        # node.propose(commands)
        recordData = json.loads(node.propose(['get', str(metatype)]))
        recordData['records'].append(data)
        recordData['timestamp'] = data['timestamp']
        recordData['len'] = str(int(recordData['len']+1))
        print(recordData)
        node.propose(['set', str(metatype), json.dumps(recordData)])
        response = {'success': True}
    except Exception as e:
        print("ERR! ", e)
        response = {'success': False, 'error': str(e)}

    return response

def provisionLog(node):
    recordTypes = ['RegisterBrokerRecord', 'TopicRecord', 'PartitionRecord', 'ProducerIdsRecord', 'RegistrationChangeBrokerRecord']
    for record in recordTypes:
        try:
            node.propose(['set', record, json.dumps({"records":[], "timestamp": "", "len": "0"})])
        except Exception as e:
            print("ERR! ", e) 

# Initialize the Raft node
node = raft.make_default_node()
node.start()
provisionLog(node)

# HTTP route to accept data and propose to the Raft network
@app.route('/propose', methods=['POST'])
def propose_data():
    data = request.json
    response = handleCreate(node, data)
    return jsonify(dict(response))

@app.route('/getlog', methods=['POST'])
def get_log():
    return jsonify(node.data)

# @app.route('/get-topic/<string:name>', methods=['GET'])
# def get_topic(name):
#     recordType="TopicRecord"
#     data=node.propose(['get', recordType])
#     final_data=node.propose(['get',data["records"][name]])
#     return jsonify({"data":final_data})

app.run(host='0.0.0.0', port=node.port-1)

node.join()