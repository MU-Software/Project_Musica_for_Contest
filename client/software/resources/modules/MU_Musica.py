#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Project Musica main definition module
import json
try:
	from . import *
except:
	pass
from __init__ import *
from MU_GUI import *
COMBO_TEXT = \
"""\
COMBO
{0}\
"""

def randomID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def toggleInterval(interval):
	if interval.isPlaying():
		interval.pause()
	else:
		interval.resume()

class MU_Musica(MU_GUI):
	def __init__(self):
		base.cTrav = CollisionTraverser()
		self.collHandEvent = CollisionHandlerEvent()
		self.collHandEvent.addInPattern('into-%in')
		self.collHandEvent.addOutPattern('outof-%in')
		MU_GUI.__init__(self)
		
		self.song_info = json.load(open('resources/song/song_info.json', 'rb'))
		self.select.song_info_dict = self.song_info
		
		self.keyStat = {
						'collBox_1' : False,
						'collBox_2' : False,
						'collBox_3' : False,
						'collBox_4' : False
						}
		self.startup_musica()
		
		
		base.accept("o", self.setup_in_game, ["MUSICA_0002"])
	
	#GUI Controller
	def GUI_mgr(self, mode):
		if   mode == 't2s':
			self.title.unload_title_GUI()
			taskMgr.doMethodLater(1, self.select.setup_select_GUI, "GUI_select_create")
			taskMgr.doMethodLater(1, self.give_select_control, "give_select_control")
			taskMgr.doMethodLater(1.5, self.timerTask, "timerTask")
			base.ignore('tab')
		elif mode == 's2p':
			(self.select.unload_select_GUI())
		elif mode == '':
			pass
	def title_coin_text_mgr(self, val):
		self.credit_updater(val)
		try:
			if self.title.credit_return() >= 3 and self.title.title_str_int_list != [15,17,4,18,18,' ',0,13,24,' ',10,4,24]:
				self.title.text_animation_change()
				base.accept('tab', self.GUI_mgr, ['t2s'])
			elif self.title.credit_return() < 3 and self.title.title_str_int_list != [8,13,18,4,17,19,' ',2,14,8,13,'(',18,')']:
				self.title.text_animation_change('INSERT COIN(S)')
				base.ignore('tab')
		except:
			pass
	def give_select_control(self, task=None):
		base.accept("arrow_up"  , self.mode_select_movement_arrow, [-1])
		base.accept("arrow_down", self.mode_select_movement_arrow, [+1])
		base.accept("time-arrow_up-repeat"  , self.mode_select_movement_arrow, [-1])
		base.accept("time-arrow_down-repeat", self.mode_select_movement_arrow, [+1])
		base.accept("arrow_left", self.menu_to_song, ['S2M'])
		base.accept("arrow_right", self.menu_to_song, ['M2S'])
	def mode_select_movement_arrow(self, pos, Long_Hold_Dummy=None):
		pos = 3 if (self.select.m_pos < 1 and pos < 0)\
					else -3 if (self.select.m_pos > 3-1 and pos > 0)\
					else pos
		self.mode_select_movement(self.select.m_pos + pos)
	def mode_select_movement(self, num):
		select_movement_seq_list  = Parallel(name="select_movement_seq")
		main_target = self.select.m_target_list[num]
		main_target_pos = main_target.getPos()
		not_target  = [i for i in self.select.m_target_list if not i == main_target]
		select_movement_seq_list.append(LerpColorScaleInterval(main_target, .25,  VBase4(1, 1, 1, 1)))
		select_movement_seq_list.append(
			self.select.m_select_frame.posInterval(.1, (main_target_pos[0], 0, main_target_pos[1]+.035)))
		select_movement_seq_list.append(
			self.select.s_select_frame.posInterval(.1, (main_target_pos[0], 0, main_target_pos[1]+.035)))
		for i in not_target:
			select_movement_seq_list.append(LerpColorScaleInterval(i, .1,  VBase4(1, 1, 1, .25)))
		self.select.m_pos = num
		select_movement_seq_list.start()
	def menu_to_song(self, way):
		main_target = self.select.m_target_list[self.select.m_pos]
		main_target_pos = main_target.getPos()
		seq = Parallel(name="menu_to_song")
		if way == 'M2S':
			self.select.a_Inf_STR["text"] = u"노래를 선택해 주세요"
			pos = (-.05, 0, .05)
			scale = (.55, 0, .125)
			base.ignore("arrow_up")
			base.ignore("arrow_down")
			base.ignore("time-arrow_up-repeat")
			base.ignore("time-arrow_down-repeat")
			base.accept("arrow_up"  , self.song_select_movement, [-1])
			base.accept("arrow_down", self.song_select_movement, [+1])
			base.accept("time-arrow_up-repeat"  , self.song_select_movement, [-1])
			base.accept("time-arrow_down-repeat", self.song_select_movement, [+1])
			base.accept("arrow_left", self.menu_to_song, ['S2M'])
			base.accept("arrow_right", self.select_to_play)

		else:
			self.select.a_Inf_STR["text"] = u"모드를 선택해 주세요"
			pos = self.select.m_select_frame.getPos()
			scale = self.select.m_select_frame.getScale()
			base.ignore("arrow_up")
			base.ignore("arrow_down")
			base.ignore("time-arrow_up-repeat")
			base.ignore("time-arrow_down-repeat")
			base.accept("arrow_up"  , self.mode_select_movement_arrow, [-1])
			base.accept("arrow_down", self.mode_select_movement_arrow, [+1])
			base.accept("time-arrow_up-repeat"  , self.mode_select_movement_arrow, [-1])
			base.accept("time-arrow_down-repeat", self.mode_select_movement_arrow, [+1])
			base.accept("arrow_left", self.menu_to_song, ['S2M'])
			base.accept("arrow_right", self.menu_to_song, ['M2S'])

		seq.append(self.select.s_select_frame.posInterval(.1, pos))
		seq.append(LerpScaleInterval(self.select.s_select_frame, .1, scale))
		seq.start()
	def song_select_movement(self, pos, Long_Hold_Dummy=None):
		#if 7, return 3; if 8, return 3.
		center_num = int(len(self.select.s_Lst_Lst)/2.1)
		center_num += 1 if len(self.select.s_Lst_Lst)%2 else 0
		if pos > 0:
			self.select.s_Lst_Lst.append(self.select.s_Lst_Lst[0])
			self.select.s_Lst_Lst = self.select.s_Lst_Lst[1:]
			for i in range(len(self.select.s_Lst_Lst))[::-1]:
				if i != 0:
					self.select.s_Lst_Lst[i-1].getPos()[1]
					self.select.s_Lst_Lst[i].setPos(0, self.select.s_Lst_Lst[i-1].getPos()[1])
				else:
					self.select.s_Lst_Lst[i].setPos(0, .5)
				if not i in range(center_num-2, center_num+3):
					self.select.s_Lst_Lst[i].setColorScale(1, 1, 1, 0)
				else:
					self.select.s_Lst_Lst[i].setColorScale(1, 1, 1, 1)
		
		elif pos < 0:
			self.select.s_Lst_Lst.insert(0, self.select.s_Lst_Lst[-1])
			self.select.s_Lst_Lst = self.select.s_Lst_Lst[:-1]
			for i in range(len(self.select.s_Lst_Lst))[::1]:
				if i != len(self.select.s_Lst_Lst)-1:
					self.select.s_Lst_Lst[i].setPos(0, self.select.s_Lst_Lst[i+1].getPos()[1])
				else:
					self.select.s_Lst_Lst[i].setPos(0, -.5)
				if not i in range(center_num-2, center_num+3):
					self.select.s_Lst_Lst[i].setColorScale(1, 1, 1, 0)
				else:
					self.select.s_Lst_Lst[i].setColorScale(1, 1, 1, 1)
		else: return;
		
		self.select.set_music_info(self.select.song_info_dict[self.select.s_Lst_Lst[center_num].getTag("songID")]['song_info'])
		
		self.select.s_Pos += pos;
		if self.select.s_Pos > len(self.select.s_Lst_Lst) - 1:
			self.select.s_Pos = 0
		elif self.select.s_Pos < 0:
			self.select.s_Pos = len(self.select.s_Lst_Lst) -1
	def select_to_play(self):
		unload_returner = self.select.unload_select_GUI()
		if unload_returner.strip():
			self.setup_in_game(unload_returner)

	def startup_musica(self):
		camera.setPosHpr(0, 12.5, 10, 0, -113, 0)
		#First, create hitbox that detects miss.
		self.Hitbox_missWall = loader.loadModel('hitbox_missWall')
		self.createHitbox(self.Hitbox_missWall, self.event_missWall)
		self.Hitbox_missWall.setHpr(90, 0, 270)
		self.Hitbox_missWall.setPos(0, -1, -5)
		self.Hitbox_missWall.setScale(1, 1.25, .25)
		self.Hitbox_missWall.reparentTo(hidden)
		
		#Second, create hitbox that will be controlled by player.
		self.Hitbox_user_list = list()
		for i in range(4):
			self.Hitbox_user_list.append(loader.loadModel('hitbox_user.egg'))
			self.Hitbox_user_list[i].setTag('name', ('collBox_{0}'.format(i+1)))
			self.createHitbox(self.Hitbox_user_list[i], self.event_success, self.event_success)
			self.Hitbox_user_list[i].reparentTo(hidden)
			self.Hitbox_user_list[i].setPos((.6*(-1+i)-.275)*5, -2, -15)
			self.Hitbox_user_list[i].setScale(2, .3, 3)
			self.Hitbox_user_list[i].setColor(0, 0, 0, 1)
		
		self.Hitbox_music_start = loader.loadModel('hitbox_missWall')
		self.createHitbox(self.Hitbox_music_start, self.event_startMusic)
		self.Hitbox_music_start.setHpr(90, 0, 270)
		self.Hitbox_music_start.setTransparency(1)
		self.Hitbox_music_start.setPos(0, -1, -16)
		self.Hitbox_music_start.setScale(1, 1.25, 1)
		self.Hitbox_music_start.setColor(0, 0, 0, 0)
		self.Hitbox_music_start.reparentTo(render)
		
		#Third, load SFX.
		self.play_input = loader.loadSfx('resources/se/play_input_short.wav')
		self.play_input.setVolume(0.1)
		
		base.accept('a', self.keyToBool, ['collBox_1', True])
		base.accept('d', self.keyToBool, ['collBox_2', True])
		base.accept('j', self.keyToBool, ['collBox_3', True])
		base.accept('l', self.keyToBool, ['collBox_4', True])
		base.accept('a-up', self.keyToBool, ['collBox_1', False])
		base.accept('d-up', self.keyToBool, ['collBox_2', False])
		base.accept('j-up', self.keyToBool, ['collBox_3', False])
		base.accept('l-up', self.keyToBool, ['collBox_4', False])
	
	#IN-Game function
	def loadBackground(self):
		self.background = OnscreenImage(parent=render2dp, image="galaxy.png")
		self.background.setTransparency(1)
		self.background.setColorScale(.5, .5, .5, .75)
		base.cam2dp.node().getDisplayRegion(0).setSort(-20)
	def setup_in_game(self, songID):
		self.loadBackground()
		self.pattern = self.patternLoader('resources/song/{0}/pattern.json'.format(self.song_info['id_list'][songID][0]))
		self.music = loader.loadMusic('resources/song/{0}/music.wav'.format(self.song_info['id_list'][songID][0]))
		self.music.stop()
		for i in self.Hitbox_user_list:
			i.reparentTo(render)
		self.Hitbox_missWall.reparentTo(render)
		self.select.unload_select_GUI()
		self.play.setup_play_GUI()
		LerpColorScaleInterval(self.title.GUI_BGI, .5, (0, 0, 0, 0)).start()
		self.tunnel = Tunnel(self.song_info[songID]['tunnel']['path'],
							 self.song_info[songID]['tunnel']['speed'])
		self.tunnel.start()
		
		self.score.score_A_deadline = self.song_info[songID]['score_deadline']['A']
		self.score.score_B_deadline = self.song_info[songID]['score_deadline']['B']
		self.score.score_C_deadline = self.song_info[songID]['score_deadline']['C']
		self.score.score_D_deadline = self.song_info[songID]['score_deadline']['D']
	def unload_in_game(self):
		for i in self.Hitbox_user_list:
			i.reparentTo(hidden)
		self.Hitbox_missWall.reparentTo(hidden)
		self.play.unload_play_GUI()
		self.tunnel.close()
		LerpColorScaleInterval(self.title.GUI_BGI, .5, (1, 1, 1, 1)).start()
		
		self.score.score_target = self.play.score_val
		self.score.hit_count    = self.play.highest_combo_count
		self.score.miss_count   = self.play.miss_count
		self.score.combo_count  = self.play.combo_count
		self.score.unload_score_GUI()
		self.score.setup_score_GUI()
		def score_to_select():
			if self.title.credit_return():
				self.score.unload_score_GUI()
				self.select.setup_select_GUI()
				self.give_select_control()
				self.title_coin_text_mgr(self.title.credit_return()-1)
				base.ignore('tab')
			else:
				self.end.setup_end_GUI()
		base.accept('tab', score_to_select)
	def patternLoader(self, path=None):
		pattern_open = json.load(open(path, 'r'))
		pattern_seq = Sequence(name='pattern_sequence')
		pattern = sorted(pattern_open, key=lambda x: float(x.keys()[0]))
		
		pattern_seq.append(Func(self.createShortNote, 2, None, 2.5, 'note', (0, 0, 0, 0)))
		
		current_time = 0.
		for i, val in enumerate(pattern):
			if current_time == float(val.keys()[0]):
				pass
			else:
				pattern_seq.append(Wait(float(val.keys()[0]) - current_time))
				current_time = float(val.keys()[0])
			
			if val.values()[0].keys()[0] == 'shortNote':
				pattern_seq.append(Func(self.createShortNote, val.values()[0][val.values()[0].keys()[0]]))
		pattern_seq.start()
		print pattern_seq
		return pattern_seq
	def keyToBool(self, mapKey, status):
		self.keyStat[mapKey] = status
		if status:
			self.Hitbox_user_list[int(mapKey[-1:])-1].setColor(0, 0, 1, 1)
			def mk_false_task(target):
				self.keyStat[target] = False
				self.Hitbox_user_list[int(target[-1:])-1].setColor(0, 0, 0, 1)
			taskMgr.doMethodLater(.5, mk_false_task, 'mk_false_task_{0}'.format(mapKey), extraArgs = [mapKey])
		else:
			self.Hitbox_user_list[int(mapKey[-1:])-1].setColor(0, 0, 0, 1)
			taskMgr.remove('mk_false_task_{0}'.format(mapKey))
		self.play_input.play() if status else None
	def stage_ender(self, task):
		if self.music.status() == self.music.READY:
			print("END")
			self.unload_in_game()
			return task.done
		return task.cont
	
	#Universal
	def createHitbox(self, object, InFunction=None, OutFunction=None, name='note', show=False):
		bound = object.getTightBounds()
		box = CollisionBox(bound[0],bound[1])
		collName = 'Collision_{0}_{1}'.format(name, randomID())
		cnodePath = object.attachNewNode(CollisionNode(collName))
		cnodePath.node().addSolid(box)
		
		base.cTrav.addCollider(cnodePath, self.collHandEvent)
		if InFunction:
			base.accept('into-' + collName, InFunction)
		if OutFunction:
			base.accept('outof-' + collName, OutFunction)
		if show:
			cnodePath.show()
	
	#Note
	def createShortNote(self, line_num, function=None, speed=2.5, model_path='note', color=(1,0,1,1)):
		#Find note node, if it already available, Find that node and make using it.
		if render.find("note_node"):
			note_node = render.find("note_node")
		else:
			note_node = render.attachNewNode("note_node")

		line = -4.7 if line_num == 1 else -1.5 if line_num == 2 else 1.7 if line_num == 3 else 4.9
		pos_start = Point3(line, -2, -200)
		pos_end = Point3(line, -2, 50)

		note = loader.loadModel(model_path)

		if function:
			self.createHitbox(note, function)
		else:
			self.createHitbox(note, None)
		
		note.setTag('note', 'short')
		note.reparentTo(note_node)
		note.setHpr(90, 0, 270)
		note.setPos(pos_start)
		note.setColorScale(1, 0, 1, 1)
		note.setScale(1.45)
		note.setTransparency(TransparencyAttrib.MAlpha)
		note.setColorScale(color)
		self.note_interval = note.posInterval(speed, pos_end)
		Sequence(self.note_interval, name=('note_short_'+randomID())).start()
	def createLongNote(self, line_num, start_function=None, mid_function=None, end_function=None, speed=2.5, model_path='note', color=(1,1,1,1)):
		if render.find("note_node"):
			note_node = render.find("note_node")
		else:
			note_node = render.attachNewNode("note_node")
		
		line = -4.5 if line_num == 1 else -1.5 if line_num == 2 else 1.5 if line_num == 3 else 4.5
		pos_start = Point3(line, -2, -200)
		pos_end = Point3(line,-2, 50)

		note_head = loader.loadModel('note_head')
		note_body = loader.loadModel('note_body')
		note_tail = loader.loadModel('note_tail')
		
		if start_function:
			self.createHitbox(note_head, start_function)
		else:
			self.createHitbox(note_head, self.event_dummy)

		if mid_function:
			self.createHitbox(note_body, mid_function)
		else:
			pass
		
		if end_function:
			self.createHitbox(note_tail, end_function)
		else:
			self.createHitbox(note_tail, self.event_dummy)
		
		self.createHitbox(note_head, self.event_dummy)
		self.createHitbox(note_tail, self.event_dummy)
		note_head.setTag('note', 'head_{0}'.format(line_num))
		note_body.setTag('note', 'body_{0}'.format(line_num))
		note_tail.setTag('note', 'tail_{0}'.format(line_num))
		note_head.reparentTo(note_node)
		note_body.reparentTo(note_node)
		note_tail.reparentTo(note_node)
		note_head.setHpr(90, 0, 270)
		note_body.setHpr(90, 0, 270)
		note_tail.setHpr(90, 0, 270)
		note_head.setTransparency(TransparencyAttrib.MAlpha)
		note_body.setTransparency(TransparencyAttrib.MAlpha)
		note_tail.setTransparency(TransparencyAttrib.MAlpha)
		note_head.setPos(pos_start)
		note_body.setPos(pos_start)
		note_tail.setPos(pos_start)
		note_head.setColorScale(color)
		note_body.setColorScale(color)
		note_tail.setColorScale(color)
		note_head.setScale(.5)
		note_body.setScale(.5)
		note_tail.setScale(.5)
		
		head_interval = Parallel(note_head.posInterval(speed, pos_end),
								 name=('note_long_head_{0}_{1}'.format(line_num, randomID())))
		body_interval = Parallel(note_body.posInterval(speed*2, pos_end),
								 note_body.scaleInterval(speed*2, (499, 0.5, 0.5)),
								 name=('note_long_body_create_{0}_{1}'.format(line_num, randomID())))
		head_interval.start()
		body_interval.start()
	def endLongNote(self, line_num):
		body_interval_list = ivalMgr.getIntervalsMatching('note_long_body_create_{0}_*'.format(line_num))
		for i in body_interval_list:
			i.pause()
			i = None
		note_node = render.find("note_node")
		# head = note_node.find('=note=head_*')
		body = note_node.find('=note=body_{0}'.format(line_num))
		tail = note_node.find('=note=tail_{0}'.format(line_num))
		body_interval = Parallel(body.posInterval(self.note_speed, (body.getX(), body.getY(), body.getZ()+250)),
								 name=('note_long_body_{0}_{1}'.format(line_num, randomID())))
		tail_interval = Parallel(tail.posInterval(self.note_speed, Point3(tail.getX(),-1, 50)),
								 name=('note_long_tail_{0}_{1}'.format(line_num, randomID())))
		body_interval.start()
		tail_interval.start()
	
	#Events
	def event_dummy(self, collEntry):
		pass
	def event_missWall(self, collEntry):
		model = collEntry.getFromNodePath().getParent()
		collName = collEntry.getFromNodePath().getNode(0).getName()
		self.play.combo_count = 0
		self.play.miss_updater(1)
		self.play.set_combo_text('MISS')
		base.ignore('into-' + collName)
		model.removeNode()
	def event_startMusic(self, collEntry):
		Hitbox_node = collEntry.getIntoNodePath().getParent()
		Note_node = collEntry.getFromNodePath().getParent()
		if Note_node.getTag('note') == 'short':
			Hitbox_node.removeNode()
			Note_node.removeNode()
			self.music.play()
			taskMgr.add(self.stage_ender, 'stage_ender')
	def event_success(self, collEntry):
		Hitbox_node = collEntry.getIntoNodePath().getParent()
		Hitbox_tag = Hitbox_node.getTag('name')
		if self.keyStat[Hitbox_tag]:
			model = collEntry.getFromNodePath().getParent()
			collName = collEntry.getFromNodePath().getNode(0).getName()
			self.play.combo_count += 1
			self.play.hit_count   += 1
			self.play.score_updater(200)
			self.play.set_combo_text(COMBO_TEXT.format(self.play.combo_count))
			if model.getTag('note') == 'short':
				base.ignore('into-' + collName)
				model.removeNode()

#MIDI to JSON exporter
class midi2pattern:
	def convert(self, path=None, enable_long_using_tick=False):
		noteSeq = list()
		def event(time, event_func, args=None):
			return {str(time) : {str(event_func) : args}}
		event_templete = dict()
		file = midi.read_midifile(path)
		bpm = 0
		current_timeline = 0.
		pattern = list(file)
		resolution = file.resolution
		
		for i1 in pattern:
			for i2 in i1:
				if i2.name == 'Set Tempo':
					bpm = i2.get_bpm()
					tick_sec = ((60.0 * 1000000.0 / bpm) / resolution) / 1000000.0
				elif i2.name == 'Note On':
					if i2.tick:
						current_timeline += tick_sec * i2.tick
					note = i2.data[0]
					if (note in [67, 69, 71, 72]) or (i2.tick > 60 and enable_long_using_tick):
						print "LONG"
						line = 4 if note == 72 else 3 if note == 71 else 2 if note == 69 else 1
						noteSeq.append(event(current_timeline, 'longNote_Start', line))
					else:
						line = 4 if note == 65 else 3 if note == 64 else 2 if note == 62 else 1 if note == 60 else random.randrange(1, 5)
						noteSeq.append(event(current_timeline, 'shortNote', line))

				elif i2.name == 'Note Off':
					if i2.tick:
						current_timeline += tick_sec * i2.tick
					note = i2.data[0]
					if note in [67, 69, 71, 72]:
						noteSeq.append(event(current_timeline, 'longNote_End'))
		return noteSeq

class Tunnel:
	def __init__(self, path='tunnel_default.egg', speed=1, length=50, quantity=8):
		self.tunnel_model_value		= quantity
		self.tunnel_time			= speed
		self.tunnel_segment_length	= length
		self.path = path
		
		#for pausing tunnel
		self.pause = (lambda:toggleInterval(self.tunnelMove))
	
	def start(self):
		self.defineFog()
		self.initTunnel(path=self.path)
	
	def close(self):
		if self.tunnelMove.isPlaying():
			self.tunnelMove.finish()
		else:
			pass
		model_list= render.findAllMatches("=tunnel")
		for m in model_list:
			m.removeNode()
	
	#Tunnel related Func
	def defineFog(self):
		self.fog = Fog('distanceFog')
		self.fog.setColor(0)
		self.fog.setExpDensity(.01)
		render.setFog(self.fog)
	
	def initTunnel(self, path, tag='normal'):
		self.tunnel = [None] * (self.tunnel_model_value + 1)
		for x in range(self.tunnel_model_value + 1):
			self.tunnel[x] = loader.loadModel(path)
			self.tunnel[x].setTag('tunnel',tag)
			self.tunnel[x].setColor(1, 1, 1)
			self.tunnel[x].setTransparency(True)
			self.tunnel[x].setColorScale(1, 1, 1, .99)
			#self.tunnel[x].setRenderModeWireframe(True)
			if x == 0:
				self.tunnel[x].reparentTo(render)
			else:
				self.tunnel[x].reparentTo(self.tunnel[x - 1])
			self.tunnel[x].setPos(0, 0, -self.tunnel_segment_length)
		self.contTunnel()
	
	def contTunnel(self):
		self.tunnel = self.tunnel[1:] + self.tunnel[0:1]
		self.tunnel[0].setZ(0)
		#self.tunnel[0].setP(90)
		self.tunnel[0].reparentTo(render)
		self.tunnel[0].setScale(.155, .155, .305)
		for i in range(self.tunnel_model_value, 0, -1):
			self.tunnel[i].reparentTo(self.tunnel[i - 1])
		self.tunnel[self.tunnel_model_value].setZ(-self.tunnel_segment_length)
		self.tunnel[self.tunnel_model_value].setScale(1)
		self.tunnelMove = Sequence(
			LerpFunc(self.tunnel[0].setZ,
					 duration=self.tunnel_time,
					 fromData=0,
					 toData=self.tunnel_segment_length * .305),
			# Func(self.contTunnel),
			name='note_tunnel')
		self.tunnelMove.loop()