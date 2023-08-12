from duo import *
from duosession import *
from os import system
import json
import threading
import time

session = duoSession() #We're creating an object using the session class we created
ids = [] #Store IDs of crawled profiles
friends = [] #Store IDs of added friends
user = session.getUserId() #Your user ID


def idsAppend(id):

	#I learned the hard way that you don't want a trillion duplicates, it tends to crash the system
	dupid = False
	dupfri = False

	for x in ids:

		if(str(x) == str(id)):
			dupid = True 
		else:
			continue
	
	for x in friends:

		if(str(x) == str(id)):
			dupfri = True
		else:
			continue

	if(dupid == False):
		ids.append(id)		
	if(dupfri == False):
		friends.append(id)


def crawlUser(id):

	print("Crawling ID ["+str(id)+"]")
	
	#Varibales of URLS
	followers = "https://www.duolingo.com/2017-06-30/users/"+str(id)+"/subscribers"
	following = "https://www.duolingo.com/2017-06-30/users/"+str(id)+"/subscriptions"

	try:
		#Get the follower data
		resp = session.authRequest(followers, "GET")
		resp = json.loads(resp)
		
		#Enumerate followers and store them in the "ids" list variable
		for id in resp['subscribers']:
		
			idsAppend(str(id['id']))

		#Get the following list
		resp = session.authRequest(following, "GET")
		resp = json.loads(resp)

		#Enumerate and store in "ids" list for later crawling
		for id in resp['subscriptions']:

			idsAppend(str(id['id']))
	
	except Exception as e:

		logError(e, id)
	

#2 hours in, I figured out there's a secret token passed other than csrf. Lots of 403 errors
def addFriend(id):
		
	add = "https://www.duolingo.com/2017-06-30/users/"+user+"/subscriptions/"+str(id)
	cookie = session.getCookie()
	data = {'csrfToken':str(cookie['csrf_token'])}
	resp = session.authRequest(add, "PUT", params=data)

	if(resp == 200):

		saveFriendToDatabase(id)
		print("["+str(resp)+"] Added user ["+str(id)+"] as a friend")

	else:

		print("["+str(resp)"] Unable to add user "+str(id))

#Mom I don't need friends
def delFriend(id):

	print("Removing user ["+str(id)+"] from subscriptions")
	cookie = session.getCookie()
	token = cookie['csrf_token']
	delete = "https://www.duolingo.com/2017-06-30/users/"+user+"/subscriptions/"+str(id)+"?csrfToken="+str(token)
	resp = session.authRequest(delete, "DELETE")
	deleteFriendFromDatabase(id)

def friendWorker():
	
	#This function will be ran by the friend thread
	for x in friends:
		
		addFriend(x)
		friends.remove(str(x))

def crawlWorker():

	#This function will be ran by the crawler thread
	for x in ids:

		crawlUser(x)
		ids.remove(str(x)) #Again... little memory as possible

def debug():

	#Lots of troubleshooting here....
	print(ids)

system("clear")
i = input("Enter the ID of the user to begin crawling: ")
system("clear")
ids = [ str(i) ]
friends = [ str(i) ]
crawlUser(i)


try:

	#We start two threads so that the script will simutaneously crawl and add
	t1 = threading.Thread(target=crawlWorker)
	t2 = threading.Thread(target=friendWorker)
	t1.start()
	t2.start()

	t1.join()
	t2.join()

except:
	print("Error: unable to start thread")

