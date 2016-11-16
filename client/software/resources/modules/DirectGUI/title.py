#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from GUI_BASE import GUIbase

TEXT_CHAR_ANIM_TIME = 0.0075
TEXT_DEL_DELAY_TIME = 2.5
TEXT_ADD_DELAY_TIME = 0.2

class Title(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		
		#Current credit label
		self.current_credit = 0
		current_credit_text = "CREDIT(S) " + str(self.current_credit) + " / 3"
		self.label_credit = OnscreenText(text=current_credit_text,
										parent=render2d,
										fg=(1, 1, 1, 1),
										font=self.font_CPMono,
										mayChange=1,
										frame=(0, 0, 0, 0))
		self.label_credit.setScale(.033)
		self.label_credit.setPos(.8, -.95)
		
		
		self.GUI_BGI = render2d.attachNewNode("GUI_BGI")
		
		#Background Image + Animation sequence
		self.title_BGI_upper = self.GUI_BGI.attachNewNode(self.cm.generate())
		self.title_BGI_upper_tex = loader.loadTexture('title/background_upper_layer.png')
		self.title_BGI_upper.setPos(-1, 0, -1)
		self.title_BGI_upper.setScale(2, 0, 2)
		self.title_BGI_upper.setColorScale(1, 1, 1, .9)
		self.title_BGI_upper.setTransparency(1)
		self.title_BGI_upper.setTexture(self.title_BGI_upper_tex)
		
		self.title_BGI_tex = loader.loadTexture('title/grid_white_edge_blur_2048.png')
		self.title_BGI_tex.setWrapU(Texture.WMRepeat)
		self.title_BGI_tex.setWrapV(Texture.WMRepeat)
		self.title_BGI = self.GUI_BGI.attachNewNode(self.cm.generate())
		self.title_BGI.setPos(-1, 0, -1)
		self.title_BGI.setColorScale(1, 1, 1, .5)
		res_x = base.win.getXSize()
		res_y = base.win.getYSize()
		self.title_BGI.setScale(2048.0*1.75/res_x, 0, 2048.0*1.75/res_y)
		self.title_BGI.setTransparency(1)
		self.title_BGI.setTexture(self.title_BGI_tex)
		self.title_BGI_lerper = NodePath('title_BGI_lerper')
		self.title_BGI.setTexProjector(TextureStage.getDefault(), NodePath(), self.title_BGI_lerper)
		self.title_BGI_anim = self.title_BGI_lerper.posInterval(60, VBase3(0, 1, 0))
		self.title_BGI_anim.loop()
		
		#self.setup_title_GUI()
		#taskMgr.doMethodLater(1, self.setup_title_GUI, "setup_title_GUI")
	
	def setup_title_GUI(self, task=None):
		try:
			taskMgr.remove("text_animation_task")
		except:
			pass
		self.GUI_OBJ = render2d.attachNewNode("GUI_OBJ_TITLE")
		
		#Copyright notice label
		self.label_copyright_text = "COPYRIGHT 2016 MU SOFTWARE"
		self.label_copyright = OnscreenText(text=self.label_copyright_text,
										parent=self.GUI_OBJ,
										fg=(1, 1, 1, 1),
										font=self.font_CPMono,
										mayChange=1,
										frame=(0, 0, 0, 0))
		self.label_copyright.setScale(.03)
		self.label_copyright.setPos(0, -.975)
		
		#Title text label
		self.title_str_list     = ['I', 'N', 'S', 'E', 'R', 'T', ' ', 'C', 'O', 'I', 'N', '(', 'S', ')']
		self.title_str_int_list = [  8,  13,  18,   4,  17,  19, ' ',   2,  14,   8,  13, '(',  18, ')']
		self.text_anim_pos = 0
		self.text_anim_stat= 0
		self.insert_coin_text = ''.join(self.title_str_list)
		self.label_insert_coin = OnscreenText(text=self.insert_coin_text,
											  fg=(1, 1, 1, 1),
											  font=self.font_square,
											  #font=self.font_CPMono,
											  #align=TextNode.ACenter,
											  shadow=(0, 0, 1, 1),
											  shadowOffset=(.0, .15),
											  mayChange=True,
											  frame=(0, 0, 0, 0))
		self.label_insert_coin.reparentTo(self.GUI_OBJ)
		self.label_insert_coin.node().preserve_trailing_whitespace = 1
		self.label_insert_coin.setScale(.05)
		self.label_insert_coin.setPos(0, -.5)
		taskMgr.doMethodLater(1, self.text_animation_del_task, "text_animation")
		
		
		self.musica_logo = OnscreenImage(parent=self.GUI_OBJ,
										 image='project_musica.png',
										 pos=(0, 0, .3))
		self.musica_logo.setTransparency(1)
		
		self.coin_count_sfx = loader.loadSfx('resources/se/gui_select.wav')
		self.text_change_sfx = loader.loadSfx('resources/se/gui_final.wav')
		
		self.title_music = loader.loadMusic('resources/se/title_theme.mp3')
		self.title_music.setLoop(True)
		self.title_music.setVolume(0.5)
		self.title_music.play()
		
		self.credit_update(0)
		
		self.resolutionChangeHandler_Title()
		base.accept('aspectRatioChanged', self.resolutionChangeHandler_Title)
		
		self.GUI_OBJ.setColorScale(0, 0, 0, 0)
		LerpColorScaleInterval(self.GUI_OBJ, 1, (1, 1, 1, 1)).start()
		
	#Title text animation tasks
	def text_animation_del_task(self, task):
		if self.text_anim_pos > len(self.title_str_list) - 1:
			self.text_anim_pos = 0
			self.text_anim_stat = 0
			taskMgr.doMethodLater(TEXT_ADD_DELAY_TIME, self.text_animation_add_task, 'text_animation_task')
			return task.done
		else:
			if self.text_anim_stat < 5:
				if self.title_str_list[self.text_anim_pos] in ['Z', ' ']:
					self.title_str_list[self.text_anim_pos] = ' '
					self.text_anim_stat = 0
					self.text_anim_pos += 1
				else:
					try:
						str_int = string.uppercase.index(self.title_str_list[self.text_anim_pos])
						self.title_str_list[self.text_anim_pos] = string.uppercase[str_int + 1]
						self.text_anim_stat += 1
					except:
						self.title_str_list[self.text_anim_pos] = ' '
						self.text_anim_pos += 1
						self.text_anim_stat = 0
			else:
				self.title_str_list[self.text_anim_pos] = ' '
				self.text_anim_stat = 0

		self.insert_coin_text = ''.join(self.title_str_list)
		self.label_insert_coin.setText(self.insert_coin_text)
		taskMgr.doMethodLater(TEXT_CHAR_ANIM_TIME, self.text_animation_del_task, 'text_animation_task')
	def text_animation_add_task(self, task):
		if self.text_anim_pos > len(self.title_str_list) - 1:
			self.text_anim_pos = 0
			self.text_anim_stat = 0
			taskMgr.doMethodLater(TEXT_DEL_DELAY_TIME, self.text_animation_del_task, 'text_animation_task')
			return task.done
		else:
			if type(self.title_str_int_list[self.text_anim_pos]) == int:
				self.title_str_list[self.text_anim_pos] = (
					string.uppercase[self.title_str_int_list[self.text_anim_pos]-(5-self.text_anim_stat)])
				if self.text_anim_stat < 5:
					self.text_anim_stat += 1
				else:
					self.text_anim_stat = 0
					self.text_anim_pos += 1
			else:
				self.title_str_list[self.text_anim_pos] = self.title_str_int_list[self.text_anim_pos]
				self.text_anim_pos += 1
		
		self.insert_coin_text = ''.join(self.title_str_list)
		self.label_insert_coin.setText(self.insert_coin_text)
		taskMgr.doMethodLater(TEXT_CHAR_ANIM_TIME, self.text_animation_add_task, 'text_animation_task')
	def text_animation_change(self, text="PRESS TAB KEY"):
		try:
			taskMgr.remove("text_animation_task")
		except:
			pass
		self.text_anim_stat = 0
		self.text_anim_pos  = 0
		self.title_str_list     = list(text.upper())
		self.title_str_int_list = list()
		for i in self.title_str_list:
			if i in list(string.ascii_uppercase):
				self.title_str_int_list.append(list(string.ascii_uppercase).index(i))
			else:
				self.title_str_int_list.append(i)
		self.insert_coin_text = ''.join(self.title_str_list)
		self.label_insert_coin.setText(self.insert_coin_text)
		taskMgr.doMethodLater(2.5, self.text_animation_del_task, "text_animation_task")
		self.text_change_sfx.play()
	
	def credit_update(self, value):
		self.current_credit = value
		if self.current_credit < 0:
			self.current_credit = 0
		self.label_credit["text"] = "CREDIT(S) " + str(self.current_credit) + " / 3"
		self.coin_count_sfx.play()
	def credit_return(self):
		return self.current_credit
		
	def user_update(self, text):
		self.user_label.setText("PLAYER : {0}".format(text))
	def user_return(self):
		return self.user_label.getText()[9:]
	
	def resolutionChangeHandler_Title(self):
		res_x = base.win.getXSize()
		res_y = base.win.getYSize()
		self.title_BGI.setScale(2048.0*1.75/res_x, 0, 2048.0*1.75/res_y)
		self.musica_logo.setScale(1032.*.5/res_x, 0, 312.*.5/res_y)
	
	#Remove title GUI resources
	def unload_title_GUI(self, task=None):
		try:
			self.text_change_sfx.play()
			taskMgr.remove("text_animation_task")
			#self.title_BGI_anim.pause()
			#self.title_BGI_anim = None
			self.title_music.stop()
		except:
			pass
		target_node = render2d.findAllMatches("GUI_OBJ_TITLE")
		for i in target_node:
			LerpColorScaleInterval(i, .5, (0, 0, 0, 0)).start()
		def remove_task(task):
			for i in target_node:
				i.remove_node()
		base.ignore('aspectRatioChanged')
		
		taskMgr.doMethodLater(1, remove_task, "unload_title_GUI")