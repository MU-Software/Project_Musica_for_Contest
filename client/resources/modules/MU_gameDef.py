#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import *


class gameDef(ShowBase):
	def __init__(self):
		base.disableMouse()
		base.setBackgroundColor(1, 1, 1)
		self.gameSetup()
		#self.startupSequence()
		
		#Sequence(Func(self.startupSequence), Wait(15), Func(lambda: self.loadingScreen(self.hardWork))).start()
		
	def hardWork(self):
		print("Hard Work started!")
		a = 2
		b = 0
		for i in range(100000):
			b += a**i
		print("Hard Work ended!")
	
	
	def setKey(self, key, value):
		self.keyMap[key] = value

	def gameSetup(self):
		
		self.transition = Transitions(loader)
		self.transition.setFadeColor(0, 0, 0)
		
		self.mainFrame = DirectFrame(frameColor=(1, 1, 1, 0),
							  image = './resources/tex/MU_software_logo_background.png',
							  pos=(0, 0, 0),
							  sortOrder=-1,
							  parent=render2d)
		self.mainFrame.setTransparency(TransparencyAttrib.MAlpha)
		self.mainFrame.setColorScale(0, 0, 0, 0)

	def startupSequence(self):
		self.mainFrame.setColorScale(0, 0, 0, 1)
		Sequence(
				Func(lambda:self.transition.fadeOut(1)),
				Wait(1),
				Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 1)),
				Func(lambda:self.transition.fadeIn(0.5)),
				Wait(3),
				Func(lambda:self.transition.fadeOut(1)),
				Wait(1),
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('./resources/tex/powered_by_panda3d.png'), 1)),
				Func(lambda:self.transition.fadeIn(0.5)),
				Wait(3),
				Func(lambda:self.transition.fadeOut(1)),
				Wait(1),
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('./resources/tex/MU_software_logo_background.png'), 1)),
				Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 0)),
				Func(lambda:self.transition.fadeIn(2))).start()
	
	def loadingScreen(self, function):
		def printf(a):
			print(a)
		loadingSequence_a = Sequence(
				Func(lambda:printf("Loading_seq a started")),
				Func(lambda:self.transition.fadeOut(0.5)),
				Wait(0.5),
				#Load loading screen
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('models/test_tex.png'), 1)),
				Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 1)),
				Func(lambda:self.transition.fadeIn(0.5)),
				Func(lambda:printf("Loading_seq a ended")))
		loadingSequence_b = Sequence(
				Func(lambda:printf("Loading_seq b started")),
				Wait(1),
				Func(lambda:self.transition.fadeOut(0.5)),
				Wait(0.5),
				Func(lambda:self.mainFrame.setTexture(loader.loadTexture('models/MU_software_logo.png'), 1)),
				# Func(lambda:self.mainFrame.setColorScale(1, 1, 1, 0)),
				Func(lambda:self.transition.fadeIn(1.5)),
				Func(lambda:printf("Loading_seq b ended")))
		loadingSequence = Sequence(loadingSequence_a, Wait(2), Func(function), loadingSequence_b)
		for i in range(3):
			if i == 0:
				loadingSequence_a.start()
			elif i == 1:
				function()
			elif i == 2:
				loadingSequence_b.start()
			else:
				pass