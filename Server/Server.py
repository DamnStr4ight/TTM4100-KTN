# -*- coding: utf-8 -*-
import SocketServer
import json
import re
import time
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
onlineUsers = set()
history = []

class ClientHandler(SocketServer.BaseRequestHandler):

	def handle(self):
       	"""
       	This method handles the connection between a client and the server.
       	"""
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request
		self.user = None

		self.possible_requests = {
			'login': self.login,
			'logout': self.logout,
			'msg': self.message,
			'history': self.history,
			'users': self.users,
			'help': self.help
		}
		# Loop that listens for messages from the client	
		while True:
	    	received_string = self.connection.recv(4096)
            
            # TODO: Add handling of received payload from client


	def history(self):
		if self.user not in onlineUsers:
			self.error('Access denied. Not logged in')
		else:
			payload = {'timestamp': datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'sender': [Server],'response': 'history','content': history }


	def login(self, recieved_msg):
		if re.match("^[A-Za-z0-9_-]+$", recieved_msg['content']):
			self.user = recieved_msg['content']
			print(self.user, 'logged in')
			self.history(recieved_msg)
			msg = {'timestamp': datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'sender': [Server],'response': 'info','content': self.user + 'connected'}
			payload = json.dumps(msg)
			for user in onlineUsers:
				user.send_payload(payload)
			history.append(msg)

	def logout(self):
		if self.user not in onlineUsers:
			self.error('Invalid request. Not logged in')
		else:
			msg = {'timestamp': datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),'sender': [Server],'response': 'info','content': self.user + 'logged out'}
			payload = json.dumps(msg)
			for user in onlineUsers:
				user.send_payload(payload)
			onlineUsers.remove(self)
			self.connection.close()
			history.append(msg)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
	allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
	HOST, PORT = 'localhost', 9998
	print 'Server running...'

    # Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever()
