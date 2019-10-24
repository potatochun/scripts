import json
import datetime
import sys
import ipaddress
import pika

from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

app = Flask(__name__)

def checkTimeStamp(ts):
	try:
		(datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S'))
		app.logger.info('Timestamp %s is successfully inserted', ts)
	except ValueError:
	    abort(400, 'Provided timestamp {0} is not a valid Unix timestamp!'.format(ts))

def checkSender(sender):
	try:
		converted_sender = sender.encode('ascii','ignore')
		app.logger.info('Sender %s is successfully inserted', sender)
	except:
		abort(400, 'Something is wrong')

def checkMessage(message):
	#Verify message has at least one key/value pair
	if bool(message) == False:
		abort(400, 'Message field has empty objects')
	else:
		app.logger.info('Message %s is successfully inserted', message)

def checkIP(ip):
	try:
		new_ip = ipaddress.ip_address(ip)
		app.logger.info('IP address %s is successfully inserted', ipaddress)
	except ValueError:
		abort(400, 'Provided IP address is wrong')

def checkPriority(prio):
	if type(prio) != int:
		abort(400, 'Priority must be integer')
	else:
		app.logger.info('Priority %s is successfully inserted', prio)

def storeMessageinRMQ(payloads):
	credentials = pika.PlainCredentials('web-user1', 'webpassword')
	parameters = pika.ConnectionParameters('rmq','5672','web-vhost',credentials)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.basic_publish(exchange='webservice2-exchange', routing_key='valid',body=payloads)
	app.logger.info('Payload %s is successfully inserted', payloads)
	connection.close()

@app.route('/', methods=['GET'])
def indexs():
        return "Nothing to see here, this is the main site. Find something to do"
        
@app.route('/forjson', methods=['POST'])
def forjson():

	#check if requests are JSON format or not
	if request.headers['Content-Type'] == 'application/json':
		pass
	else:
	    abort(415, 'Unsupported Media Type')

	try:
		content = request.get_json()
	except:
		abort(400, 'JSON format is invalid')

	#Lame ways to verify if the payload contains valid keys and contents only
	#Possible way is to use jsonschema
	if content.viewkeys() == {'message', 'sender', 'ts', 'priority'}:
		checkTimeStamp(content.get('ts'))
		checkSender(content.get('sender'))
		checkMessage(content.get('message'))
		checkPriority(content.get('priority'))

	elif content.viewkeys() == {'message', 'sender', 'ts', 'priority', 'sent-from-ip'}:
		checkTimeStamp(content.get('ts'))
		checkSender(content.get('sender'))
		checkMessage(content.get('message'))
		checkIP(content.get('sent-from-ip'))
		checkPriority(content.get('priority'))
			
	else:
		abort(400, 'The request does not satisfy accepted fields(s) detected')

	app.logger.info("JSON payload contains valid fields")

	#Insert all fields into RabbitMQ messaging queue here
	message2 = json.dumps(content.items())
	storeMessageinRMQ(message2)

	return "Transaction successfully"


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug="True", port=80)
	#enable this for docker image
	#app.run(host="localhost", port=5000, debug="True")
