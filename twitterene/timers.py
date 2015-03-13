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

import os
import re
import time
import sys
from threading import Thread

class refresh(Thread):

	def __init__ (self,app):
		Thread.__init__(self)
		self.app = app
		self.cont=True
		self.tmout=0

	def run(self):	
		while(self.cont):
			if(self.tmout==0):
				self.app.syncEmesene()	

			self.tmout=(self.tmout+1)%25
			time.sleep(3)

	def stop(self):
		self.cont=False



