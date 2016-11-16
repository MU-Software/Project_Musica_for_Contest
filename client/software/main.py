#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2016 MU Software(@MUsoftware on twitter), All Rights Reserved.

import sys; reload(sys); sys.setdefaultencoding('utf-8')
import random, string, json, zipfile, argparse, time, midi
from panda3d.core import *
loadPrcFile("resources/config.prc")

from resources.modules.MU_Hardware import *
from resources.modules.MU_Musica import *
from resources.modules.MU_GUI import *
#Short Note 1 = 60
#Short Note 2 = 62
#Short Note 3 = 64
#Short Note 4 = 65
#Long  Note 1 = 67
#Long  Note 2 = 69
#Long  Note 3 = 71
#Long  Note 4 = 72

class Game(ShowBase, MU_Musica):
	def __init__(self):
		ShowBase.__init__(self)
		MU_Musica.__init__(self)

		base.disableMouse()
		base.setBackgroundColor(0, 0, 0)
		base.accept('shift-control-alt-x', taskMgr.stop)
		
		self.process_status_argv = Queue()
		self.HW_sub_process = Process(target = HW_support().hardware_event_handler, args=(arcade_mode,))
		self.HW_sub_process.daemon = True
		self.HW_sub_process.start()
		
		self.title.setup_title_GUI()
		def credit_1up():
			self.title_coin_text_mgr(self.title.credit_return()+1)
		base.accept("tab", credit_1up)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	arcade_help_text  = 'Run game on arcade mode. You can also use auto. ex) -a=COM3'
	parser.add_argument('-a', '--arcade' , type=str, help=arcade_help_text, required=False)
	args = parser.parse_args()
	arcade_mode = args.arcade
	game = Game()
	game.run()