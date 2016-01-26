import commands
from utilities import is_registered


def reply_ping(bot, data):
	data_split = data.split()
	bot.send_message('PONG ' + data_split[1])
	bot.ping_count += 1


def reply_authenticate(bot, data):
	bot.send_message('PASS :' + bot.nickpass)
	bot.send_message('NICK ' + bot.nick)
	bot.send_message('USER ' + bot.nick + ' 0 ' + bot.host + ' :' + bot.ident)


def reply_privmsg(bot, data):
	data_split = data.split()
	user = data_split[0][1:]
	nick = user.split('!')[0]
	channel = data_split[2]
	message = ' '.join([data_split[3][1:]] + data_split[4:])
	if message[0] == bot.trigger and len(message) > 1:
		if channel == bot.nick:
			channel = nick
		command = message.split()[0][1:].lower()
		if command in bot.owner_command_list:
			registered = is_registered(bot, nick)
		else:
			registered = False
		try:
			getattr(commands, 'comm_' + command)(bot, registered, nick, channel, message)
		except AttributeError, ex:
			print ex


def reply_notice(bot, data):
	pass
	# print "Received Notice: " + data)


def reply_001(bot, data):
	for channel in bot.channels:
		bot.send_message('JOIN ' + channel)


def reply_error(bot, data):
	print data


def reply_002(bot, data):
	pass


def reply_003(bot, data):
	pass


def reply_004(bot, data):
	pass


def reply_005(bot, data):
	pass


def reply_250(bot, data):
	pass


def reply_251(bot, data):
	pass


def reply_252(bot, data):
	pass


def reply_253(bot, data):
	pass


def reply_254(bot, data):
	pass


def reply_255(bot, data):
	pass


def reply_265(bot, data):
	pass


def reply_266(bot, data):
	pass


def reply_332(bot, data):
	pass


def reply_333(bot, data):
	pass


def reply_336(bot, data):
	pass


def reply_353(bot, data):
	pass


def reply_366(bot, data):
	pass


def reply_372(bot, data):
	pass


def reply_375(bot, data):
	pass


def reply_376(bot, data):
	pass


def reply_401(bot, data):
	pass


def reply_900(bot, data):
	pass


def reply_903(bot, data):
	pass


def reply_join(bot, data):
	pass


def reply_mode(bot, data):
	pass


def reply_part(bot, data):
	pass


def reply_quit(bot, data):
	pass


def reply_invite(bot, data):
	pass


def reply_nick(bot, data):
	pass
