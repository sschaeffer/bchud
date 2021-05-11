#!/usr/bin/env python3

from os import stat_result
from re import I
from subprocess import call
from time import sleep


class BCLog():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot"):

        self._minecraftdir = minecraftdir
        self._servername = servername
        self._seed = None

        self._logentries = []

        self._outfile = None

    def BCLogFilename(self):
        result = ""
        if(self._seed is not None):
            result = self._minecraftdir+"/bclogs/"+self._servername+"_"+self._seed
        return(result)

    def SetSeed(self, seed):
        self._seed = seed

    def Close(self):
        if(self._outfile):
            self._outfile.close()

    def Open(self, seed):
        if(seed is not None):
            self.SetSeed(seed)
        self.Close()
        self._outfile = open(self.BCLogFilename(),'w')

    def Log(self, output):
        if(self._outfile):
            self._outfile.write(output)

    def Flush(self, output):
        if(self._outfile):
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