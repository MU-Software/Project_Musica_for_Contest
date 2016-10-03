#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2016 MU Software(@MUsoftware on twitter), All Rights Reserved.
import sys; sys.dont_write_bytecode = True
reload(sys); sys.setdefaultencoding('utf-8')
import random, string, json, zipfile, argparse, time, midi
from panda3d.core import *
loadPrcFile("resources/config.prc")

import serial

from resources.modules.MU_stdlib import *
from resources.modules.MU_gameDef import *
from resources.modules.MU_Musica import *
#Short Note 1 = 60
#Short Note 2 = 62
#Short Note 3 = 64
#Short Note 4 = 65
#Long  Note 1 = 67
#Long  Note 2 = 69
#Long  Note 3 = 71
#Long  Note 4 = 72
#Short Note random = 59

NOW_DEV_MODE = False

class Game(ShowBase, Musica_main, gameDef):
	def __init__(self):
		ShowBase.__init__(self)
		gameDef.__init__(self)
		Musica_main.__init__(self)
		
		song_list_file = open("resources/song/song_list.json")
		song_list = json.loads(song_list_file.read())
		
		self.tunnel = Tunnel()
		self.tunnel.tunnel_start()
	
		base.accept('escape', sys.exit)
		base.accept('a', render.ls)
		if NOW_DEV_MODE:
			PStatClient.connect()
			render.analyze()

class Arcade_Support:
	def __init__(self):
		pass

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	game = Game()
	game.run()

class demo(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()
		base.setBackgroundColor(0, 0, 0)
		base.camLens.setFov(30)
		self.ingameSetup()
		self.note_speed = 5
		self.accept('escape', self.handlePause)
		self.accept('=', sys.exit)
		self.accept('0', self.midi2seq)
		self.accept('r', render.ls)
		self.startUp()
	def ingameSetup(self):
		
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