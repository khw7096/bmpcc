# -*- coding: utf-8 -*-
# khw7096@gmail.com

import os
import sys

def os_run_status(cmdlist):
	totalnum = len(cmdlist)
	num = 0
	status_str = "="
	for i in cmdlist:
		persent = (100 * num) / totalnum
		status = (40 * num) / totalnum
		os.system(i) #run cmd
		sys.stdout.write( "\r[%-40s] %03s%s" % (status_str*status, persent, "%") )
		num = num + 1
		sys.stdout.flush()
	#fin
	sys.stdout.flush()
	sys.stdout.write( "\r[%-40s] %03s%s\n" % (status_str*40, 100, "%") )
	print "process done."

if __name__ == "__main__":
	cmdlist = ["1","2","3","4","5","6","7","8","9"]
	os_run_status(cmdlist)


