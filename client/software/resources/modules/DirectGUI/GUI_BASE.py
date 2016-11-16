#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This is base module of GUI.
from __init__ import *

class GUIbase():
	def __init__(self):
		base.setBackgroundColor(0, 0, 0)
		# base.messenger.toggleVerbose()
		
		#Font load
		self.font_koverwatch = loader.loadFont("resources/fonts/koverwatch.otf")
		self.font_koverwatch.setPixelsPerUnit(210)
		self.font_square = loader.loadFont("resources/fonts/square.ttf")
		self.font_square.setPixelsPerUnit(210)
		self.font_square2 = loader.loadFont("resources/fonts/unispace.ttf")
		self.font_square2.setPixelsPerUnit(210)
		self.font_CPMono = loader.loadFont("resources/fonts/CPMono_v07_Plain.otf")
		self.font_CPMono.setPixelsPerUnit(210)
		self.font_SourceSans = loader.loadFont("resources/fonts/SourceHanSansHWK-Regular.otf")
		self.font_CPMono.setPixelsPerUnit(258)
		
		#Fade In/Out
		self.transition = Transitions(loader)
		self.transition.setFadeColor(0, 0, 0)
		
		#CardBoard load
		self.cm = CardMaker('BGI')