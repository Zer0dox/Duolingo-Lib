import json
import requests
import sqlite3
import pandas
import time
from os import system, getcwd, mkdir

base_url = "https://www.duolingo.com/"
data_url = base_url + "2017-06-30/users/"
login_url = base_url + "2017-06-30/login?fields="
parameters = "?fields=acquisitionSurveyReason,adsConfig,betaStatus,bio,blockedUserIds,canUseModerationTools,courses,creationDate,currentCourse,email,emailAnnouncement,emailAssignment,emailAssignmentComplete,emailClassroomJoin,emailClassroomLeave,emailComment,emailEditSuggested,emailEventsDigest,emailFollow,emailPass,emailPromotion,emailWeeklyProgressReport,emailSchoolsAnnouncement,emailStreamPost,emailVerified,emailWeeklyReport,enableMicrophone,enableSoundEffects,enableSpeaker,experiments%7Bconnect_web_kudos_feed_redesign,courses_fr_ja_v1,courses_it_de_v1,hoots_web,hoots_web_100_crowns,hoots_web_rename,learning_det_scores_v1,learning_duolingo_score_v1,learning_fix_whitespace_grading,media_shorten_cant_speak_web,midas_new_years_2022_14_day_ft,midas_new_years_2022_purchase_flow,midas_new_years_2022_purchase_page,midas_web_checklist_header_copy,midas_web_immersive_plus_v2,midas_web_longscroll,midas_web_new_years_discount_2022,midas_web_plus_applicable_taxes,midas_web_plus_dashboard_mobile_users,midas_web_plus_dashboard_stripe_users,nurr_web_add_coach_duo_section_test_out,nurr_web_coach_duo_in_placement_v2,nurr_web_session_end_v0,nurr_web_simplify_first_skill_popouts,nurr_web_uo_home_message_v0,security_web_profile_reporting,sigma_web_direct_purchase_hide_monthly,sigma_web_family_plan_shop_promo,sigma_web_family_se_promo,sigma_web_legendary_gold_promo,sigma_web_legendary_practice_promo,spam_non_blocking_email_verification,speak_allow_continue_block_microphone,speak_rewrite_speak_challenge,speak_web_port_speak_waveform,speak_web_retries,stories_web_column_match_challenge,stories_web_crown_pacing_new_labels,stories_web_freeform_writing_examples,stories_web_intro_callout_tier_1,stories_web_newly_published_labels,unify_checkpoint_logic_web%7D,facebookId,fromLanguage,globalAmbassadorStatus,googleId,hasPlus,id,inviteURL,joinedClassroomIds,lastStreak%7BisAvailableForRepair,length%7D,learningLanguage,lingots,location,monthlyXp,name,observedClassroomIds,persistentNotifications,picture,plusDiscounts,practiceReminderSettings,privacySettings,referralInfo,rewardBundles,roles,streak,streakData%7Blength%7D,timezone,timezoneOffset,totalXp,trackingProperties,unconsumedGiftIds,username,webNotificationIds,weeklyXp,xpGains,xpGoal,zhTw,_achievements&_=1641137089800"

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

def extractUserProfilePic(id):

    try:
        #Download photo
        r = requests.get(data_url+str(id)+parameters)
        data = r.json()
        pLoc = "https:"+ str( data['picture'] ) + "/xxlarge"
        r  = requests.get(pLoc)

        #Save photo to user directory
        path = getcwd() + "/extractions/" + str(id)
        try:
            mkdir(path)
        except:
            print("directory exists")
        filename = str(path) + "/xxlarge.jpeg"
        try:
            f = open(filename, "wb").write(r.content)
        except:
            print("file exists!")

    except Exception as e:

        logError(e, id)
    


    return r

def getUsername(id):

    try:

        url = data_url + str(id) + parameters
        r = requests.get(url)
        data = r.json()
        username = data['username']
        return(username)

    except Exception as e:

        logError(e, id)

def extractUserDataByID(id):

    try:

        username = getUsername(id)
        url = "https://www.duolingo.com/2017-06-30/users?username="+username+"&_=1641137906100"
        r = requests.get(url)
        return(r.content)

    except Exception as e:

        logError(e, id)

def extractUserDataByUsername(username):

    try:
        url = "https://www.duolingo.com/2017-06-30/users?username="+username+"&_=1641137906100"
        r = requests.get(url)
        return(r.content)

    except Exception as e:

        logError(e, username)

def saveFriendToDatabase(id):

    try:

        conn = sqlite3.connect("userdata.sql")
        t = time.time()
        t = int(t)
        
        sql = "INSERT INTO friends (id, timestamp) VALUES ('%s', '%i');" % (id, t)
        conn.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:

        logError(e, id)

def deleteFriendFromDatabase(id):

    try:

        conn = sqlite3.connect("userdata.sql")
        sql = "DELETE FROM friends WHERE id='%s';" % (id)
        conn.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:

        logError(e, id)


def logError(e, id):

    print(R+"An error occurred with id "+str(id)+W)
    f = open("errors.log", "a+")
    error = "Error ID "+str(id)+" - "+str(e)+"\n"
    f.write(str(error))
    f.close()



