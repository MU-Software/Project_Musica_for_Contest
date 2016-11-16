#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from GUI_BASE import GUIbase

class End(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		#self.setup_end_GUI()
		#taskMgr.doMethodLater(1, self.setup_end_GUI, "setup_end_GUI")
	
	#It just has a text animation, and it'll remove itself.
	#So just calling setup_end_GUI will automatically unload text after 2 secs.
	def setup_end_GUI(self, task=None):
		self.thanks_text = OnscreenText(text="THANKS FOR PLAYING!",
										parent=render2d,
										fg=(1, 1, 1, 1),
										font=self.font_CPMono,
										pos=(0, 0, 0),
										scale=1
										)
		self.thanks_text.setColorScale(1, 1, 1, 0)
		Sequence(
			Parallel(
					LerpColorScaleInterval(self.thanks_text, .5, (1, 1, 1, 1), blendType='easeOut'),
					LerpScaleInterval(self.thanks_text, .5, .1, blendType='easeOut')
					),
					Wait(1),
			Parallel(
					LerpColorScaleInterval(self.thanks_text, .5, (1, 1, 1, 0), blendType='easeIn'),
					LerpScaleInterval(self.thanks_text, .5,  0, blendType='easeIn')
					)
				).start()
		def remove_task(task):
			self.thanks_text.remove_node()
		base.ignore('aspectRatioChanged')
		
		taskMgr.doMethodLater(2, remove_task, "unload_end_text")