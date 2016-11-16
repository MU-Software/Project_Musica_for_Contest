#!/usr/bin/env python
# -*- coding: utf-8 -*-
from panda3d.core import *

from direct.gui.DirectGui import *
from direct.gui.OnscreenText  import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.Transitions import Transitions

from direct.task import Task
from direct.interval.LerpInterval import *
from direct.interval.IntervalGlobal import *
from direct.interval.FunctionInterval import Func
from direct.interval.MetaInterval import Parallel
from direct.interval.MetaInterval import Sequence

from direct.showbase.MessengerGlobal import messenger

import copy
import string
import operator
from PIL import Image, ImageFilter

#pyreverse -Amy -o png -p main main.py