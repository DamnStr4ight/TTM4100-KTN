# -*- coding: utf-8 -*-
import socket,sys,codecs,json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
	"""
	This is the chat client class
	"""

	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""

		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
		# TODO: Finish init process with necessary code
		self.host = host
		self.server_port = server_port
		self.run()

		def run(self):
		# Initiate the connection to the server
			self.connection.connect((self.host, self.server_port))
			self.thread= MessageReciever(self, self.connect)
			self.thread.start()
			while True:
				txt = input().split(' ',1)#Split on first space
				if(len(txt) > 0 and len(txt) < 3): # Dont accept more than 2 arguments
					if(len(txt)==1):
						txt.append('')#What if short input?
					if(txt[0]=='login'):
						payload=json.dumps({'request': 'login', 'content':text[1]})
						self.send_payload(payload)
						break;
					elif(txt[0]=='msg'):
						payload=json.dumps({'request': 'msg', 'content':text[1]})
						self.send_payload(payload)
						break;
					elif(txt[0]=='names'):
						payload=json.dumps({'request': 'names', 'content':text[1]})
						self.send_payload(payload)
						break;
					elif(txt[0]=='logout'):
						payload=json.dumps({'request': 'logout', 'content':text[1]})
						self.send_payload(payload)
						break;
					elif(txt[0]=='help'):
						payload=json.dumps({'request': 'help', 'content':text[1]})
						self.send_payload(payload)
						break;
					elif(txt[0]=='history'):
						payload=json.dumps({'request': 'history', 'content':text[1]})
						self.send_payload(payload)
						break;
					else:
						print('Oh oh! No such command, type "help" to see all possible commands')
					}
				else:	
					print('Oh oh! No such command, type "help" to see all possible commands')
					



	def disconnect(self):
		# TODO: Handle disconnection
		payload=jason.dumps({'Request': 'logout'})
		self.send_payload(payload)
		print('Sorry to see you go!')
		sys.exit() #Exit the program.

	def receive_message(self, message):
		# TODO: Handle incoming message
		parser=MessageParser()
		parsed_message=parser.parse(message)
		print(parsed_message,'\n> ',end='')

	def send_payload(self, data):
		# TODO: Handle sending of a payload
		self.connection.send(bytes(data, 'uft-8'))
		# More methods may be needed!


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""
	server_ip=input('Please enter the IP of the server you wish to join: ')
	print('Welcome to Top dank 420 blazeit max cancer chat 2017! Type "login <username> to log in!','\n> ',end='')
	client = Client(server_ip, 9998)
