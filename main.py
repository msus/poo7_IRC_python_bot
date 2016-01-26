#!/usr/bin/env python
import sys
import socket
import time
import replies
from utilities import CRLF


class Bot:

	def __init__(self, host, port, nick, ident, nickpass, owners):

		self.host = host
		self.port = port
		self.nick = nick
		self.ident = ident
		self.nickpass = nickpass
		self.owners = owners
		self.connection = None
		self.trigger = '!'
		self.channels = ['#bots']  # , '#fuzer']
		self.owner_command_list = ['join', 'part', 'quit']
		self.ping_count = 0

	def connect(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.connection.connect((self.host, self.port))
			replies.reply_authenticate(self, '')
		except Exception, ex:
			print "Connection failed:"
			print ex.message
			sys.exit()
		self.run()

	def run(self):
		data = ""
		while True:
			try:
				data += self.connection.recv(1024)
			except KeyboardInterrupt, ex:
				print ex.message
				sys.exit()
			if data:
				while data.find(CRLF) != -1:
					index = data.find(CRLF)
					data_in = data[:index]
					self.input_received(data_in)
					data = data[(index + len(CRLF)):]

	def input_received(self, data_in):
		input_split = data_in.split()
		if input_split[0] == 'PING':
			reply = 'reply_ping'
		elif input_split[0] == 'ERROR':
			reply = 'reply_error'
		elif input_split[0] == 'AUTHENTICATE':
			reply = 'reply_authenticate'
		else:
			reply = "reply_" + str(input_split[1]).lower()
		if reply != 'reply_ping':
			print "recv<<< ", data_in
		try:
			getattr(replies, reply)(self, data_in)
		except AttributeError, ex:
			print ex.message

	def send_message(self, message):
		print "send>>>", message
		message += CRLF
		self.connection.send(message)
		time.sleep(0.310)


if __name__ == '__main__':
	poo = Bot('irc.fuzer.me', 6667, 'poo7', 'poo7', '*****PSWWD****', ['boo7', 'Salem'])
	try:
		poo.connect()
	except:
		print "interrupt"
		print sys.exc_info()[0]
		raise
