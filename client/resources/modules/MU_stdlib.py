#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import *
import StringIO, contextlib

#Return random string.
def randomID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def toggleInterval(interval):
	if interval.isPlaying():
		interval.pause()
	else:
		interval.resume()

#Redirect the standard output to a string.
#USAGE
# code = """
# i = [0,1,2]
# for j in i :
    # print j
# """
# with stdoutIO() as s:
    # exec code

# print "out:", s.getvalue()
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
