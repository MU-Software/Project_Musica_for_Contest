from __init__ import *
from GUI_BASE import GUIbase

class StartUp(GUIbase):
	def __init__(self):
		GUIbase.__init__(self)
		
		# self.startup_BGI_upper = render2d.attachNewNode(self.cm.generate())
		# self.startup_BGI_upper.setPos(-1, 0, -1)
		# self.startup_BGI_upper.setScale(2, 0, 2)
		# self.startup_BGI_upper.setColorScale(1, 1, 1, .9)
		# self.startup_BGI_upper.setTransparency(1)
		# self.startup_BGI_upper.setTexture(loader.loadTexture('title/background_upper_layer.png'))
		
		# self.startup_BGI_upper.setTransparency(TransparencyAttrib.MAlpha)
		# self.startup_BGI_upper.setColorScale(0, 0, 0, 1)
		# self.startup_seq = Sequence(
							# Func(lambda:self.transition.fadeOut(1)),
							# Wait(1),
							# Func(lambda:self.startup_BGI_upper.setColorScale(1, 1, 1, 1)),
							# Func(lambda:self.transition.fadeIn(0.5)),
							# Wait(3),
							# Func(lambda:self.transition.fadeOut(1)),
							# Wait(1),
							# Func(lambda:self.startup_BGI_upper.setTexture(loader.loadTexture('startup/powered_by_panda3d_1920X1080.png'), 1)),
							# Func(lambda:self.transition.fadeIn(0.5)),
							# Wait(3),
							# Func(lambda:self.transition.fadeOut(1)),
							# Wait(1),
							# Func(lambda:self.startup_BGI_upper.setTexture(loader.loadTexture('startup/MU_software_logo_1920X1080.png'), 1)),
							# Func(lambda:self.startup_BGI_upper.setColorScale(1, 1, 1, 0)),
							# Func(lambda:self.transition.fadeIn(2)))