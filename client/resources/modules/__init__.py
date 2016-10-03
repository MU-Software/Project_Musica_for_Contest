#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from panda3d.core import *
import random, string, json, zipfile, argparse, time, midi
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
from direct.filter.FilterManager import FilterManager
from direct.showbase.DirectObject import DirectObject
import ctypes, math
from ctypes import *
from ctypes.wintypes import BYTE, WORD, SHORT, DWORD, SHORT
UBYTE = c_ubyte