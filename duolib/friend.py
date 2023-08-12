from duo import *
from duosession import *
from friendbot import *
from os import system, getcwd 
import json
import threading
import time

MASS = "1"
RECENT = "2"
DELALL = "3"
FFF = "4"

def massCrawl():

	system("clear")
	i = input("Enter the ID to start crawling: ")
	bot = friendBot(i)
	bot.crawlUser(i)
	bot.option = MASS
	bot.start()

def recentlyActive():

	system("clear")
	i = input("Enter the ID to start crawling: ")
	bot = friendBot(i)
	bot.crawlUser(i)
	bot.option = RECENT
	bot.start()

def delAllFriends():

	system("clear")
	bot = friendBot()
	bot.option = DELALL
	bot.start()

def followForFollow():

	system("clear")
	bot = friendBot()
	bot.option = FFF
	bot.start()

def sessionCheck():

	path = getcwd() + "/session.json"

	if(exists(path)):

		ch = input("It looks like you have a previous session. Would you like to resume?(y/n) ")

		if(ch == "y"):

			bot = friendBot()
			bot.loadSession()

def menu():

	system("clear")
	sessionCheck()
	print("------------------------\nDuolingo SmartFriend Bot v2.0.1\n\nMain Menu\n------------------------\n")
	print("[1] Mass crawl and add\n[2] Add recently active users\n[3] Unadd friends all friends\n[4] Unadd friends who don't follow you\n\n")
	ch = input("Enter your choice: ")
	ch = str(ch)

	if(ch == "1"):
		massCrawl()
	elif(ch == "2"):
		recentlyActive()
	elif(ch == "3"):
		delAllFriends()
	elif(ch == "4"):
		followForFollow()

menu()


