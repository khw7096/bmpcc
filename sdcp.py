# -*- coding: utf-8 -*-
import os
import time
import tui
import sys

class eat:
	MT_POINT = ""
	PROJECT = ""
	SEQ = ""
	isitRM = 0
	INpath = ""
	HW = ""

	def get_mountpoint(self):
		if os.path.isdir("/Volumes/camsd"): #bmpcc
			self.MT_POINT = "/Volumes/camsd"
			self.HW = "bmpcc"
		elif os.path.isdir("/Volumes/ZOOM"):
			self.MT_POINT = "/Volumes/ZOOM"
			self.HW = "zoom"
		elif os.path.isdir("/Volumes/noname"): #gopro defalut value
			self.MT_POINT = "/Volumes/noname"
			self.HW = "gopro"
		else:
			print "No SD card."
			sys.exit(0)
		print "   Detect %s" % (self.HW)

	def diskfree(self):
		s = os.statvfs('/') #mount name
		free = (s.f_bavail * s.f_frsize) / 1024 / 1024 / 1024 #k,m,g byte.
		print "   Disk size : %04s G" % (free)

	def diskuse(self):
		s = os.statvfs(self.MT_POINT)
		use = (s.f_blocks - s.f_bfree) * s.f_frsize / 1024 / 1024 / 1024.0
		print  "     SD size : %04s G" % (str(use)[0:4])

	def intro(self):
		print "=== SD DATA Managing System ==="

	def ask_copy(self):
		answercopy = raw_input("Copy SD to HDD ?(y/n) : ")
		if answercopy in ['y', 'Y']:
			return 1
		else:
			exit()
	
	def select_project(self):
		projectlist = os.listdir("%s/lazypic/show" % (os.path.expanduser('~')))
		menunum = 1
		rmlist = []
		for i in projectlist:
			if i[0] != ".":
				print "%s. %s" % (menunum, i)
				menunum = menunum + 1
			else:
				rmlist.append(i)

		#remove except list
		for j in rmlist:
			projectlist.remove(j)

		projectnum = raw_input("Select Project(q:quit) : ")
		self.PROJECT = projectlist[int(projectnum) - 1]
		print "Select -> %s" % (self.PROJECT)
	

	def askrmsd(self):
		isitrmsd = raw_input("remove SD card(y/n) : ")
		if isitrmsd in ["Y", "y"]:
			self.isitRM = 1
		else:
			self.isitRM = 0

	def copy(self):
		copylist = []
		self.INpath = "%s/lazypic/show/%s/product/in/%s" % (os.path.expanduser("~"), self.PROJECT, time.strftime('%y%m%d'))
		try:
			if self.HW == "bmpcc":
				os.system("mkdir -p %s" % (self.INpath))
			elif self.HW == "zoom":
				os.system("mkdir -p %s/sound" % (self.INpath))
			else:
				pass
		except:
			pass
		#make copy list
		try:
			if self.HW == "bmpcc":
				filelist = os.listdir("/Volumes/camsd")
				for i in filelist:
					if i[-3:] == "mov":
						copylist.append("cp -f /Volumes/camsd/%s %s" % (i, self.INpath))
					else:
						pass
				tui.os_run_status(copylist)
			elif self.HW == "zoom":
				filelist = os.listdir("/Volumes/ZOOM/STEREO/FOLDER01")
				for i in filelist:
					if i[-3:] == "MP3":
						copylist.append("cp -f /Volumes/ZOOM/STEREO/FOLDER01/%s %s/sound" % (i, self.INpath))
					else:
						pass
				tui.os_run_status(copylist)
			else:
				pass
		except:
			print "check connect SDcard."
			sys.exit(1)
	def rmsd(self):
		if self.isitRM:
			os.system("rm -rf %s/*" % (self.MT_POINT))
	
	def openfolder(self):
		os.system("open %s" % (self.INpath)) 

def main():
	foo = eat()
	foo.intro()
	foo.get_mountpoint() #get sdcard mountpoint
	foo.diskfree()
	foo.diskuse()
	if foo.ask_copy():
		foo.select_project()
		foo.askrmsd()
		foo.copy()
		foo.rmsd()
		foo.openfolder()
		print "Enjoy work~~~!!! yo~~!"

if __name__ == "__main__":
	main()

