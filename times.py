import os, sys, subprocess
import nbt
from nbt import NBTFile

class MCTimes:

    def gettime(self):
        filename = os.path.join('/media/deflection/Minecraft/server/snapshot/snapshot','level.dat')
        level = NBTFile(filename)
        return(level["Data"]["Time"])

    def getdaytime(self):
        filename = os.path.join('/media/deflection/Minecraft/server/snapshot/snapshot','level.dat')
        level = NBTFile(filename)
        daytimestring = str(level["Data"]["DayTime"])
        return(int(daytimestring)%24000)

    def getday(self):
        filename = os.path.join('/media/deflection/Minecraft/server/snapshot/snapshot','level.dat')
        level = NBTFile(filename)
        daytimestring = str(level["Data"]["DayTime"])
        return(int(daytimestring)/24000)

    def saveallfiles(self):
        subprocess.call(["/home/integ/Code/scratch/save-it-all.bash"])        