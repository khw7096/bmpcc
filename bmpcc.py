# coding: utf-8
import os
import time
import tui
import sys

ROOT = "%s/onsetdata" % (os.path.expanduser('~'))

class Onsetcopy:
	MT_POINT = ""
	PROJECT = ""
	SEQ = ""
	isitRM = False
	INpath = ""
	HW = ""

	def setHwAndMountpoint(self):
		"""
		메모리가 장착되었을 때 사용된 하드웨어, 마운트포인트를 설정한다.
		"""
		if os.path.isdir("/Volumes/bmpcc"): #bmpcc
			self.MT_POINT = "/Volumes/bmpcc"
			self.HW = "bmpcc"
		elif os.path.isdir("/Volumes/ZOOM"): # zoom h1 audio
			self.MT_POINT = "/Volumes/ZOOM"
			self.HW = "zoom"
		elif os.path.isdir("/Volumes/noname"): #gopro defalut value
			self.MT_POINT = "/Volumes/noname"
			self.HW = "gopro"
		else:
			print "No SD card."
			sys.exit(0)
		print "   Detect %s" % (self.HW)

	def printFreeSpace(self):
		"""
		현재 하드디스크 남아있는 용량을 출력한다.
		"""
		s = os.statvfs('/') #mount name
		free = (s.f_bavail * s.f_frsize) / 1024 / 1024 / 1024 #k,m,g byte.
		print "   Disk size : %04s G" % (free)

	def printUsedSpace(self):
		"""
		메모리카드 내부 복사될 용량을 출력한다.
		"""
		s = os.statvfs(self.MT_POINT)
		use = (s.f_blocks - s.f_bfree) * s.f_frsize / 1024 / 1024 / 1024.0
		print  "     SD size : %04s G" % (str(use)[0:4])

	def title(self):
		print "=== Onset Data Copy Managing System ==="

	def isCopy(self):
		answercopy = raw_input("Copy SD to HDD ?(y/n) : ")
		if answercopy in ['y', 'Y']:
			return 1
		else:
			exit()
	
	def selectProject(self):
		projectlist = os.listdir(ROOT)
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
	

	def isRmSDcard(self):
		"""
		복사가 끝나고 메모리를 삭제할지 물어본다.
		"""
		isitrmsd = raw_input("remove SD card(y/n) : ")
		if isitrmsd in ["Y", "y"]:
			self.isitRM = True

	def copy(self):
		copylist = []
		self.INpath = "%s/%s/%s/%s" % (ROOT, self.PROJECT, time.strftime('%y%m%d'), self.HW)
		if not os.path.exists(self.INpath):
			os.makedirs(self.INpath)
		#make copy list
		if self.HW == "bmpcc":
			filelist = os.listdir("/Volumes/bmpcc")
			for i in filelist:
				if os.path.splitext(i)[-1].lower() == ".mov": # proresHQ로만 촬영합니다.
					copylist.append("cp -f /Volumes/bmpcc/%s %s" % (i, self.INpath))
				else:
					pass
			tui.os_run_status(copylist)
		elif self.HW == "zoom":
			filelist = os.listdir("/Volumes/ZOOM/STEREO/FOLDER01")
			for i in filelist:
				if os.path.splitext(i)[-1].lower() in [".mp3",".wav"]: # proresHQ로만 촬영합니다.
					copylist.append("cp -f /Volumes/ZOOM/STEREO/FOLDER01/%s %s/sound" % (i, self.INpath))
				else:
					pass
			tui.os_run_status(copylist)
		else:
			pass

	def rmsd(self):
		if self.isitRM:
			os.system("rm -rf %s/*" % (self.MT_POINT))
	
	def openFolder(self):
		os.system("open %s" % (self.INpath)) 

def main():
	foo = Onsetcopy()
	foo.title()
	foo.setHwAndMountpoint() #get sdcard mountpoint
	foo.printFreeSpace()
	foo.printUsedSpace()
	if foo.isCopy():
		foo.selectProject()
		foo.isRmSDcard()
		foo.copy()
		foo.rmsd()
		foo.openFolder()
		print "copy done."

if __name__ == "__main__":
	main()

