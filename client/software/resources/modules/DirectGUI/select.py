#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from GUI_BASE import GUIbase

class Select(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		
		self.song_info_dict = {}
		#self.setup_select_GUI()
		#taskMgr.doMethodLater(.1, self.setup_select_GUI, "setup_select_GUI")
	
	def setup_select_GUI(self, task=None):
		self.GUI_OBJ = render2d.attachNewNode("GUI_OBJ_SELECT")
		#Timer Text
		self.timer_STR = OnscreenText(sort=-4,
									  text='90',
									  parent=self.GUI_OBJ,
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(.85, .775, 1),
									  scale=.25)
		
		#Select Mode Info
		self.a_Inf_STR = OnscreenText(sort=-4,
									  parent=self.GUI_OBJ,
									  text='모드를 선택해 주세요',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(-.25, .8, 1),
									  scale=.15)
		
		#Mode List
		self.m_Lst_S_1 = OnscreenText(sort=-4,
									  parent=self.GUI_OBJ,
									  text='4KEY SHORT',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(-.8, .4, 1),
									  scale=.1)
		self.m_Lst_S_2 = OnscreenText(sort=-4,
									  parent=self.GUI_OBJ,
									  text='4KEY LONG',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(-.8, .2, 1),
									  scale=.1)
		self.m_Lst_S_3 = OnscreenText(sort=-4,
									  parent=self.GUI_OBJ,
									  text='8KEY SHORT',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(-.8, .0, 1),
									  scale=.1)
		self.m_Lst_S_4 = OnscreenText(sort=-4,
									  parent=self.GUI_OBJ,
									  text='8KEY LONG',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(-.8, -.2, 1),
									  scale=.1)
		self.m_target_list = [self.m_Lst_S_1, self.m_Lst_S_2, self.m_Lst_S_3, self.m_Lst_S_4]
		for i in self.m_target_list:
			if i != self.m_Lst_S_1:
				i.setColorScale(1, 1, 1, .25)
		self.m_pos = 0
		self.s_Pos = 0
		
		#Selected Mode&Song Info
		self.s_Inf_Sart= OnscreenImage(sort=-3, #Album art
									  image='grid_white.png',
									  parent=self.GUI_OBJ,
									  pos =(.75, 0, .275),
									  scale=.15)
		self.s_Inf_Sart.setBin("opaque", 20)
		self.s_Inf_Sart.setDepthTest(False)
		self.s_Inf_Sart.setDepthWrite(False)
		self.s_Inf_Sngn = OnscreenText(sort=-4, #Song title name
									  parent=self.GUI_OBJ,
									  text='SONG_TITLE',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(.75, -.2, 1),
									  scale=.075)
		self.s_Inf_Satn = OnscreenText(sort=-4, #Artist name
									  parent=self.GUI_OBJ,
									  text='ARTIST_NAME',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(.75, -.325, 1),
									  scale=.075)
		self.s_Inf_Sabn = OnscreenText(sort=-4, #Album title name
									  parent=self.GUI_OBJ,
									  text='SONG_ALBUM',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(.75, -.45, 1),
									  scale=.075)
		
		#Controller Info
		self.c_Inf_STR = OnscreenText(sort=-4,
									  parent=self.GUI_OBJ,
									  text='◀ ▲ ▼ ▶ 로 선택',
									  fg=(1, 1, 1, 1),
									  font=self.font_koverwatch,
									  pos=(0, -.9, 1),
									  scale=.15)
		
		#Mode Select Frame
		self.m_select_frame  = OnscreenImage(image='grid_white.png',
											 parent=self.GUI_OBJ,
											 pos=(-.8, 0, .43),
											 scale=(.2, 0, .1))
		self.m_select_frame.setColorScale(1, 1, 1, 1)
		#Song Select Frame
		self.s_select_frame  = OnscreenImage(image='grid_white.png',
												parent=self.GUI_OBJ,
												pos=(-.8, 0, .43),
												scale=(.2, 0, .1))
		self.s_select_frame.setColorScale(1, 1, 1, 1)
		
		self.select_list_setup(self.song_info_dict)
		
		for o in render2d.findAllMatches("GUI_OBJ_SELECT/*"):
			o.setTransparency(1)
		
		self.resolutionChangeHandler_Select()
		base.accept('aspectRatioChanged', self.resolutionChangeHandler_Select)
		
		self.timeout_sfx = loader.loadSfx('resources/se/timeout.wav')
		
		target_node = render2d.findAllMatches("GUI_OBJ_SELECT")
		for i in target_node:
			LerpColorScaleInterval(i, .5, (1, 1, 1, 1), (1, 1, 1, 0)).start()
	
	def select_list_setup(self, input_dict):
		self.s_Lst_node = self.GUI_OBJ.attachNewNode('Scrollable_List')
		
		self.s_Lst_Lst = list()
		song_name_list = list()
		for o in input_dict['id_list'].items():
			song_name_list.append(o[1][0])
		
		list_quantity = len(input_dict['id_list'].items())
		center_num = self.s_Pos = int(list_quantity/2.1)
		center_num += 1 if list_quantity%2 else 0
		for i in range(list_quantity):
			title_text = (song_name_list[i][:6]) if len(song_name_list[i])> 7 else (song_name_list[i])
			self.s_Lst_Lst.append(OnscreenText(parent=self.GUI_OBJ,
											   font=self.font_SourceSans,
											   scale=.125,
											   pos=(0, (i-center_num)*-.25, 0),
											   fg=(1, 1, 1, 1),
											   text=title_text))
			self.s_Lst_Lst[i].setTag("songID", input_dict['id_list'].items()[i][0])
			if not i in range(center_num-2, center_num+3):
				self.s_Lst_Lst[i].setColorScale(1, 1, 1, 0)
		
		self.set_music_info(self.song_info_dict[self.s_Lst_Lst[center_num].getTag("songID")]['song_info'])
		
	def set_music_info(self, input_dict):
		try:
			self.s_Inf_Sart['image'] = 'resources/song/{0}/albumart.png'.format(input_dict['title'])
		except Exception as e:
			print e
		self.s_Inf_Sngn.setText(input_dict['title'])
		self.s_Inf_Satn.setText(input_dict['artist'])
		self.s_Inf_Sabn.setText(input_dict['album'])
	
	def resolutionChangeHandler_Select(self):
		res_x = base.win.getXSize()
		res_y = base.win.getYSize()
		s_Inf_Sart_x = .02/(1./res_x*.1)
		self.s_Inf_Sart.setScale((s_Inf_Sart_x)/(res_x), 0, ((s_Inf_Sart_x))/(res_y))
	
	#Remove select GUI resources
	def unload_select_GUI(self, task=None):
		try:
			taskMgr.remove('timerTask')
		except:
			pass
		target_node = render2d.findAllMatches("GUI_OBJ_SELECT")
		for i in target_node:
			LerpColorScaleInterval(i, .5, (0, 0, 0, 0)).start()
		def remove_task(task):
			for i in target_node:
				i.remove_node()
		base.ignore('aspectRatioChanged')
		
		taskMgr.doMethodLater(1, remove_task, "unload_select_GUI")
		try:
			center_num = int(len(self.s_Lst_Lst)/2.1)
			center_num += 1 if len(self.s_Lst_Lst)%2 else 0
			return self.s_Lst_Lst[center_num].getTag("songID")
		except:
			pass