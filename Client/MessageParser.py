import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    'login': self.parse_login,
	    'logout': self.parse_logoff,
	    'history': self.parse_history,
	    'names': self.parse_names
	    'help': self.parse_help
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.load(payload)# decode the JSON object
	print payload

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
	    self.parse_error(payload)
            # Response not valid

    def parse_error(self, payload):
    	payload = json.load(payload)
	print payload

    def parse_info(self, payload):
	payload = json.load(payload)
	print payload

    def parse_login(self, payload):
	payload = json.load(payload)
	print payload

    def parse_logout(self, payload):
	payload = json.load(payload)
	print payload

    def parse_history(self, payload):
	payload = json.load(payload)
	print payload

    def parse_names(self, payload):
	payload = json.load(payload)
	print payload

    def parse_help(self, payload):
	payload = json.load(payload)
	print payload
    
    # Include more methods for handling the different responses... 
