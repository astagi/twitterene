"""
	Developed by 
	Andrea Stagi <stagi.andrea@gmail.com>

	Twitterene: update emesene with your Twitter status
	Copyright (C) 2010 Andrea Stagi

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from tweepy import *
import tweepy.error
import blowfish
from hashlib import sha256
import pickle
import os

def getApi(usr,psw):

    username = usr  
    password = psw

    cipher = blowfish.Blowfish(sha256('key').digest()) 
    cipher.initCTR() 
		
    if os.path.exists(os.path.join(os.getcwd(),"emesene","plugins_base","twitterene","twitthings.twl")):
	consumer=cipher.decryptCTR(pickle.load(open(os.path.join(os.getcwd(),"emesene","plugins_base","twitterene","twitthings.twl"), 'rb'))) 
    else:
        consumer=cipher.decryptCTR(pickle.load(open(os.path.join(os.getcwd(),"plugins_base","twitterene","twitthings.twl"), 'rb'))) 

    auth = OAuthHandler(consumer[0:21], consumer[22:len(consumer)])

    try:
    	token = auth.get_xauth_access_token(username, password)
    except error.TweepError as details:
	print  details.reason
	return None


    auth.set_access_token(token.key, token.secret)

    return API(auth)
