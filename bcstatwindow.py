from bclogfile import BCLogFileUpdate, BCLogFile
import curses
from datetime import datetime
from time import sleep, strftime
from subprocess import call

class BCStatWindow():

    def __init__(self, window):
        self.window = window
        self.statcount = 8
        self.stats = ["{}".format(i) for i in range(self.statcount)]

    def RenderStatWindow(self, bclf):
        self.window.box()
        for i in range(self.statcount):
            self.window.addstr(i+1,1,self.stats[i])
            bclf_update = bclf.GetLogUpdate(bclf.NumLogUpdates()-(i+1))
            if bclf_update != None:
                updatestr="{} {:5.0f} ".format(bclf_update._updatetime.strftime("(%m/%d)%H:%M:%S"),bclf_update._gametime)
                updatestr=updatestr+"{} {}".format(bclf_update.estgametime(),datetime.fromtimestamp(bclf_update.eststarttime()).strftime("(%m/%d)%H:%M:%S"))
                self.window.addstr(i+1,33,updatestr)

    def RecordTime(self,bct):
        for i in range(self.statcount-1):
            self.stats[(self.statcount-1)-i] = self.stats[(self.statcount-1)-(i+1)]
        self.stats[0] = "[{}] The time is {}".format(strftime("%H:%M:%S"),round(bct.EstimatedGameTime()))
        call(["/home/integ/Code/stage/query-time.bash"])
        sleep(0.5)
