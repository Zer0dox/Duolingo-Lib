import requests
import pickle
import json
from os.path import exists
import pyuser_agent

#Whitespace in python isn't bad. Only thing that matters are the indents. Imagine if there weren't space..
class duoSession:

	#Login data from script to run
	__username = ""
	__password = ""
	__userID = "" # LOL SCRATCH THAT 3 HOURS I HAD THE WRONG USER ID. CANT ADD FRIENDS FOR OTHER PEOPLE

	#URL schemes
	__base_url = "https://www.duolingo.com/"
	__data_url = __base_url + "2017-06-30/users/"
	__login_url = __base_url + "2017-06-30/login?fields="
	__parameters = "?fields=acquisitionSurveyReason,adsConfig,betaStatus,bio,blockedUserIds,canUseModerationTools,courses,creationDate,currentCourse,email,emailAnnouncement,emailAssignment,emailAssignmentComplete,emailClassroomJoin,emailClassroomLeave,emailComment,emailEditSuggested,emailEventsDigest,emailFollow,emailPass,emailPromotion,emailWeeklyProgressReport,emailSchoolsAnnouncement,emailStreamPost,emailVerified,emailWeeklyReport,enableMicrophone,enableSoundEffects,enableSpeaker,experiments%7Bconnect_web_kudos_feed_redesign,courses_fr_ja_v1,courses_it_de_v1,hoots_web,hoots_web_100_crowns,hoots_web_rename,learning_det_scores_v1,learning_duolingo_score_v1,learning_fix_whitespace_grading,media_shorten_cant_speak_web,midas_new_years_2022_14_day_ft,midas_new_years_2022_purchase_flow,midas_new_years_2022_purchase_page,midas_web_checklist_header_copy,midas_web_immersive_plus_v2,midas_web_longscroll,midas_web_new_years_discount_2022,midas_web_plus_applicable_taxes,midas_web_plus_dashboard_mobile_users,midas_web_plus_dashboard_stripe_users,nurr_web_add_coach_duo_section_test_out,nurr_web_coach_duo_in_placement_v2,nurr_web_session_end_v0,nurr_web_simplify_first_skill_popouts,nurr_web_uo_home_message_v0,security_web_profile_reporting,sigma_web_direct_purchase_hide_monthly,sigma_web_family_plan_shop_promo,sigma_web_family_se_promo,sigma_web_legendary_gold_promo,sigma_web_legendary_practice_promo,spam_non_blocking_email_verification,speak_allow_continue_block_microphone,speak_rewrite_speak_challenge,speak_web_port_speak_waveform,speak_web_retries,stories_web_column_match_challenge,stories_web_crown_pacing_new_labels,stories_web_freeform_writing_examples,stories_web_intro_callout_tier_1,stories_web_newly_published_labels,unify_checkpoint_logic_web%7D,facebookId,fromLanguage,globalAmbassadorStatus,googleId,hasPlus,id,inviteURL,joinedClassroomIds,lastStreak%7BisAvailableForRepair,length%7D,learningLanguage,lingots,location,monthlyXp,name,observedClassroomIds,persistentNotifications,picture,plusDiscounts,practiceReminderSettings,privacySettings,referralInfo,rewardBundles,roles,streak,streakData%7Blength%7D,timezone,timezoneOffset,totalXp,trackingProperties,unconsumedGiftIds,username,webNotificationIds,weeklyXp,xpGains,xpGoal,zhTw,_achievements&_=1641137089800"
	
	#
	__r = requests.Session()

	#headers
	ua = pyuser_agent.UA()
	__useragent = ua.random
	__referrer = "https://www.duolingo.com/profile/zyantos"
	__auth = "Bearer "

	#Set the PAINFUL Authorization Header and save cookies/auth to files
	__head = {

		'User-Agent' : __useragent, 
		'Referer' : __referrer, 
		'TE' : 'trailers',
		'Origin' : __base_url

	}

	#This function executes when we call the duoSession Class in a script
	def __init__(self):

		#Check if cookies have already been saved in previous session
		if(exists("cookie.dat")):
 			
 			#If the files exist, the data is loaded into the current session
			with open('cookie.dat', 'rb') as f:
			    self.__r.cookies.update(pickle.load(f))
			f.close()
			with open('auth.dat', 'r') as f:
				self.__auth = f.readline()
			f.close()

			#Set our authorization header for special requests
			self.__r.headers.update({'Authorization' : self.__auth})

		else:

			#Grab logged out user ID from cookie, for login request
			path = self.__login_url
			self.__r.get(self.__base_url)
			cookie = self.__r.cookies.get_dict()
			payload = json.dumps({"distinctId":str(cookie['logged_out_uuid']),"identifier":self.__username,"password":self.__password,"landingUrl":self.__base_url})
			
			#Login
			resp = self.__r.post(path, data=payload)
			headers = resp.headers
			self.__auth = self.__auth+str(headers['jwt'])


			self.__r.headers.update(self.__head)
			with open('cookie.dat', 'wb') as f:
				pickle.dump(self.__r.cookies, f)
			with open('auth.dat', 'w+') as f:
				f.write(self.__auth)


	def getUserId(self):
		
		return self.__userID

	#There are a million different ways to handle this, but  honestly, having all of your functions in one place makes scripts cleaner
	#I could have called these individually in massfriend.py without using a class
	#But this allows me to make one tweak for one mistake. If I called these in every function I made a request, one mistake becomes 7
	#Think of it like building blocks
	def authRequest(self, path, method, params = {}):

		if(method == "POST"):

			req = self.__r.post(path, data=params)
			return(req.text)

		elif(method == "GET"):

			req = self.__r.get(path)
			return(req.text)

		elif(method == "PUT"):

			self.__r.headers.update(self.__head)
			req = self.__r.put(path, json=params)
			return(req.status_code)

		elif(method == "DELETE"):

			req = self.__r.delete(path)
			return(req.status_code)

		elif(method == "OPTIONS"):

			req = self.__r.options(path)
			return(req.text)

	def getCookie(self):

		return self.__r.cookies.get_dict()

	def getHeaders(self):

		return self.__r.headers

