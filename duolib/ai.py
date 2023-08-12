from duo import *
from duosession import *
import json
import threading
import sqlite3

"""
Score calculated by
- Follow for follow ratio 
	- if less than .75 (-50)
	- if less than .50 (-100)
	- if less than .25 (-200)
	- if greater than .75 (+50)
	- if greater than .85 (+100)
	- if greater than .95 (+150)
	- if greater than .98 (+200)

- Streak?
	- no (-100)
	- yes (+10)
	- greater than 25 (+15)
	- greater than 50 (+40)
	- greater than 75 (+65)
	- greater than 100 (90)
- XP
	- less than 1000 (-40)
	- greater 1000-5000 (+25)
	- greater 5000-15000 (+50)
	- greater 20000 (+75)
	- greater 40000 (+100)
- Plus
	- (+10)
"""



class botAI():

	__xp = 0
	__streak = 0
	__fratio = 0.00
	total = 0
	__hasPlus = False
	__passing_score = 325
	followers = 0
	following = 0
	session = duoSession()

	def __init__(self, __id):


		
		self.__id = __id
		data = extractUserDataByID(__id)
		data = json.loads(data)
		
		self.__xp = int(data['users'][0]['totalXp'])
		self.__streak = int(data['users'][0]['streak'])
		if(data['users'][0]['hasPlus'] == "true"):
			__hasPlus = True
		else:
			__hasPlus = False

		fw = "https://www.duolingo.com/2017-06-30/users/"+str(__id)+"/subscribers"
		fwi = "https://www.duolingo.com/2017-06-30/users/"+str(__id)+"/subscriptions"

		resp = json.loads(self.session.authRequest(fw, "GET"))
		self.followers = int(resp['totalSubscribers'])
		resp = json.loads(self.session.authRequest(fwi, "GET"))
		self.following = int(resp['totalSubscriptions'])


	def getPassingScore(self):

		return str(self.__passing_score)


	def calculateXpScore(self):

		if(self.__xp < 1000):
			self.total -= 40
			#print(str(self.__xp))
			#print("x score decrease 40")
		if(self.__xp >= 1000 and self.__xp < 5000):
			self.total += 25
			#print("x score inc 25")
		if(self.__xp >=5000 and self.__xp < 15000):
			self.total += 50
			#print("x score inc 50")
		if(self.__xp >= 15000 and self.__xp < 40000):
			self.total += 75
			#print("x score inc 75")
		if(self.__xp >= 50000):
			self.total += 100
			#print("x score inc 100")

	def calculateStreakScore(self):

		if(self.__streak == 0):
			self.total -= 100
			#print("s score decrease 100")
		if(self.__streak > 1):
			self.total += 10
			#print("s score inc 10")
		if(self.__streak >= 25 and self.__streak < 50):
			self.total += 15
			#print("s score inc 15")
		if(self.__streak >= 50 and self.__streak < 75):
			self.total += 40
			#print("s score inc 40")
		if(self.__streak >= 75 and self.__streak < 100):
			self.total += 65
			#print("s score inc 65")
		if(self.__streak >= 100):
			self.total += 100
			#print("s score inc 100")

	def calculateRatio(self):

		ratio = self.following / self.followers
		if(ratio < 0.25):
			self.total -= 200
			#print("r score decrease 200")
		if(ratio <= 0.50 and ratio > 0.25):
			self.total -= 100
			#print("r score decrease 100")
		if(ratio <= 0.75 and ratio > 0.50):
			self.total -= 50
			#print("r score decrease 50")
		if(ratio <= 0.85 and ratio > 0.75 ):
			self.total += 50
			#print("r score inc 50")
		if(ratio <= 0.95 and ratio > 0.85):
			self.total += 100 
			#print("r score inc 100")
		if(ratio <= 0.98 and ratio > 0.95):
			self.total += 150
			#print("r score inc 150")
		if(ratio > 0.98):
			self.total += 200
			#print("r score inc 200")

		self.__fratio = ratio

	def saveToDatabase(self):

		conn = sqlite3.connect("userdata.sql")
		sql = "INSERT INTO score_data (id, score, xp, streak, ratio) VALUES ('%s', '%i', '%i', '%i', '%s');" % (str(self.__id), self.total, self.__xp, self.__streak, str(self.__fratio))
		
		try:

			conn.execute(sql)
			conn.commit()
			conn.close()

		except Exception as e:

			logError(e, self.__id)
			conn.close()

	def calculateUserScore(self):

		self.calculateRatio()
		self.calculateXpScore()
		self.calculateStreakScore()
		self.saveToDatabase()

		
		if(self.total > self.__passing_score):
			return True 
		else:
			return False