#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2016 MU Software(@MUsoftware on twitter), All Rights Reserved.
import sys; sys.dont_write_bytecode = True
import random, string, json, zipfile, argparse, time, midi
from panda3d.core import *
reload (sys)
loadPrcFile("config.prc")
sys.setdefaultencoding('utf-8')
from direct.task.Task import Task
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.interval.MetaInterval import Sequence
from direct.interval.MetaInterval import Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
from direct.showbase.Transitions import Transitions
from direct.showbase.DirectObject import DirectObject
#Short Note 1 = 60
#Short Note 2 = 62
#Short Note 3 = 64
#Short Note 4 = 65
#Long  Note 1 = 67
#Long  Note 2 = 69
#Long  Note 3 = 71
#Long  Note 4 = 72
#Short Note random = 59

TUNNEL_SEGMENT_LENGTH = 50
TUNNEL_TIME = 0.5
TUNNEL_MODEL_VALUE = 20

def randomID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class demo(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()
		base.setBackgroundColor(0, 0, 0)
		camera.setPosHpr(0, 3, 10, 0, -100, 0)
		base.camLens.setFov(30)
		self.ingameSetup()
		self.note_speed = 5
		self.accept('escape', self.handlePause)
		self.accept('=', sys.exit)
		self.accept('0', self.midi2seq)
		self.accept('r', render.ls)
		self.startUp()
		# Sequence(Func(self.startUp), Wait(15), Func(lambda: self.loadingScreen(self.hardWork))).start()
	def setKey(self, key, value):
		self.keyMap[key] = value
		
	def hardWork(self):
		a = 2
		b = 0
		for i in range(100000):
			b += a**i
	def ingameSetup(self):
		base.cTrav = CollisionTraverser()
		self.collHandEvent = CollisionHandlerEvent()
		self.collHandEvent.addInPattern('into-%in')
		self.collHandEvent.addOutPattern('outof-%in')
		
		self.keyMap = {
						 'user_note_1': False,
						 'user_note_2': False,
						 'user_note_3': False,
						 'user_note_4': False,
						 'GUI_UP'     : False,
						 'GUI_DOWN'   : False,
						 'GUI_LEFT'   : False,
						 'GUI_RIGHT'  : False,
						 # '': False,
						 'escape': False}
		# skybox = self.loader.loadModel("models/skybox_1024")
		# skybox.reparentTo(self.camera)
		# skybox.set_two_sided(True)
		# skybox.setScale(.1)
		# skybox.set_bin("background", 0)
		# skybox.set_depth_write(False)
		# skybox.set_compass()

		# b=OnscreenImage(parent=render2dp, image='models/city_night_fix.jpg')
		# base.cam2dp.node().getDisplayRegion(0).setSort(-50)
		
		self.font_koverwatch= loader.loadFont('models/koverwatch.ttf')
		self.font_koverwatch.setPixelsPerUnit(120)

		self.mainFrame = DirectFrame(frameColor=(1, 1, 1, 0),
							  image = 'models/MU_software_logo_background.png',
							  pos=(0, 0, 0),
							  sortOrder=-1,
							  parent=render2d)
		self.mainFrame.setTransparency(TransparencyAttrib.MAlpha)
		self.mainFrame.setColorScale(0, 0, 0, 1)

		self.transition = Transitions(loader)
		self.transition.setFadeColor(0, 0, 0)

		self.defineFog()
		self.initTunnel()

		self.mainLabel = DirectLabel(frameColor=(1, 1, 1, 0),
							  text='',
							  text_fg=(1,1,1,1),
							  text_font=self.font_koverwatch,
							  textMayChange=1,
							  pos=(0, 0, 0),
							  scale=(.1,.1,.1),
							  sortOrder=1,
							  parent=render2d)

		Hitbox_missWall = loader.loadModel('models/hitbox_missWall')
		self.createHitbox(Hitbox_missWall, self.event_missWall)
		Hitbox_missWall.setHpr(90, 0, 270)
		Hitbox_missWall.setPos(0, -1, 25)
		Hitbox_missWall.setScale(.5)
		Hitbox_missWall.reparentTo(render)

		self.user_note = [None, None, None, None]
		for i in range(4):
			x = -1.7 if i == 0 else -0.56 if i == 1 else 0.56 if i == 2 else 1.7
			self.user_note[i] = loader.loadModel('models/hitbox_user')
			self.user_note[i].setScale(.4)
			self.user_note[i].setPos( x, -1, -1000)
			self.user_note[i].reparentTo(render)
			self.createHitbox(self.user_note[i], self.event_touched)
		
		self.accept(   'z', self.user_note[0].setZ, [0])
		self.accept(   'x', self.user_note[1].setZ, [0])
		self.accept(   '.', self.user_note[2].setZ, [0])
		self.accept(   '/', self.user_note[3].setZ, [0])
		self.accept('z-up', self.user_note[0].setZ, [1000])
		self.accept('x-up', self.user_note[1].setZ, [1000])
		self.accept('.-up', self.user_note[2].setZ, [1000])
		self.accept('/-up', self.user_note[3].setZ, [1000])

	#Tunnel related Func
	def defineFog(self):
		self.fog = Fog('distanceFog')
		self.fog.setColor(0)
		self.fog.setExpDensity(.01)
		render.setFog(self.fog)
	def initTunnel(self, tag='normal'):
		self.tunnel = [None] * (TUNNEL_MODEL_VALUE + 1)
		for x in range(TUNNEL_MODEL_VALUE + 1):
			self.tunnel[x] = loader.loadModel('models/tunnel_road')
			self.tunnel[x].setTag('tunnel',tag)
			self.tunnel[x].setColor(1, 1, 1)
			self.tunnel[x].setTransparency(True)
			if x == 0:
				self.tunnel[x].reparentTo(render)
			else:
				self.tunnel[x].reparentTo(self.tunnel[x - 1])
			self.tunnel[x].setPos(0, 0, -TUNNEL_SEGMENT_LENGTH)
		self.contTunnel()
	def contTunnel(self):
		self.tunnel = self.tunnel[1:] + self.tunnel[0:1]
		self.tunnel[0].setZ(0)
		self.tunnel[0].reparentTo(render)
		self.tunnel[0].setScale(.155, .155, .305)
		for i in range(TUNNEL_MODEL_VALUE, 0, -1):
			self.tunnel[i].reparentTo(self.tunnel[i - 1])
		self.tunnel[TUNNEL_MODEL_VALUE].setZ(-TUNNEL_SEGMENT_LENGTH)
		self.tunnel[TUNNEL_MODEL_VALUE].setScale(1)
		self.tunnelMove = Sequence(
			LerpFunc(self.tunnel[0].setZ,
					 duration=TUNNEL_TIME,
					 fromData=0,
					 toData=TUNNEL_SEGMENT_LENGTH * .305),
			# Func(self.contTunnel),
			name='note_tunnel')
		self.tunnelMove.loop()

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

		if function != None:
			self.createHitbox(note, function)
		else:
			self.createHitbox(note, self.event_dummy)
		
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
		
		if not start_function:
			self.createHitbox(note_head, start_function)
		else:
			self.createHitbox(note_head, self.event_dummy)

		if not mid_function:
			self.createHitbox(note_body, mid_function)
		else:
			pass
		
		if not end_function:
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
			self.accept('into-' + collName, InFunction)
		if OutFunction:
			self.accept('outof-' + collName, OutFunction)
		if show:
			cnodePath.show()
	
	#Events
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

	#MIDI to rhythm note
	def midi2seq(self, midiFile=None):
		song_start_event_used = False
		self.noteSeq = Sequence(name = 'midi2seq')
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
					tick_sec = ((60 * 1000000 / bpm) / resolution) / 1000000.0
				elif i2.name == 'Note On':
					if i2.tick:
						self.noteSeq.append(Wait(tick_sec * i2.tick))
					note = i2.data[0]
					if note in [67, 69, 71, 72]:
						line = 4 if note == 72 else 3 if note == 71 else 2 if note == 69 else 1
						if song_start_event_used:
							self.noteSeq.append(Func(self.createLongNote, line))
						else:
							self.noteSeq.append(Func(self.createLongNote, line, self.event_startMusic))
							song_start_event_used = True
					else:
						line = 4 if note == 65 else 3 if note == 64 else 2 if note == 62 else 1 if note == 60 else random.randrange(1, 5)
						if song_start_event_used:
							self.noteSeq.append(Func(self.createShortNote, line))
						else:
							self.noteSeq.append(Func(self.createShortNote, line, self.event_startMusic))
							song_start_event_used = True

				elif i2.name == 'Note Off':
					if i2.tick:
						self.noteSeq.append(Wait(tick_sec * i2.tick))
					note = i2.data[0]
					if note in [67, 69, 71, 72]:
						self.noteSeq.append(Func(self.endLongNote, line))
		#self.noteSeq.append(Func)
		print self.noteSeq
		self.noteSeq.start()

	#GUI related Func
	def startUp(self):
		Sequence(
				Func(lambda:self.transition.fadeOut(1)),
				Wait(1),
				Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 1)),
				Func(lambda:self.transition.fadeIn(0.5)),
				Wait(3),
				Func(lambda:self.transition.fadeOut(1)),
				Wait(1),
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('models/powered_by_panda3d.png'), 1)),
				Func(lambda:self.transition.fadeIn(0.5)),
				Wait(3),
				Func(lambda:self.transition.fadeOut(1)),
				Wait(1),
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('models/MU_software_logo.png'), 1)),
				Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 0)),
				Func(lambda:self.transition.fadeIn(2))).start()
	def loadingScreen(self, function):
		loadingSequence_a = Sequence(
				Func(lambda:self.transition.fadeOut(0.5)),
				Wait(0.5),
				#Load loading screen
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('models/test_tex.png'), 1)),
				Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 1)),
				Func(lambda:self.transition.fadeIn(0.5)))
		loadingSequence_b = Sequence(
				Wait(1),
				Func(lambda:self.transition.fadeOut(0.5)),
				Wait(0.5),
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('models/MU_software_logo.png'), 1)),
				# Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 0)),
				Func(lambda:self.transition.fadeIn(1.5)))
		loadingSequence = Sequence(loadingSequence_a, Wait(2), Func(function), loadingSequence_b)
		loadingSequence.start()
	def resultScreen(self):
		pass
	
	#Main related Func
	def startPlayMode(self):
		self.initTunnel()
	def handlePause(self):
		try:
			if self.noteSeq.isStopped():
				pass
			else:
				toggleInterval(self.noteSeq)
		except:
			pass
		note_dict = ivalMgr.getIntervalsMatching('note_*')
		if not bool(note_dict):
			note_dict = self.note_dict_save
		else:
			pass
		for i in note_dict:
			toggleInterval(i)
		print 
		toggleInterval(self.tunnelMove)
		self.note_dict_save = note_dict
	def closePlayMode(self):
		#1. Remove midi to note task.
		#2. Stop and remove all intervals.
		#3. Find objects that have 'note' and 'tunnel' tags and remove them.
		self.tunnelMove.finish()
		self.randomNote.finish()
		model_list	= render.findAllMatches("=tunnel")
		model_list += render.find("note_node").findAllMatches("=note")
		for m in model_list:
			m.removeNode()
		print('Closing Playing Mode')

def toggleInterval(interval):
	if interval.isPlaying():
		interval.pause()
	else:
		interval.resume()

if __name__=="__main__":
	Demo = demo()
	Demo.run()
	try:
		print sys.argv
		if sys.argv[1] == 'dev':
			PStatClient.connect()
			render.analyze()
	except:
		pass