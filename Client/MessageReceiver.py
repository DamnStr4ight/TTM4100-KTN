# -*- coding: utf-8 -*-
import json
from threading import Thread
class MessageReceiver(Thread):
	"""
	This is the message receiver class. The class inherits Thread, something that
	is necessary to make the MessageReceiver start a new thread, and it allows
	the chat client to both send and receive messages at the same time
	"""

	def __init__(self, client, connection):
		"""
		This method is executed when creating a new MessageReceiver object
		"""

		Thread.__init__(self)
		# Flag to run thread as a deamon
		self.daemon = True
		self.stop=False
		self.connection = connection
		self.client = client

		# TODO: Finish initialization of MessageReceiver

	def run(self):
		# TODO: Make MessageReceiver receive and handle payloads
		# While we have not yet recieved a logout, run
		while not  self.stop:
			msg= self.connection.recv(4096).decode('utf-8')
			if not msg:
				break
			else:
				self.client.receive_message(json.loads(msg))
