
from MessageReceiver import MessageReceiver
import json

class MessageParser():
	def __init__(self):

		self.possible_responses = {
			'error': self.parse_error,
			'info': self.parse_info,
			'message': self.parse_message,
			'history': self.parse_history
			# More key:values pairs are needed	
		}

	def parse(self, payload):
		#payload = # decode the JSON object

		if payload['response'] in self.possible_responses:
			return self.possible_responses[payload['response']](payload)
		else:
			return 'Response not valid'

	def parse_error(self, payload):
		return '[Error]' + str(payload['content'])
	def parse_info(self, payload):
		return '[Server]' + str(payload['content'])
	def parse_message(self, payload):
		return '[' + str(payload['timestamp']) + ' by ' + str(payload['sender']) + '] ' + str(payload['content'])
	def parse_history(self, payload):
		history=''
		#The payloade will in this case consist of several json elements.
		#This is fiksed by recursion.
		for message in payload['content']:
			parser=MessageParser()
			history+=parser.parse(message) +'\n'
		return history
		# Include more methods for handling the different responses... 
