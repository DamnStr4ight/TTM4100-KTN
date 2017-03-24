# -*- coding: utf-8 -*-
import socketserver as SocketServer
import json
import re
import time
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
onlineUsers = set()
connectedUsers = []
history = []


class ClientHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		"""
       		This method handles the connection between a client and the 			server.
		"""
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request
		self.user = None

		connectedUsers.append(self)

		self.possible_requests = {
			'login': self.login,
			'logout': self.logout,
			'msg': self.message,
			'history': self.history,
			'names': self.names,
			'help': self.help
		}

		
		# Loop that listens for messages from the client	
		while True:
			received_msg =json.loads(self.connection.recv(4096).decode('utf-8'))
			print(received_msg)

			if received_msg['request'] in self.possible_requests:
				self.possible_requests[received_msg['request']](received_msg)
			else:
				self.error('Invalid request')	
            


	def history(self, received_msg):
		if self.user not in onlineUsers:
			self.error('Access denied strongly. Not logged in')
		else:
			payload = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M'),'sender': ['Server'],'response': 'history','content': print(*history,sep='\n')}



	def login(self, received_msg):
		if re.match("^[A-Za-z0-9_-]+$", received_msg['content']):
			self.user = received_msg['content']
			onlineUsers.add(self.user)
			print(self.user, 'logged in')
			self.history(received_msg)
			msg = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'sender': ['Server'],'response': 'info','content': self.user + ' connected'}
			payload = json.dumps(msg)
			for user in connectedUsers:
				user.send_payload(payload)
			history.append(msg)

	def logout(self, received_msg):
		if self.user not in onlineUsers:
			self.error('Invalid request. Not logged in')
		else:
			msg = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M'),'sender': ['Server'],'response': 'info','content': self.user + 'logged out'}
			payload = json.dumps(msg)
			for user in connectedUsers:
				user.send_payload(payload)
			onlineUsers.remove(self.user)
			self.connection.close()
			history.append(msg)

	def message(self, received_msg):
		if self.user not in onlineUsers:
			self.error('Invalid request. Not logged in')
		else:
			msg = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M'),'sender': [self.user],'response': 'message','content': received_msg['content']}
			payload = json.dumps(msg)
			for user in connectedUsers:
				user.send_payload(payload)
			history.append(msg)


	def names(self, received_msg):
		if self.user not in onlineUsers:	
			self.error('Invalid request. Not logged in')
		else:
			names = ""
			for user in connectedUsers:
				names += user.user
			msg = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M'),'sender': ['Server'],'response': 'info','content': names}
			payload = json.dumps(msg)
			self.send_payload(payload)


	def help(self, reveived_msg):
		help_box = 'These commands are available:\n{login username}:Grants access to the chat service\n{msg message}: Writes a post on the main board\n{help}: Shows valid commands\n{history}: Shows a log over all posts on the main board, their posters, and the time of posting\n{names}: Shows allusers currently online\n{logout}: logs out of the chat service'
		msg = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M'),'sender': [self.user],'response': 'info','content': help_box}
		payload = json.dumps(msg)
		self.send_payload(payload)

	def send_payload(self, data):
		self.connection.send(bytes(data, 'UTF-8'))

	def error(self, msg):
		msg = {'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M'),'sender': [],'response': 'error','content': msg}
		payload = json.dumps(msg)
		self.send_payload(payload)
		

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

	allow_reuse_address = True

if __name__ == "__main__":

	HOST, PORT = '', 9998
	print('Server running...')

	# Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever()
