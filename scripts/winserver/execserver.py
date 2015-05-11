#!/usr/bin/env python
import subprocess
import sys, os



dirpath = os.path.dirname(os.path.realpath(__file__))+"/"
print "Executing driver server"
print "Path: ", dirpath

#subprocess.call(["cd", dirpath])
#subprocess.call(["pwd"])
#subprocess.call(["wine", "RTX_Sturing_Win_Server.exe"])

os.chdir(dirpath)
serverfile = (dirpath + "RTX_Sturing_Win_Server.exe")
subprocess.call(["wine", serverfile])
