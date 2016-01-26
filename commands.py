import os
import re
import urllib2
import requests
from random import randint
from utilities import path, banlist, bookmark_file, songoffer_file, url_from


def comm_say(bot, registered, nick, channel, message):
	bot.send_message('PRIVMSG ' + channel + ' :' + nick + ' STFU')


def comm_stats(bot, registered, nick, channel, message):
	msg = "PRIVMSG  %s :%s: uptime is: %s minuts, " % (channel, nick, ((bot.ping_count * 123) / 60))
	if bookmark_file:
		msg = "%s, song repository size: %s" % (msg, len(bookmark_file))
	if os.name == 'posix':
		temp = os.popen('vcgencmd measure_temp').readline().split('=')[1]
		msg = "%s , temp of %s's CPU is: %s " % (msg, bot.nick, temp)
	bot.send_message(msg)


def comm_join(bot, registered, nick, channel, message):
	pre_msg = 'PRIVMSG ' + channel + ' :' + nick + ': '
	if not registered:
		bot.send_message(pre_msg + 'You.. ain\'t.. in the system :S')
		return None
	message = message.split()
	if len(message) <= 1:
		bot.send_message(pre_msg + 'Argumennt error. -Usage: !join <channel name>')
		return None
	for owner in bot.owners:
		if owner == nick:
			bot.send_message('JOIN ' + message[1])
			return None
	bot.send_message(pre_msg + 'Access denied.')
	return None


def comm_part(bot, registered, nick, channel, message):
	pre_msg = 'PRIVMSG ' + channel + ' :' + nick + ': '
	if registered:
		message = message.split()
		if len(message) > 1:
			for owner in bot.owners:
				if owner == nick:
					if len(message) == 2:
						bot.send_message('PART ' + message[1] + ' :Cya')
						return None
					bot.send_message('PART ' + message[1] + ' :' + ' '.join(message[2:]))
					return None
			bot.send_message(pre_msg + 'Access denied.')
			return None
		bot.send_message(pre_msg + 'Argumennt error. -Usage: !part <channel name>')
		return None
	bot.send_message(pre_msg + 'You.. ain\'t.. in the system :S')


def comm_quit(bot, registered, nick, channel, message):
	pre_msg = 'PRIVMSG ' + channel + ' :' + nick + ': '
	if registered:
		message = message.split()
		if len(message) > 1:
			for owner in bot.owners:
				if owner == nick:
					if len(message) == 2:
						bot.send_message('QUIT ' + message[1] + ' :Cya')
						return None
					bot.send_message('QUIT ' + message[1] + ' :' + ' '.join(message[2:]))
					return None
			bot.send_message(pre_msg + 'Access denied.')
			return None
		bot.send_message(pre_msg + ' Argumennt error. -Usage: !part <channel name>')
		return None
	bot.send_message(pre_msg + 'You.. ain\'t.. in the system :S')


def comm_song(bot, registered, nick, channel, message):
	while True:
		if len(banlist) == 220:
			del banlist[:]
		intt = randint(0, len(bookmark_file) - 1)
		if intt not in banlist:
			banlist.append(intt)
			bot.send_message('PRIVMSG ' + channel + ' :Song no.#' + str(intt) + ' ' + bookmark_file[intt])
			return None


def comm_songoffer(bot, registered, nick, channel, message):
	if len(message) == 1:

		count = 0
		for line in songoffer_file:
			if line:
				if line.split('@')[0] == nick:
					count += 1
		if count >= 15:
			bot.send_message('PRIVMSG ' + channel + ' :' + nick + ': You mad bro?')
			return None
		if message.find('youtube.com/watch?') != -1 and message.find('v=') != -1:
			my_file = open(path + '/songoffer.html', 'a')
			my_file.write(nick + '@' + channel + ' ' + ' '.join(message.split()[1:]) + ' </br>\n')
			my_file.close()
			bot.send_message('PRIVMSG ' + channel + ' :' + nick + ': Your suggestion received and will be considered.')
			return None
	bot.send_message('PRIVMSG ' + channel + ' :' + nick + ': Argument error. Usage: !songoffer <You0,4Tube_link>')
	return None


def comm_commands(bot, registered, nick, channel, message):
	helpmsg = '''
: Available commands at the moment:
3!say,
4!join,
4!part,
4!quit,
3!bothelp,
3!song,
3!songoffer,
3!geoip,
3!loto
'''
	bot.send_message('PRIVMSG ' + channel + ' :' + nick + ': ' + helpmsg.replace('\n', ' '))
	return None


def comm_geoip(bot, registered, nick, channel, message):
	if len(message.split()) != 1:
		url = message.split()[1]
		msg = url_from(url)
		bot.send_message('PRIVMSG %s :%s: %s' % (channel, nick, msg))
		return None
	bot.send_message('PRIVMSG %s :%s: Argumennt error. -Usage: !geoip <domain\IP>' % (channel, nick))
	return None


def comm_loto(bot, registered, nick, channel, message):
	response = urllib2.urlopen("http://api.thingspeak.com/apps/thinghttp/send_request?api_key=IZW7S6NXRTZTGLGH")
	page_source = response.read()
	searchobj = re.findall(r'>\d\w*<|\s\d{4}\s|\d{1,2}/\d{1,2}/\d{4}|\d{2}:\d{2}', page_source, re.M | re.I)
	string = ''
	for i in range(len(searchobj)):
		if 2 < i < 8:
			string += searchobj[i].strip('><') + ', '
		elif i == 8:
			string += searchobj[i].strip('><')
	date = searchobj[1] + ' '
	date += searchobj[2]
	msg = 'PRIVMSG %s :Wining lottory numbers for lotto no.#%s that took place at:%s are: %s and the strong number of: %s'\
		% (channel, searchobj[0].strip(" \r\n"), date, string, searchobj[9].strip('><'))
	bot.send_message(msg)
	return None
