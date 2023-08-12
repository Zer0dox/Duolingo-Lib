from duosession import *
from duo import *
from ai import *
import json


id = "766274822"
session = duoSession()
followers = "https://www.duolingo.com/2017-06-30/users/"+str(id)+"/subscribers"

#Get the follower data
resp = session.authRequest(followers, "GET")
resp = json.loads(resp)

for user in resp['subscribers']:

	try:
		uid = user['id']
		ai = botAI(uid)
		score = ai.calculateUserScore()
		name = user['name']

		print("["+str(id)+"] "+name+" scored "+str(score))
	except Exception as e:
		logError(e, user)