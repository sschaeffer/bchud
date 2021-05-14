#!/usr/bin/env python3

from pathlib import Path
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

    def ReadExistingLog(self, bclogpath):
        filehandle = open(bclogpath)
        for line in filehandle:
            print(line)
        filehandle.close()

    def Open(self, seed):

        if(seed is None):
            print("Seed is blank")
            return()

        if(self._outfile and seed is self._seed):
            print("Seed is the same and the file is already open")
            return()

        if(self._outfile and seed is not self._seed):
            print("Closing file and opening with new seed")
            self.Close()

        self._seed = seed
        bclogpath = Path(self.BCLogFilename())
        if(bclogpath.exists()):
            self.ReadExistingLog(bclogpath)

        self._outfile = open(self.BCLogFilename(),'a')

    def Log(self, output):
        if(self._outfile):
            self._outfile.write(output)

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
    bclog.Open("123")
    bclog.Log("This is a test 123")
    bclog.Open("321")
    bclog.Log("This is a test 321")

if __name__ == '__main__':
    main()