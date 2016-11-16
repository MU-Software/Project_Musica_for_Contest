#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from DirectGUI.end import End
from DirectGUI.play import Play
from DirectGUI.title import Title
from DirectGUI.score import Score
from DirectGUI.select import Select
from DirectGUI.startup import StartUp
from DirectGUI.GUI_BASE import GUIbase

class MU_GUI:
	def __init__(self):
		self.GUI_base = GUIbase()
		
		self.end = End()
		self.play = Play()
		self.title = Title()
		self.user_updater  = self.title.user_update
		self.user_returner = self.title.user_return
		self.credit_updater  = self.title.credit_update
		self.credit_returner = self.title.credit_return
		self.score = Score()
		self.select = Select()
		
		base.accept('GUI_MGR', self.GUI_mgr)
	
	def credit_1up(self):
		self.title_coin_text_mgr(self.title.credit_return()+1)
	
	def timerTask(self, task):
		self.secondsTime = 90-int(task.time)%180
		if self.secondsTime <= 15:
			if int(self.select.timer_STR.getText()) != self.secondsTime:
				self.select.timeout_sfx.play()
			self.select.timer_STR["fg"]=(.75, 0, 0, 1)
		self.select.timer_STR.setText(str(self.secondsTime))
		if self.secondsTime <= 0:
			self.select.unload_select_GUI(None)
			self.end.setup_end_GUI()
			taskMgr.doMethodLater(3, self.title.setup_title_GUI, "GUI_title_create")
			base.accept("tab", self.credit_1up)
			return Task.done
		return Task.cont
	
