#!/usr/bin/env python
# -*- coding: utf-8 -*-
from MU_stdlib import *
import json, id3reader
from PIL import Image

sys.path.insert(0, "resources/modules/GUI/TreeGUI/")
from gui.core import GUI
from gui.keys import Keys
from themes.rtheme import RTheme
from gui.controls import *

import MU_GUI_layout

class Note:
	def __init__(self):
		base.cTrav = CollisionTraverser()
		self.collHandEvent = CollisionHandlerEvent()
		self.collHandEvent.addInPattern('into-%in')
		self.collHandEvent.addOutPattern('outof-%in')
		
	#Create Hit Box
	def createHitbox(self, object, InFunction=None, OutFunction=None, name='note', show=False):
		bound = object.getTightBounds()
		box = CollisionBox(bound[0],bound[1])
		# box.setPos(object.getPos())
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
	
	#Note creation related Func
	def createShortNote(self, line_num, function=None, speed=5, model_path='models/note', color=(1,1,1,1)):
		#Find note node, if it already available, Find that node and make using it.
		if render.find("note_node"):
			note_node = render.find("note_node")
		else:
			note_node = render.attachNewNode("note_node")

		line = -1.7 if line_num == 1 else -0.56 if line_num == 2 else 0.56 if line_num == 3 else 1.7
		pos_start = Point3(line, -1, -200)
		pos_end = Point3(line,-1, 50)

		note = loader.loadModel(model_path)

		if function:
			self.createHitbox(note, function)
		else:
			# self.createHitbox(note, self.event_dummy)
			self.createHitbox(note, None)
		
		note.setTag('note', 'short')
		note.reparentTo(note_node)
		note.setHpr(90, 0, 270)
		note.setPos(pos_start)
		note.setScale(.5)
		note.setTransparency(TransparencyAttrib.MAlpha)
		note.setColorScale(color)
		self.note_interval = note.posInterval(speed, pos_end)
		Sequence(self.note_interval, name=('note_short_'+randomID())).start()
	
	def createLongNote(self, line_num, start_function=None, mid_function=None, end_function=None, speed=5, model_path='models/note', color=(1,1,1,1)):
		if render.find("note_node"):
			note_node = render.find("note_node")
		else:
			note_node = render.attachNewNode("note_node")
		
		line = -1.7 if line_num == 1 else -0.56 if line_num == 2 else 0.56 if line_num == 3 else 1.7
		pos_start = Point3(line, -1, -200)
		pos_end = Point3(line,-1, 50)

		note_head = loader.loadModel('models/note_head')
		note_body = loader.loadModel('models/note_body')
		note_tail = loader.loadModel('models/note_tail')
		
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
	
	#MIDI to rhythm note
	def midi2seq(self, midiFile=None):
		song_start_event_used = False
		noteSeq = Sequence(name = 'midi2seq')
		if midiFile == None:
			file = midi.read_midifile('models/note_test.mid')
		else:
			file = midi.read_midifile(midiFile)
		bpm = 0
		pattern = list(file)
		resolution = file.resolution
		for i1 in pattern:
			for i2 in i1:
				if i2.name == 'Set Tempo':
					bpm = i2.get_bpm()
					tick_sec = ((60.0 * 1000000.0 / bpm) / resolution) / 1000000.0
				elif i2.name == 'Note On':
					if i2.tick:
						noteSeq.append(Wait(tick_sec * i2.tick))
					note = i2.data[0]
					if note in [67, 69, 71, 72]:
						line = 4 if note == 72 else 3 if note == 71 else 2 if note == 69 else 1
						if song_start_event_used:
							noteSeq.append(Func(self.createLongNote, line))
						else:
							noteSeq.append(Func(self.createLongNote, line, self.event_startMusic))
							song_start_event_used = True
					else:
						line = 4 if note == 65 else 3 if note == 64 else 2 if note == 62 else 1 if note == 60 else random.randrange(1, 5)
						if song_start_event_used:
							noteSeq.append(Func(self.createShortNote, line))
						else:
							noteSeq.append(Func(self.createShortNote, line, self.event_startMusic))
							song_start_event_used = True

				elif i2.name == 'Note Off':
					if i2.tick:
						noteSeq.append(Wait(tick_sec * i2.tick))
					note = i2.data[0]
					if note in [67, 69, 71, 72]:
						noteSeq.append(Func(self.endLongNote, line))
		return noteSeq

class Tunnel:
	def __init__(self, path='models/tunnel_road', speed=1, length=50, quantity=8):
		self.tunnel_model_value		= quantity
		self.tunnel_time			= speed
		self.tunnel_segment_length	= length
		self.path = path
	
	def tunnel_start(self):
		self.defineFog()
		self.initTunnel(path=self.path)
	
	def tunnel_close(self):
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
			#self.tunnel[x].setH(90)
			# self.tunnel[x].setScale(2)
			self.tunnel[x].setTransparency(True)
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

class Event:
	def event_dummy(self, collEntry):
		pass
	def event_missWall(self, collEntry):
		model = collEntry.getFromNodePath().getParent()
		if model.getTag('note') == 'short':
			model.removeNode()
	def event_short(self, collEntry):
		pass
	def event_startMusic(self, collEntry):
		# print collEntry
		print("Music started!")
		# music = loader.loadMusic('models/cirno_perfect_math_class.mp3')
		# Sequence(SoundInterval(music)).start()
	def event_touched(self, collEntry):
		print("Touched")

class GUI_define:
	def __init__(self):
		GUI(theme=RTheme("resources/modules/GUI/TreeGUI/data/r.png"))
		self.DEF_playing()
		#gui.addLayout(MU_GUI_layout.GUI_playing)
		
	def DEF_title(self):
		gui.addLayout(MU_GUI_layout.GUI_title)
	
	def DEF_selectSong(self):
		gui.addLayout(MU_GUI_layout.GUI_select)
	
	def DEF_playing(self):
		#MU_GUI_layout.GUI_playing.text_return_to_game = 
		gui.addLayout(MU_GUI_layout.GUI_playing)
	
	def DEF_pause(self):
		pass
	
	def DEF_score(self):
		gui.addLayout(MU_GUI_layout.GUI_title)

class Stage(Note):
	status_list = ["playing", "pause", "stop"]
	status = status_list[2]
	def __init__(self, json_path):
		song_info = json.loads(open(json_path).read())
		
		tunnel_path     = song_info["tunnel"]["model"]["path"]
		tunnel_length   = song_info["tunnel"]["model"]["length"]
		tunnel_speed    = song_info["tunnel"]["speed"]
		tunnel_quantity = song_info["tunnel"]["quantity"]
		self.tunnel = Tunnel(path    =tunnel_path,
							 speed   =tunnel_speed,
							 length  =tunnel_length,
							 quantity=tunnel_quantity)
		
		self.song_path = ''
		self.song_idv3 = id3reader.Reader(self.song_path)
		self.song_title  = self.song_idv3.getValue('title')
		self.song_artist = self.song_idv3.getValue('performer')
		self.song_album  = self.song_idv3.getValue('album')
		self.song_year   = self.song_idv3.getValue('year')
		# self.song_image  = self.song_idv3.getValue('year')
		self.pattern_path_dict = song_info["pattern"]
		
		
	def start(self):
		self.status = self.status_list[0]
		self.tunnel.tunnel_start()
	
	def resume(self):
		self.status = self.status_list[0]
		if self.tunnel.tunnelMove.isStopped():
			self.tunnel.tunnelMove.loop()
		else:
			pass
	
	def pause(self):
		self.status = self.status_list[1]
		if self.tunnel.tunnelMove.isPlaying():
			self.tunnel.tunnelMove.pause()
		else:
			pass
	
	def stop(self):
		self.status = self.status_list[2]
		self.tunnel.tunnel_close()
		self.tunnel = None
		model_list = render.find("note_node").findAllMatches("=note")
		for m in model_list:
			m.removeNode()
	
	def isPlaying(self):
		return True if self.status == self.status_list[0] else False
	def isPause(self):
		return True if self.status == self.status_list[1] else False
	def isPause(self):
		return True if self.status == self.status_list[2] else False

class Musica_main(Note):
	def __init__(self):
		Note.__init__(self)
		camera.setPosHpr(0, 12.5, 10, 0, -113, 0)
		
		self.credit_counter = 0
		
		Hitbox_missWall = loader.loadModel('models/hitbox_missWall')
		self.createHitbox(Hitbox_missWall, Event().event_missWall)
		Hitbox_missWall.setHpr(90, 0, 270)
		Hitbox_missWall.setPos(0, -1, 25)
		Hitbox_missWall.setScale(.5)
		Hitbox_missWall.reparentTo(render)
		
		s = loader.loadModel("smiley")
		s.setPos(0, -1, -10)
		self.createHitbox(s, InFunction=Event().event_touched)
		s.reparentTo(render)
		
		# base.accept("a", self.stageLoader)
		
		GUI_define()
		
		def test():
			for i in range(1, 5):
				self.createShortNote(i)
		Sequence(Func(test), Wait(2)).loop()
	
	def stageLoader(self):
		a = Stage("resources/song/melt/song_info.json")