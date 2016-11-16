#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from GUI_BASE import GUIbase
#print base.messenger.toggleVerbose()

COMBO_TEXT = \
"""\
COMBO
{0}\
"""

class Play(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		
		#self.clear_status_bar['value'] = 0
		
		#self.setup_play_GUI()
		#taskMgr.doMethodLater(.1, self.setup_play_GUI, "setup_play_GUI")
	
	def setup_play_GUI(self, task=None):
		self.GUI_OBJ = render2d.attachNewNode("GUI_OBJ_PLAY")
		
		self.highest_combo_count = 0
		self.combo_count = 0
		self.miss_count = 0
		self.hit_count = 0
		self.score_val = 0
		
		self.combo_Lbl = OnscreenText(text='',
									  mayChange=1,
									  parent=render,
									  font=self.font_koverwatch,
									  fg=(0, 0, 0, 1),
									  pos=(0, 35, 20),
									  scale=(6, 8, 0)
									  )
		self.combo_Lbl.setHpr(0, 182.5, 0)
		self.combo_Lbl.setTwoSided(True)
		
		self.h_com_Lbl = OnscreenText(text='COMBO: 000',
									  mayChange=1,
									  parent=self.GUI_OBJ,
									  font=self.font_koverwatch,
									  fg=(1, 1, 1, 1),
									  pos=(-.75, .75, 0),
									  scale=(.1))
		self.miss_Lbl  = OnscreenText(text='MISS : 000',
									  mayChange=1,
									  parent=self.GUI_OBJ,
									  font=self.font_koverwatch,
									  fg=(1, 1, 1, 1),
									  pos=(-.75, .6, 0),
									  scale=(.1))
		self.score_Lbl = OnscreenText(text='SCORE: %06d'%self.score_val,
									  mayChange=1,
									  parent=self.GUI_OBJ,
									  font=self.font_koverwatch,
									  fg=(1, 1, 1, 1),
									  pos=(.75, .75, 0),
									  scale=(.1))
	
	def set_combo_text(self, text):
		self.combo_Lbl.setText(text)
		LerpColorScaleInterval(self.combo_Lbl, 1.5, (0, 0, 0, 0), (0, 0, 0, 1), name='combo_txt_effect').start()
		if self.combo_count > self.highest_combo_count:
			self.highest_combo_count = self.combo_count
			self.h_com_Lbl.setText('COMBO : %03d'%self.highest_combo_count)
	
	def return_combo_count(self):
		return self.combo_count
	
	def miss_updater(self, val):
		self.miss_count += val
		self.miss_Lbl.setText('MISS : %03d'%self.miss_count)
		
	def score_updater(self, val):
		self.score_val += val
		self.score_Lbl.setText('SCORE: %06d'%self.score_val)
	
	#Remove play GUI resources
	def unload_play_GUI(self, task=None):
		target_node = render2d.findAllMatches("GUI_OBJ_PLAY")
		for i in target_node:
			LerpColorScaleInterval(i, .5, (0, 0, 0, 0)).start()
		def remove_task(task):
			for i in target_node:
				i.remove_node()
		
		taskMgr.doMethodLater(1, remove_task, "unload_play_GUI")