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

#! /usr/bin/python
from modalbox import *
from twittapi import *
from timers import *
import urllib
import random
import os
import tempfile

gtk.gdk.threads_init()

def download_file(url,filename):
	u = urllib.urlopen(url)
	localFile = open(filename, 'wb')
	localFile.write(u.read())
	localFile.close()

class App:

	def __init__(self,msn,controller,config,appname):

		if os.path.exists(os.path.join(os.getcwd(),"emesene","plugins_base","twitterene","img","wait.gif")):
			self.wait_path=os.path.join(os.getcwd(),"emesene","plugins_base","twitterene","img","wait.gif")
			self.logo_path=os.path.join(os.getcwd(),"emesene","plugins_base","twitterene","img","twitterlogo.png") 
		else:
			self.wait_path=os.path.join(os.getcwd(),"plugins_base","twitterene","img","wait.gif")
			self.logo_path=os.path.join(os.getcwd(),"plugins_base","twitterene","img","twitterlogo.png")

		self.appname=appname
		self.controller=controller
		self.msn=msn

		self.usr=""
		self.psw=""

		self.isenable=1
		self.avatar=1
		self.mess=1
		self.name=1

		self.tmpdir=tempfile.mkdtemp(suffix="twitterene")

		self.reftim=None

		self.config=config

		self.api=None

	def updateMyStatus(self):

		if(self.reftim!=None):
			self.reftim.stop()

		self.reftim=refresh(self)
		self.reftim.start()

	def buildImage(self,url):

		url=url[url.find("src"):len(url)]
		url=url[url.find("\"")+1:len(url)]
		url=url[:url.find("\"")]

		return url
		

	def getProfileImage(self):

		html_lines = urllib.urlopen("http://twitter.com/"+self.api.me().screen_name).readlines()

		count=0

		for line in html_lines:
			if line.find("profile-user") != -1:
				filename=os.path.join(self.tmpdir,"imgprev.jpeg")
				download_file(self.buildImage(html_lines[count+3]),filename)
				return filename
			count+=1
						

	def syncEmesene(self):

		if not self.isenable:
			return

		self.mbox.set_preview(self.wait_path)

		if self.name:
			try:
				name=self.api.me().screen_name
			except:
				return
			self.mbox.set_prevuser_text(name)
			self.msn.changeNick(name)
		else:
			self.mbox.set_prevuser_text(self.msn.nick)
			

		if self.mess:
			status=self.api.user_timeline()	

			if(len(status[0].text)>32):
				self.mbox.set_prevmess_text(status[0].text[0:32]+"...")
			else:
				self.mbox.set_prevmess_text(status[0].text)

			self.msn.changePersonalMessage(status[0].text[0:129])
		else:
			if(len(self.msn.personalMessage)>32):
				self.mbox.set_prevmess_text(self.msn.personalMessage[0:32]+"...")
			else:
				self.mbox.set_prevmess_text(self.msn.personalMessage)

		if self.avatar:
			try:
				filename=self.getProfileImage()
			except:
				filename=self.controller.avatar.imagePath
				
			self.mbox.set_preview(filename)
			self.controller.changeAvatar(filename)
		else:
			self.mbox.set_preview(self.controller.avatar.imagePath)

	def showConnectionError(self):
		pass

	def userIsChanged(self):
		if(self.mbox.get_user_text()!=self.usr or self.mbox.get_password_text()!=self.psw):
			return True
		return False

	def storeConfig(self):
		self.config.setPluginValue(self.appname, 'user', self.mbox.get_user_text())
		self.config.setPluginValue(self.appname, 'password', self.mbox.get_password_text())

		self.isenable=self.mbox.is_enabled()
		self.avatar=self.mbox.is_avatar()
		self.name=self.mbox.is_name()
		self.mess=self.mbox.is_mess()

		self.config.setPluginValue(self.appname, 'enable', self.isenable)
		self.config.setPluginValue(self.appname, 'avatar', self.avatar)
		self.config.setPluginValue(self.appname, 'username', self.name)
		self.config.setPluginValue(self.appname, 'message', self.mess)

		self.config.setPluginValue(self.appname, 'firsttime', self.firsttime)


	def restoreConfig(self):
		self.usr=self.config.getPluginValue(self.appname, 'user','')
		self.psw=self.config.getPluginValue(self.appname, 'password','')

		self.isenable=int( self.config.getPluginValue(self.appname, 'enable',1))
		self.avatar= int( self.config.getPluginValue(self.appname, 'avatar',1))
		self.name= int( self.config.getPluginValue(self.appname, 'username',1))
		self.mess= int( self.config.getPluginValue(self.appname, 'message',1))

		self.firsttime= int( self.config.getPluginValue(self.appname, 'firsttime',1))

		self.mbox.set_is_enabled(self.isenable)
		self.mbox.set_is_avatar(self.avatar)
		self.mbox.set_is_name(self.name)
		self.mbox.set_is_mess(self.mess)

		self.mbox.set_user_text(self.usr)
		self.mbox.set_password_text(self.psw)

	def connectTwitter(self):

		self.stopMe()

		if(self.api==None or self.userIsChanged()):
			self.api=getApi(self.mbox.get_user_text(),self.mbox.get_password_text())

		if(self.api==None):
			self.showConnectionError()
			return

		self.firsttime=0
		
	def on_done(self):
		self.connectTwitter()
		self.storeConfig()
		self.updateMyStatus()

	def stopMe(self):

		if(self.reftim!=None):
			self.reftim.stop()

	def main(self):
		
		self.mbox=ModalBox()
		self.mbox.set_app_logo(self.logo_path)

		self.mbox.set_done_callback(self.on_done)

		self.restoreConfig()

		if(self.firsttime!=1):
			self.connectTwitter()
			self.updateMyStatus()
		
		return 0



