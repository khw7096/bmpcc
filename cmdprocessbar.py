# coding: utf-8

import os
import sys

def cmdProcessBar(cmdlist):
	#start
	sys.stdout.flush()
	sys.stdout.write( "\r[%-40s] %03d%s" % ("", 0, "%") )
	totalnum = len(cmdlist)
	num = 0
	status_str = "="
	for i in cmdlist:
		persent = (100 * num) / totalnum
		status = (40 * num) / totalnum
		os.system(i) #run cmd
		sys.stdout.write( "\r[%-40s] %03d%s" % (status_str*status, int(persent), "%") )
		num += 1
		sys.stdout.flush()
	#fin
	sys.stdout.flush()
	sys.stdout.write( "\r[%-40s] %03d%s\n" % (status_str*40, 100, "%") )
