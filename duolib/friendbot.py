from duo import *
from duosession import *
from ai import *
from os import system
import json
import threading
import time


class friendBot:

	session = duoSession()
	ids = [  ] #Store IDs of crawled profiles
	friends = [  ] #Store IDs of added friends
	whitelist = [ "0" ]
	option = ""

	W  = '\033[0m'  # white (normal)
	R  = '\033[31m' # red
	G  = '\033[32m' # green
	O  = '\033[33m' # orange
	B  = '\033[34m' # blue
	P  = '\033[35m' # purple

	def __init__(self, id="0"):

		self.user = self.session.getUserId() #Your user ID
		self.ids = [str(id)]
		self.friends = [str(id)]

	def saveSession(self):

		f = open("session.json", "w")
		data = json.dumps({'loadedCrawls':self.ids, 'loadedFriends':self.friends, 'scanType':self.option})
		f.write(data)
		f.close()

	def loadSession(self):

		f = open("session.json")
		data = json.load(f)
		f.close()

		self.option = data['scanType']
		self.ids = data['loadedCrawls']
		self.friends = data['loadedFriends']

		self.start()

	def idsAppend(self, id):

		#I learned the hard way that you don't want a trillion duplicates, it tends to crash the system
		dupid = False
		dupfri = False

		for x in self.ids:

			if(str(x) == str(id)):
				dupid = True 
			else:
				continue
		
		for x in self.friends:

			if(str(x) == str(id)):
				dupfri = True
			else:
				continue

		if(dupid == False):

			self.ids.append(id)	

		if(dupfri == False):

			self.friends.append(id)


	def crawlUser(self, id):

		print("Crawling ID ["+str(id)+"]")
		
		#Varibales of URLS
		followers = "https://www.duolingo.com/2017-06-30/users/"+str(id)+"/subscribers"
		following = "https://www.duolingo.com/2017-06-30/users/"+str(id)+"/subscriptions"

		try:
			#Get the follower data
			resp = self.session.authRequest(followers, "GET")
			resp = json.loads(resp)
			
			#Enumerate followers and store them in the "ids" list variable
			for id in resp['subscribers']:
			
				self.idsAppend(str(id['id']))

			#Get the following list
			resp = self.session.authRequest(following, "GET")
			resp = json.loads(resp)

			#Enumerate and store in "ids" list for later crawling
			for id in resp['subscriptions']:

				self.idsAppend(str(id['id']))
		
		except RuntimeError as e:

			logError(e, id)
		

	#2 hours in, I figured out there's a secret token passed other than csrf. Lots of 403 errors
	def addFriend(self, id):
			
		add = "https://www.duolingo.com/2017-06-30/users/"+self.user+"/subscriptions/"+str(id)
		cookie = self.session.getCookie()
		data = {'csrfToken':str(cookie['csrf_token'])}
		resp = self.session.authRequest(add, "PUT", params=data)

		if(resp == 200):

			saveFriendToDatabase(id)
			print(self.G+"["+str(resp)+"] Added user ["+str(id)+"] as a friend"+self.W)

		else:

			print(self.R+"["+str(resp)+"] Unable to add user "+str(id)+self.W)

	#Mom I don't need friends
	def delFriend(self, id):

		try:

			print("Removing user ["+str(id)+"] from subscriptions")
			cookie = self.session.getCookie()
			token = cookie['csrf_token']
			delete = "https://www.duolingo.com/2017-06-30/users/"+user+"/subscriptions/"+str(id)+"?csrfToken="+str(token)
			resp = self.session.authRequest(delete, "DELETE")
			deleteFriendFromDatabase(id)

		except Exception as e:

			err = str(e)+" CODE: "+resp
			logError(e, id)

	def hasRecentActivity(self, id):

		try:

			data = extractUserDataByID(id)
			data = json.loads(data)
			user = data['users'][0]

			if(str(user['hasRecentActivity15']) == "false"):

				return False

			elif(str(user['hasRecentActivity15']) == "true"):

				return True

		except Exception as e:

			logError(e, id)

	def friendWorker(self):

		while 1:

			if(str(self.option) == "1"):
				
				for x in self.friends:
					
					ai = botAI(x)
					if(ai.calculateUserScore() == True):
						
						self.addFriend(x)
						self.friends.remove(str(x))

					else:

						print("ID [%s] does not meet minimum score [%s]/[%s]" % (x, str(ai.total), ai.getPassingScore()))
						self.friends.remove(str(x))

					del ai

			elif(str(self.option) == "2"):

				for x in self.friends:

					ai = botAI(x)

					if(ai.calculateUserScore() == True and self.hasRecentActivity(str(x)) == True):
						
						time.sleep(5)
						self.addFriend(x)
						self.friends.remove(str(x))
					
					else:

						print("ID [%s] does not meet minimum score [%s]/[%s]" % (x, str(ai.total), ai.getPassingScore()))
						self.friends.remove(str(x))

					del ai 

	def crawlWorker(self):

		#This function will be ran by the crawler thread
		for x in self.ids:

			self.crawlUser(x)
			self.ids.remove(str(x)) #Again... little memory as possible
			self.saveSession()

	def unfriendWorker(self):

		system("clear")
		print("Starting unfriend worker...")

		if(self.option == "3"):

			try:
				print("Loading whitelist...")
				f = open("whitelist.txt", "r")

				for line in f:

					self.whitelist.append(line)

				following = "https://www.duolingo.com/2017-06-30/users/"+self.user+"/subscriptions/"
				resp = self.session.authRequest(following, "GET")
				json = json.loads(resp)

				for user in json['subscriptions']:

					self.friends.append(user['id'])

				for x in self.friends:

					for i in whitelist:

						if(x == i):
							self.friends.remove(x)
						else:
							continue

				for x in self.friends:

					delFriend(x)
					self.friends.remove(x)
					print(self.G+"["+str(x)+"] has been deleted!"+self.W)

			except Exception as e:
				logError(e, x)

		elif(self.option == "4"):

			try:

				followers = ["0"]
				following = ["0"]

				foll = "https://www.duolingo.com/2017-06-30/users/"+self.user+"/subscribers"
				following = "https://www.duolingo.com/2017-06-30/users/"+self.user+"/subscriptions"

				print("Loading your followers...")
				resp = self.session.authRequest(followers, "GET")
				resp = json.loads(resp)
				
				for id in resp['subscribers']:
				
					followers.append(id)

				print("Loading your subscriptions...")
				resp = self.session.authRequest(following, "GET")
				resp = json.loads(resp)

				for id in resp['subscriptions']:

					following.append(id)

				for x in following:

					for i in followers:

						if(i == x):

							following.remove(i)

				for x in following:

					delFriend(x)
					following.remove(x)
					print(self.G+"["+str(x)+"] doesn't follow you and has been deleted!"+self.W)

			except Exception as e:

				logError(e, x)

		print("Done!")

	def start(self):

		system("clear")
		if(str(self.option) == "1" or str(self.option) == "2"):

			try:

				#We start two threads so that the script will simutaneously crawl and add
				t1 = threading.Thread(target=self.crawlWorker)
				t2 = threading.Thread(target=self.friendWorker)
				t1.start()
				t2.start()

				t1.join()
				t2.join()

			except:

				print("Error: unable to start thread")

		elif(str(self.option) == "3" or self.option == "4"):

			unfriendWorker()


