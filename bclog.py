#!/usr/bin/env python3

from bclevelfile import BCLevelFile
from bclogfiles import BCLogFiles

from pathlib import Path
from re import I
from subprocess import call
from time import sleep
from datetime import datetime

class BCLog():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot"):

        self._minecraftdir = minecraftdir
        self._servername = servername
        self._seed = None
        
        self._outfile = None
        self._gametime = 0

    def BCLogFilename(self):
        result = ""
        if(self._seed is not None):
            result = self._minecraftdir+"/bclogs/"+self._servername+"_"+self._seed
        return(result)

    def ReadExistingLog(self, bclogpath):
        filehandle = open(bclogpath)
        for line in filehandle:
            if "Nether:" in line:
                print(line)
            if "LevelUpdate:" in line:
                self._gametime = int(line.split(',')[0].split()[-1])

        filehandle.close()

    def Open(self, seed):

        if(self._outfile and seed is self._seed):
            print("Seed is the same and the file is already open")
            return()

        if(self._outfile and seed is not self._seed):
            print("Closing file and opening with new seed")
            self.Close()
            self._gametime = 0

        if(seed is None):
            print("Seed is blank")
            return()

        self._seed = seed
        bclogpath = Path(self.BCLogFilename())
        if(bclogpath.exists()):
            self.ReadExistingLog(bclogpath)

        self._outfile = open(self.BCLogFilename(),'a')

    def LogResults(self, levelfile: BCLevelFile, logfiles: BCLogFiles):
        if self._seed is not levelfile.Seed():
            self.Open(levelfile.Seed())
        if self._gametime != levelfile.GameTime() and self._outfile:
            self._gametime = levelfile.GameTime()
            self._outfile.write(f"{datetime.fromtimestamp(levelfile.LevelFileLastUpdate()).strftime('%Y-%m-%d %H:%M:%S')}")
            self._outfile.write(f" LevelUpdate: ")
            self._outfile.write(f"{levelfile.GameTime()},")
            self._outfile.write(f"{levelfile.DayTime()},")
            self._outfile.write(f"{levelfile.ClearWeatherTime()},")
            self._outfile.write(f"{levelfile.Raining()},")
            self._outfile.write(f"{levelfile.RainTime()},")
            self._outfile.write(f"{levelfile.Thundering()},")
            self._outfile.write(f"{levelfile.ThunderTime()},")
            self._outfile.write(f"{levelfile.WanderingTraderSpawnDelay()},")
            self._outfile.write(f"{levelfile.WanderingTraderSpawnChance()},")
            self._outfile.write(f"{levelfile.WanderingTraderID()}\n")
            self._outfile.flush()

    def Flush(self, output=""):
        if(self._outfile):
            self._outfile.flush()

    def Close(self):
        if(self._outfile):
            self._outfile.close()

    def SaveAllFiles():
        call(["./save-it-all.bash"])
        sleep(0.5)

def main():
    print("BCLog: Unit Testing")
    bclog = BCLog()

if __name__ == '__main__':
    main()