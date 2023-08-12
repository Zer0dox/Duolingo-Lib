from duo import *
from os import system
import json
import pandas as pd
import sqlite3
from datetime import datetime, date

def main():

	#Clear terminal
	system("clear")

	print("For mass extraction, enter 1\nTo extract specific user, enter 2\n\n")
	ch = input("Enter Option: ")

	if(str(ch) == "1"):

		system("clear")
		i = input("Enter the starting ID: ")
		i = int(i)


		while(i < 900000000):

			extractUserProfilePic(i)
			data = extractUserDataByID(i)

			#Save data to database
			try:
				name = "NULL"
				data = json.loads(data)
				conn = sqlite3.connect("userdata.sql")
				date = datetime.fromtimestamp(int(data['users'][0]['creationDate'])).strftime('%Y-%m-%d %H:%M:%S')
				try:
					name = data['users'][0]['name']
				except:
					name = "NULL"
				sql = """INSERT INTO users (id, username, bio, profileCountry, globalAmbassador, currentCourseId, hasPhoneNumber, creationDate, hasPlus, name, emailVerified, totalXp, motivation, surveyReason,
				picture,
				hasFacebook,
				moderator,
				hasGoogleId) VALUES ('%i', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
				""" % (int(data['users'][0]['id']), data['users'][0]['username'], data['users'][0]['bio'], data['users'][0]['profileCountry'],data['users'][0]['globalAmbassadorStatus'],data['users'][0]['currentCourseId'],data['users'][0]['hasPhoneNumber'],date, data['users'][0]['hasPlus'],name,data['users'][0]['emailVerified'],data['users'][0]['totalXp'],data['users'][0]['motivation'],data['users'][0]['acquisitionSurveyReason'],data['users'][0]['picture'],data['users'][0]['hasFacebookId'],data['users'][0]['canUseModerationTools'],data['users'][0]['hasGoogleId'])  
				try:

					conn.execute(sql)
					conn.commit()
					conn.close()

				except Exception as e:

					logError(e, i)
					conn.close()

				print("["+str(i)+"] Extracted successfully!")

			#Catch error and save to log
			except Exception as e: 

				logError(e, i)

			i += 1

	elif(str(ch) == "2"):
		
		system("clear")
		print("To extract by ID, enter 1\nTo extract by username, enter 2")
		ch = input("Enter Option: ")

		if(str(ch) == "1"):

			#Save extract to file
			system("clear")
			i = input("Enter ID to extract data: ")
			extractUserProfilePic(i)
			data = extractUserDataByID(i)
			path = "extractions/"+str(i)+"/"+str(i)+".json"
			f = open(path, "w").write(data)

			try:

				#Save data to database
				data = json.loads(data)
				date = datetime.fromtimestamp(int(data['users'][0]['creationDate'])).strftime('%Y-%m-%d %H:%M:%S')
				if(not data['users'][0]['name']):
					name = "NULL"
				else:
					name = data['users'][0]['name']
				conn = sqlite3.connect("userdata.sql")
				sql = """INSERT INTO users (id, username, bio, profileCountry, globalAmbassador, currentCourseId, hasPhoneNumber, creationDate, hasPlus, name, emailVerified, totalXp, motivation, surveyReason,
				picture,
				hasFacebook,
				moderator,
				hasGoogleId) VALUES ('%i', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
				""" % (int(data['users'][0]['id']), data['users'][0]['username'], data['users'][0]['bio'], data['users'][0]['profileCountry'],data['users'][0]['globalAmbassadorStatus'],data['users'][0]['currentCourseId'],data['users'][0]['hasPhoneNumber'],date, data['users'][0]['hasPlus'],name,data['users'][0]['emailVerified'],data['users'][0]['totalXp'],data['users'][0]['motivation'],data['users'][0]['acquisitionSurveyReason'],data['users'][0]['picture'],data['users'][0]['hasFacebookId'],data['users'][0]['canUseModerationTools'],data['users'][0]['hasGoogleId'])  
				conn.execute(sql)
				conn.commit()
				conn.close()

				#Display user data
				system("clear")
				print("ID:\t\t\t" + str(data['users'][0]['id']))
				print("Username:\t\t" + data['users'][0]['username'])
				print("Bio:\t\t" + data['users'][0]['bio'])
				print("Profile Country:\t" + str(data['users'][0]['profileCountry']))
				print("Current Course:\t\t" + data['users'][0]['currentCourseId'])
				print("Has Phone:\t\t"+ str(data['users'][0]['hasPhoneNumber']))
				print("Created :\t\t" + date)
				print("Plus:\t\t\t"+str(data['users'][0]['hasPlus']))
				print("Name:\t\t\t"+name)
				print("Email:\t\t\t"+str(data['users'][0]['emailVerified']))
				print("Total XP:\t\t"+str(data['users'][0]['totalXp']))
				print("Motivation:\t\t"+data['users'][0]['motivation'])
				print("Survey:\t\t\t"+data['users'][0]['acquisitionSurveyReason'])
				print("Photo Location:\t\t"+data['users'][0]['picture'])
				print("Has Facebook:\t\t"+str(data['users'][0]['hasFacebookId']))
				print("Moderator:\t\t"+str(data['users'][0]['canUseModerationTools']))
				print("Has Google ID:\t\t"+str(data['users'][0]['hasGoogleId']))

			except Exception as e: 

				logError(e, i)



		elif(ch == "2"):

			#Save extract to file
			system("clear")
			username = input("Enter username to extract data: ")
			data = extractUserDataByUsername(username)
			try:
				data = json.loads(data)
			except Exception as e:
				logError(e, username)
			i = str(data['users'][0]['id'])
			date = datetime.fromtimestamp(int(data['users'][0]['creationDate'])).strftime('%Y-%m-%d %H:%M:%S')
			if(not data['users'][0]['name']):
					name = "NULL"
			else:
					name = data['users'][0]['name']
			try:

				#Save data to database
				conn = sqlite3.connect("userdata.sql")
				sql = """INSERT INTO users (id, username, bio, profileCountry, globalAmbassador, currentCourseId, hasPhoneNumber, creationDate, hasPlus, name, emailVerified, totalXp, motivation, surveyReason,
				picture,
				hasFacebook,
				moderator,
				hasGoogleId) VALUES ('%i', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
				""" % (int(data['users'][0]['id']), data['users'][0]['username'], data['users'][0]['bio'], data['users'][0]['profileCountry'],data['users'][0]['globalAmbassadorStatus'],data['users'][0]['currentCourseId'],data['users'][0]['hasPhoneNumber'],date, data['users'][0]['hasPlus'],name,data['users'][0]['emailVerified'],data['users'][0]['totalXp'],data['users'][0]['motivation'],data['users'][0]['acquisitionSurveyReason'],data['users'][0]['picture'],data['users'][0]['hasFacebookId'],data['users'][0]['canUseModerationTools'],data['users'][0]['hasGoogleId'])  
				conn.execute(sql)
				conn.commit()
				conn.close()

				#Download user profile picture
				extractUserProfilePic(i)

				#Display user data
				system("clear")
				print("ID:\t\t\t" + str(data['users'][0]['id']))
				print("Username:\t\t" + data['users'][0]['username'])
				print("Bio:\t\t" + data['users'][0]['bio'])
				print("Profile Country:\t" + str(data['users'][0]['profileCountry']))
				print("Current Course:\t\t" + data['users'][0]['currentCourseId'])
				print("Has Phone:\t\t"+ str(data['users'][0]['hasPhoneNumber']))
				print("Created :\t\t" + date)
				print("Plus:\t\t\t"+str(data['users'][0]['hasPlus']))
				print("Name:\t\t\t"+name)
				print("Email:\t\t\t"+str(data['users'][0]['emailVerified']))
				print("Total XP:\t\t"+str(data['users'][0]['totalXp']))
				print("Motivation:\t\t"+data['users'][0]['motivation'])
				print("Survey:\t\t\t"+data['users'][0]['acquisitionSurveyReason'])
				print("Photo Location:\t\t"+data['users'][0]['picture'])
				print("Has Facebook:\t\t"+str(data['users'][0]['hasFacebookId']))
				print("Moderator:\t\t"+str(data['users'][0]['canUseModerationTools']))
				print("Has Google ID:\t\t"+str(data['users'][0]['hasGoogleId']))

			#Catch error and save to log
			except Exception as e: 

				logError(e, i)	    	

		else:

			print("\nYou have entered an invalid option.")
			main()


main()