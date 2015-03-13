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

import gtk
import sys
import os 

class ModalBox:

	def __init__(self):

		#attribs
		self.user=gtk.Entry()
		self.password=gtk.Entry()
		self.password.set_invisible_char('*')
		self.password.set_visibility(False)
		self.time_change=gtk.Entry()

		#gtk.gtk_entry_set_invisible_char(self.password,'*')

		self.prevuser=gtk.Label("")
		self.prevmess=gtk.Label("")

		self.prevuser.set_line_wrap(True)
		#self.prevmess.set_width_chars() 

		self.logo=gtk.Image()
		self.preview=gtk.Image()

		self.combobox=gtk.ComboBoxEntry()
		self.combospeed=gtk.ComboBoxEntry()

		self.check_enable=gtk.CheckButton("Enable")
		self.check_avatar=gtk.CheckButton("Get avatar")
		self.check_name=gtk.CheckButton("Get name")
		self.check_mess=gtk.CheckButton("Get status")

		self.combo_change_callback=None

		self.btn_logout=gtk.Button("Logout")
		self.btn_ok=gtk.Button("Update")

		#gui layout
		self.main_boxv=gtk.VBox()
		self.main_box=gtk.HBox()
		self.main_boxv.pack_start(self.main_box)

		user_layout=gtk.HBox()
		user_layout.pack_start(gtk.Label("Username:"))
		user_layout.pack_start(self.user)
		user_layout.pack_start(gtk.Label(" "))

		psw_layout=gtk.HBox()
		psw_layout.pack_start(gtk.Label("Passoword:"))
		psw_layout.pack_start(self.password)
		psw_layout.pack_start(gtk.Label(" "))

		desc=gtk.VBox()

		desc.pack_start(self.logo)        
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)       

		fields=gtk.VBox()

		fields.pack_start(user_layout)
		fields.pack_start(psw_layout)

		fields.pack_start(gtk.Label(""))
		fields.pack_start(gtk.HSeparator())


		boxgroup1_layout=gtk.VBox()

		boxgroup1_layout.pack_start(self.check_enable)
		boxgroup1_layout.pack_start(self.check_avatar)

		boxgroup2_layout=gtk.VBox()

		boxgroup2_layout.pack_start(self.check_name)
		boxgroup2_layout.pack_start(self.check_mess)

		boxes=gtk.HBox()

		boxes.pack_start(boxgroup1_layout)
		boxes.pack_start(boxgroup2_layout)
	
		fields.pack_start(boxes)

		fields.pack_start(gtk.HSeparator())
		fields.pack_start(gtk.Label(""))

		prev_layout=gtk.HBox()

		prev_layout.pack_start(self.preview)
		prev_layout.pack_start(gtk.Label(" "))

		prev_mess_layout=gtk.VBox()


		self.align_user=gtk.Alignment(xalign=0.0,xscale=0.0)
       		self.align_mess=gtk.Alignment(xalign=0.0,xscale=0.0)
       		self.align_user.add(self.prevuser)
       		self.align_mess.add(self.prevmess)

		prev_mess_layout.pack_start(self.align_user)
		prev_mess_layout.pack_start(self.align_mess)

		prev_layout.pack_start(prev_mess_layout)

		fields.pack_start(prev_layout)
		

		self.main_box.pack_start(desc)
		self.main_box.pack_start(gtk.VSeparator())
		self.main_box.pack_start(fields)
		self.main_boxv.pack_start(self.btn_ok)

		#window      
		self.window.add(self.main_boxv)
		self.window.set_title("Twitterene for emesene (ver. 1.0)")
		self.window.set_modal(True)

		#signal connection
		self.btn_ok.connect("clicked",self.done_cb)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)	
		self.window.connect("delete-event", self.delete_event)

		self.window.set_resizable(False)

	def set_app_logo(self,path):
		self.logo_path=path
		self.set_logo(self.logo_path)

	#callbacks

	def restore_on_logout(self):
		self.logoutmess.set_text("")

	def done_cb(self,event):
		if self.done_callback:
			self.done_callback()

	def get_album_cb(self,event):
		if self.get_album_callback:
			self.get_album_callback()

	def logout_cb(self,event):
		if self.logout_callback:
			self.logout_callback()

	def random_cb(self,event):
		if self.random_callback:
			self.random_callback()

	def combo_change_cb(self,event):
		if self.combo_change_callback:
			self.combo_change_callback()

	#callback setter
	def set_album_callback(self,cb):
		self.get_album_callback=cb

	def set_logout_callback(self,cb):
		self.logout_callback=cb

	def set_done_callback(self,cb):
		self.done_callback=cb

	def set_random_callback(self,cb):
		self.random_callback=cb

	def set_combo_change_callback(self,cb):
		self.combo_change_callback=cb

	#window callback

	def self_destroy(self,e,w):
		self.window.hide_all()

	def hide_event(self,e,w):
		self.window.hide()

	def show(self,e=None,w=None):
		self.window.show_all()

	def delete_event(self,event,widget):
		self.window.hide()
		return True

	def set_logo(self,img):
		self.logo.set_from_file(img)

	def set_preview(self,img):
		self.preview.set_from_file(img)

	def set_albums(self,albums):
		self.albums=albums
		self.set_model_from_list(self.combobox,albums)
		self.combobox.set_active(0)
        
	def get_selected_album(self):
		return self.combobox.get_active_text()

	def set_model_from_list (self,cb, items):           
		model = gtk.ListStore(str)
		for i in items:
			model.append([i])
			cb.set_model(model)
			if type(cb) == gtk.ComboBoxEntry:
				cb.set_text_column(0)
			elif type(cb) == gtk.ComboBox:
				cell = gtk.CellRendererText()
				cb.pack_start(cell, True)
				cb.add_attribute(cell, 'text', 0)

	#states
	def is_enabled(self):
		return int(self.check_enable.get_active())

	def is_avatar(self):
		return int(self.check_avatar.get_active())

	def is_name(self):
		return int(self.check_name.get_active())

	def is_mess(self):
		return int(self.check_mess.get_active())

	def set_is_enabled(self,value):
		self.check_enable.set_active(value)

	def set_is_avatar(self,value):
		self.check_avatar.set_active(value)

	def set_is_name(self,value):
		self.check_name.set_active(value)

	def set_is_mess(self,value):
		self.check_mess.set_active(value)

	def get_time_text(self,text):
		self.time_change.set_text(text)

	def get_user_text(self):
		return self.user.get_text()

	def get_password_text(self):
		return self.password.get_text()

	def set_prevuser_text(self,text):
		return self.prevuser.set_text(text)

	def set_prevmess_text(self,text):
		return self.prevmess.set_text(text)

	def set_password_text(self,text):
		return self.password.set_text(text)

	def set_user_text(self,text):
		return self.user.set_text(text)

	def get_combo_index(self):
		return self.combobox.get_active()

	def get_combo_speed_index(self):
		return self.combospeed.get_active()

	def set_combo_index(self,n):
		return self.combobox.set_active(n)

	def set_combo_speed_index(self,n):
		return self.combospeed.set_active(n)


