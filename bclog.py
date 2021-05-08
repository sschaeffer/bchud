from os import umask
from subprocess import call
from getopt import getopt
from time import sleep, strftime

class BCLog():

    def __init__(self, argv=None):
        self.logresults = True
        self.outfh = None
        if self.logresults:
            self.outfh = open("{}.{}".format("/tmp/bchud",strftime("%H%M%S")),"w+")
        self.serverdir = "/media/local/Minecraft/server/snapshot"
        self.serverworlddir = "/media/local/Minecraft/server/snapshot/snapshot"

    def ServerDir(self):
        return (self.serverdir)

    def ServerWorldDir(self):
        return (self.serverworlddir)

    def Write(self, output):
        if(self.outfh):
            self.outfh.write(output)
            self.outfh.flush()

    def SaveAllFiles():
        call(["./save-it-all.bash"])
        sleep(0.5)