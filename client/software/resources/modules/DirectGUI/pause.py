#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from GUI_BASE import GUIbase

class Pause(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		
		#Warning: self.setup_select_GUI() shouldn't be used in __init__ directly
		#because render result of first frame must be just black, and may get unexpected results.
		#taskMgr.doMethodLater(1, self.setup_pause_GUI, "setup_pause_GUI")
	
	def setup_pause_GUI(self, task=None):
		self.GUI_OBJ = render2d.attachNewNode("GUI_OBJ_PAUSE")
		
		self.prevRes = (base.win.getXSize(), base.win.getYSize())
		self.pause_BGI = self.GUI_OBJ.attachNewNode(self.cm.generate())
		self.pause_BGI.setPos(-1, 0, -1)
		self.pause_BGI.setScale(2, 0, 2)
		self.pause_BGI.setTransparency(1)
		self.pause_BGI.setColor(1, 1, 1, 1)
		self.pause_BGI.setColorScale(1, 1, 1, 0)
		
		self.graphic_buffer_str = base.win.getScreenshot().getRamImageAs("rgba")
		self.graphic_buffer_pil = Image.frombuffer("RGBA", self.prevRes, self.graphic_buffer_str)
		self.pause_BGI_pil = (self.graphic_buffer_pil.filter(ImageFilter.GaussianBlur(10))).tobytes()
		
		self.pause_BGI_tex = Texture()
		self.pause_BGI_tex.setup2dTexture(self.prevRes[0], self.prevRes[1],
										  Texture.TUnsignedByte, Texture.FRgba)
		self.pause_BGI_tex.setRamImageAs(self.pause_BGI_pil, "RGBA")
		self.pause_BGI.setTexture(self.pause_BGI_tex)
		self.pause_BGI.setTexScale(TextureStage.getDefault(), 1, -1)
		
		LerpColorScaleInterval(self.pause_BGI, .4,  VBase4(1, 1, 1, 1)).start()
		taskMgr.doMethodLater(.001, self.setup_additional_pause_GUI, "setup_additional_pause_GUI")
		
	def setup_additional_pause_GUI(self, task):
		self.text_size    = .125
		self.text_x       = -.4
		self.text_start_y = .3
		self.text_space   = .2
		self.label_return_to_game = OnscreenText(text='Return to Game',
												 parent=self.GUI_OBJ,
												 fg=(1, 1, 1, 1),
												 font=self.font_koverwatch,
												 pos=(self.text_x, self.text_start_y-self.text_space*0),
												 scale=self.text_size
												 )
		self.label_giveup_select  = OnscreenText(text='Give up and Select song',
												 parent=self.GUI_OBJ,
												 fg=(1, 1, 1, 1),
												 font=self.font_koverwatch,
												 pos=(self.text_x, self.text_start_y-self.text_space*1),
												 #shadow=(0, 0, 1, .75),
												 #shadowOffset=(.0, .05),
												 scale=self.text_size
												 )
		self.label_giveup_title   = OnscreenText(text='Give up and Go to title',
												 parent=self.GUI_OBJ,
												 fg=(1, 1, 1, 1),
												 font=self.font_koverwatch,
												 pos=(self.text_x, self.text_start_y-self.text_space*2),
												 scale=self.text_size
												 )
		self.label_giveup_exit    = OnscreenText(text='Give up and Exit Game',
												 parent=self.GUI_OBJ,
												 fg=(1, 1, 1, 1),
												 font=self.font_koverwatch,
												 pos=(self.text_x, self.text_start_y-self.text_space*3),
												 scale=self.text_size
												 )
		self.allLbl = [self.label_return_to_game,
					   self.label_giveup_select,
					   self.label_giveup_title,
					   self.label_giveup_exit]
		
		self.show_select_frame    = OnscreenImage(image='grid_white.png',
												  scale=(.5, 0, .1),
												  parent=self.GUI_OBJ
												  )
		self.show_select_frame.setTransparency(1)
		self.show_select_frame.setColorScale(1, 1, 1, 0)
		
		start_anim_seq = Parallel()
		for i in self.allLbl:
			i.setColorScale(1, 1, 1, 0)
			if not i == self.label_return_to_game:
				start_anim_seq.append(LerpColorScaleInterval(i, .25,  VBase4(1, 1, 1, .25)))
			else:
				start_anim_seq.append(LerpColorScaleInterval(i, .75,  VBase4(1, 1, 1, 1)))
		start_anim_seq.append(LerpColorScaleInterval(self.show_select_frame, .75,  VBase4(1, 1, 1, 1)))
		start_anim_seq.start()
		
		self.cPos = 0
		
		self.resolutionChangeHandler_Pause()
		base.accept("arrow_up"  , self.select_movement_arrow, [-1])
		base.accept("arrow_down", self.select_movement_arrow, [+1])
		base.accept("time-arrow_down-repeat", self.select_movement_arrow, [+1])
		base.accept("time-arrow_up-repeat"  , self.select_movement_arrow, [-1])
		base.accept('aspectRatioChanged', self.resolutionChangeHandler_Pause)

	def select_movement_arrow(self, pos, Long_Hold_Dummy=None):
		allLbl_num = len(self.allLbl)-1
		#ADD SFX HERE!
		pos = allLbl_num if (self.cPos < 1 and pos < 0)\
						 else -allLbl_num if (self.cPos > allLbl_num-1 and pos > 0)\
						 else pos
		self.select_movement(self.cPos + pos)
		
	def select_movement(self, num):
		select_movement_seq_list  = Parallel(name="select_movement_seq")
		tLbl = self.allLbl[num]
		not_tLbl = [i for i in self.allLbl if not i == self.allLbl[num]]
		select_movement_seq_list.append(LerpColorScaleInterval(tLbl, .25,  VBase4(1, 1, 1, 1)))
		select_movement_seq_list.append(
			self.show_select_frame.posInterval(.1, (self.text_x, 0, tLbl.getPos()[1]+tLbl.getScale()[1]/2.0)))
		for i in not_tLbl:
			select_movement_seq_list.append(LerpColorScaleInterval(i, .1,  VBase4(1, 1, 1, .25)))
		self.cPos = num
		select_movement_seq_list.start()
	
	def resolutionChangeHandler_Pause(self):
		res_x = base.win.getXSize()
		res_y = base.win.getYSize()
		show_select_frame_Z = self.allLbl[self.cPos].getPos()[1]+(self.allLbl[self.cPos].getScale()[1]/2.0)
		self.show_select_frame.setPos(self.text_x, 0, show_select_frame_Z)
		if self.prevRes != (base.win.getXSize(), base.win.getYSize()):
			self.reload_pause_GUI()
			self.prevRes = (base.win.getXSize(), base.win.getYSize())
	
	#WARNING: unload_pause_GUI only unloads GUI!
	# def unload_pause_GUI(self, task=None):
		# target  = []
		# target.append(self.pause_BGI)
		# target.append(self.show_select_frame)
		# for i in self.allLbl:
			# target.append(i)
		# for o in target:
			# o.remove_node()
		# self.cPos = 0
		# base.ignore('aspectRatioChanged')
		# base.ignore('arrow_down')
		# base.ignore('arrow_up')
	
	def unload_pause_GUI(self, task=None):
		target_node = render2d.findAllMatches("GUI_OBJ_PAUSE")
		for i in target_node:
			LerpColorScaleInterval(i, .5, (0, 0, 0, 0)).start()
		def remove_task(task):
			for i in target_node:
				i.remove_node()
		base.ignore('aspectRatioChanged')
		base.ignore('arrow_down')
		base.ignore('arrow_up')
		
		taskMgr.doMethodLater(1, remove_task, "unload_pause_GUI")
	
	def reload_pause_GUI(self):
		self.unload_pause_GUI()
		taskMgr.doMethodLater(.2, self.setup_pause_GUI, "setup_pause_GUI")