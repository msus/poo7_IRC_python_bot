import os
import re
import requests
from urlparse import urlparse
from lepl.apps.rfc3696 import HttpUrl

CRLF = '\r\n'

path = os.path.dirname(os.path.abspath(__file__))
banlist = []
bookmark_file = open(path + '/bookmark.html', 'r')
bookmark_file = bookmark_file.read().splitlines()
songoffer_file = open(path + '/songoffer.html', 'r')
songoffer_file = songoffer_file.read().splitlines()


validator = HttpUrl()


def valid_url(url):
	url = url.replace('https', 'http')
	if is_ip(url):
		return True
	return validator(url)


def is_ip(url):
	regex = "\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b"
	searchobj = re.findall(regex, url, re.M | re.I)
	if searchobj:
		return True
	return False


def base_site(url):
	temp = urlparse(url)
	for i in temp:
		if is_ip(i):
			return i
	return temp[1]


def url_from(url):
	if valid_url(url):
		if is_ip(url):
			ip_address = base_site(url)
		else:
			ip_address = requests.get('http://api.konvert.me/forward-dns/' + base_site(url)).content
		country = requests.get('http://api.konvert.me/ip-country/' + ip_address).content
		city = requests.get('http://api.konvert.me/ip-city/' + ip_address).content.replace('\n', ' ')
		if not city == '   ':
			return "%s is from %s, %s" % (url, country, city)
		return "%s is from %s " % (url, country)
	return 'Invaild link!.. Hen Tal broke the internet.'


def is_registered(bot, nick):
	bot.send_message(str('PRIVMSG NickServ :STATUS ' + nick))  # ###
	data = bot.connection.recv(128)
	print "is_registered reply: ", data.strip()
	if data.find(':STATUS') != -1:
		if data.split(':STATUS')[1].split()[1] == '3':
			return True
	return False
