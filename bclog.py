#!/usr/bin/env python3

from subprocess import call
from time import sleep

class BCLog():

    def __init__(self, logresults=True, minecraftdir="/media/local/Minecraft/server", servername="snapshot"):

        self._logresults = logresults
        self._minecraftdir = minecraftdir
        self._servername = servername
        self._seed = "null"

        self._outfile = None

    def BCLogFilename(self):
        return (self._minecraftdir+"/bcogs/"+self._servername+"_"+self._seed)

    def SetSeed(seed):
        self._seed = seed

    def Log(self, output):
        if(self._outfile):
            self._outfile.write(output)
            self._outfile.flush()

    def LogFlush(self, output):
        if(self._outfile):
            self._outfile.write(output)
            self._outfile.flush()

    def SaveAllFiles():
        call(["./save-it-all.bash"])
        sleep(0.5)

def main():
    print("BCLog: Unit Testing")
    bclog = BCLog()

    print(bclog.BCLogFilename())

if __name__ == '__main__':
    main()