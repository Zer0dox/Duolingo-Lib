###########################################
Duolingo Tools
v2.0.1
###########################################

Edit duosession.py and enter your username and password
You will need to  set your user ID as well
You can use extract.py and get your ID by username

***FOR GOOD MEASURE, USE VPN, EVEN IF FREE

###########################################
Duo SmartFriend Bot (friend.py)

This script crawls through user profiles and adds friends for you

**Each user is given a scored based on the likelyhood of receiving a
follow back. If the score is below threshold, the script won't add them

**You can unadd friends that don't follow you back

**You can choose to add friends who have been active recently

**You can unfollow everyone. Use whitelist.txt for this option to make
exceptions

############################################
userdata.sql

You will need an sql db viewer installed.

**Stores extracted user data
**Stores score data, so you can make adjustments to the algo if needed
**Stores friend data 

############################################
whitelist.txt

Store IDs of users you want to keep following
Put only one ID per line, then hit enter

