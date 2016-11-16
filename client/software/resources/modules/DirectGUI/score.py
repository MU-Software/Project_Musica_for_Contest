#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from GUI_BASE import GUIbase
TEXT_CHAR_ANIM_TIME = 0.0075
TEXT_DEL_DELAY_TIME = 2.5
TEXT_ADD_DELAY_TIME = 0.2

class Score(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		
		self.score_target = 300000
		self.hit_count   = 24
		self.miss_count   = 50
		self.combo_count  = 36
		self.score_A_deadline = 280000
		self.score_B_deadline = 200000
		self.score_C_deadline = 100000
		self.score_D_deadline =  50000
		
		self.grade_list = [('GUEST', 30000),
						   ('GUEST', 25520),
						   ('GUEST', 26220),
						   ('GUEST', 1220),
						   ('GUEST', 0)]
		
		#self.setup_score_GUI()
		#taskMgr.doMethodLater(1, self.setup_score_GUI, "setup_score_GUI")
	
	def setup_score_GUI(self, task=None):
		try:
			taskMgr.remove("text_animation_task")
		except:
			pass
		self.score_current = 0
		self.score_deadline_pos = 0
		self.GUI_OBJ = render2d.attachNewNode("GUI_OBJ_SCORE")
		
		self.score_page_node = self.GUI_OBJ.attachNewNode("SCORE_NODE")
		self.score_meter = OnscreenText(parent=self.score_page_node,
								  text='0',
								  fg=(1, 1, 1, 1),
								  font=self.font_square2,
								  mayChange=True,
								  pos=(0, .4, 0),
								  scale=.25)
		
		self.score_deadline = [ ["A", self.score_A_deadline],
								["B", self.score_B_deadline],
								["C", self.score_C_deadline],
								["D", self.score_D_deadline]]
		self.score_grade_color_list = [
				( 1., .75,  .0, 1.),
				(.75, .75, .75, 1.),
				(.80,  .5,  .2, 1.),
				( .0, .37, 065, 1.)]
		self.score_grade = OnscreenText(parent=self.score_page_node,
								  text='F',
								  fg=(0, 0, .5, 1),
								  font=self.font_square2,
								  pos=(0, -.1, 0),
								  scale=.35)
		
		self.text_anim_pos = 0
		self.text_anim_stat= 0
		self.title_str_list     = ['P', 'R', 'E', 'S', 'S', ' ', 'A', 'N', 'Y', ' ', 'K', 'E', 'Y']
		self.title_str_int_list = [ 15,  17,   4,  18,  18, ' ',   0,  13,  24, ' ',  10,   4,  24]
		self.press_any_key_text = ''.join(self.title_str_list)
		self.label_press_any_key = OnscreenText(parent=self.GUI_OBJ,
											  text=self.press_any_key_text,
											  fg=(1, 1, 1, 1),
											  font=self.font_square,
											  shadow=(0, 0, 1, .75),
											  shadowOffset=(.0, .15),
											  mayChange=True,
											  pos=(0, -.5, 0),
											  frame=(0, 0, 0, 0))
		self.label_press_any_key.node().preserve_trailing_whitespace = 1
		self.label_press_any_key.setColorScale(1, 1, 1, 0)

		self.great_str = OnscreenText(parent=self.score_page_node,
								  text="COMBO: %03d" % self.combo_count,
								  fg=(1, 1, 1, 1),
								  font=self.font_square2,
								  shadow=(1, 0, 0, .75),
								  shadowOffset=(.0, .075),
								  pos=(.2, .15, 0),
								  scale=.08)
		self.good_str = OnscreenText(parent=self.score_page_node,
								  text="HIT  : %03d" % self.hit_count,
								  fg=(1, 1, 1, 1),
								  font=self.font_square2,
								  shadow=(1, 1, 0, .75),
								  shadowOffset=(.0, .075),
								  pos=(.2, .03, 0),
								  scale=.08)
		self.miss_str = OnscreenText(parent=self.score_page_node,
								  text="MISS : %03d" % self.miss_count,
								  fg=(1, 1, 1, 1),
								  font=self.font_square2,
								  shadow=(.5, .5, .5, 1),
								  shadowOffset=(.0, .075),
								  pos=(.2, -.09, 0),
								  scale=.08)
		self.user_game_count = [self.great_str, self.good_str, self.miss_str]
		for i in self.user_game_count:
			i.setColorScale(1, 1, 1, 0)
		
		#Next score page
		self.grade_text_list = list()
		self.grade_list = sorted(self.grade_list, key=lambda x: x[1])#JUST IN CASE
		self.grade_page_node = self.GUI_OBJ.attachNewNode('GRADE_NODE')
		for i, val in enumerate(reversed(self.grade_list)):
			if val[1]:
				self.grade_text_list.append([
											OnscreenText(
												parent=self.grade_page_node,
												text=unicode(str(i+1)),
												font=self.font_koverwatch,
												fg=(1, 1, 1, 1),
												pos=(-.65, .51-(i*.175), 0), 
												scale=.2
											), 
											OnscreenText(
												parent=self.grade_page_node,
												text=unicode(str(val[0])),
												font=self.font_koverwatch,
												fg=(1, 1, 1, 1),
												pos=(-.3, .51-(i*.175), 0), 
												scale=.2
											), 
											OnscreenText(
												parent=self.grade_page_node,
												text=unicode(str('%08d' % val[1])),
												font=self.font_square2,
												fg=(1, 1, 1, 1),
												pos=( .4, .51-(i*.175), 0), 
												scale=.125
											)])
		self.grade_page_node.setPos(2, 0, 0)
		
		base.accept('aspectRatioChanged', self.resolutionChangeHandler_Score)
		taskMgr.doMethodLater(1, self.score_updater_task, "score_updater_task")
	
	def score_updater_task(self, task):
		self.score_current += 600;
		self.score_meter['text'] = str(self.score_current)
		if self.score_deadline_pos < 4:
			if self.score_current > [k[1] for k in self.score_deadline][3-self.score_deadline_pos]:
				self.score_grade['text'] = [k[0] for k in self.score_deadline][3-self.score_deadline_pos]
				self.score_grade['fg'] = self.score_grade_color_list[3-self.score_deadline_pos]
				Parallel(
					LerpScaleInterval(self.score_grade, .5, 1.1, startScale=2),
					LerpColorScaleInterval(self.score_grade, .5, (1, 1, 1, 1), startColorScale=(0, 0, 0, 0))).start()
				self.score_deadline_pos += 1
		if self.score_target - self.score_current < 600:
			self.score_current += self.score_target - self.score_current;
			self.score_meter['text'] = str(self.score_current)
			show_anim_seq = Sequence()
			show_anim_seq.append(LerpPosInterval(self.score_grade, .25, (-.36, 0, 0)))
			for i in self.user_game_count:
				show_anim_seq.append(LerpColorScaleInterval(i, .25, (1, 1, 1, 1)))
			show_anim_seq.append(Wait(1))
			show_anim_seq.append(LerpColorScaleInterval(self.label_press_any_key, 1, (1, 1, 1, 1)))
			show_anim_seq.start()
			taskMgr.doMethodLater(4, self.text_animation_del_task, "text_animation")
			return
		taskMgr.doMethodLater(.01, self.score_updater_task, "score_updater_task")
	
	def score_page_scroll(self):
		Parallel(
				LerpPosInterval(self.score_page_node, .25, (-2, 0, 0)),
				LerpPosInterval(self.grade_page_node, .25, (0, 0, 0))
				).start()
	
	#Text animation tasks
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

		self.press_any_key_text = ''.join(self.title_str_list)
		self.label_press_any_key.setText(self.press_any_key_text)
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
		
		self.press_any_key_text = ''.join(self.title_str_list)
		self.label_press_any_key.setText(self.press_any_key_text)
		taskMgr.doMethodLater(TEXT_CHAR_ANIM_TIME, self.text_animation_add_task, 'text_animation_task')
	
	def resolutionChangeHandler_Score(self):
		res_x = base.win.getXSize()
		res_y = base.win.getYSize()
	
	def unload_score_GUI(self, task=None):
		try:
			taskMgr.remove("text_animation_task")
			taskMgr.remove("score_updater_task")
		except:
			pass
		target_node = render2d.findAllMatches("GUI_OBJ_SCORE")
		for i in target_node:
			LerpColorScaleInterval(i, .5, (0, 0, 0, 0)).start()
		def remove_task(task):
			for i in target_node:
				i.remove_node()
		base.ignore('aspectRatioChanged')
		
		taskMgr.doMethodLater(1, remove_task, "unload_score_GUI")