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

    def Render(self, bclf):
        self.window.box()
        for i in range(self.statcount):
            self.window.addstr(i+1,1,self.stats[i])
            bclf_update = bclf.GetLogUpdate(bclf.NumLogUpdates()-(i+1))
            if bclf_update != None:
                updatestr="{} {:5.0f} ".format(bclf_update._updatetime.strftime("Estimated [%H:%M:%S]"),bclf_update._gametime)
                actualgametime = 0
                if(len(self.stats[i])>1):
                    actualgametime = int(self.stats[i].split()[4])
                    updatestr=updatestr+f" {actualgametime-bclf_update._gametime}     "
                self.window.addstr(i+1,33,updatestr)

    def RecordTime(self,bct):
        for i in range(self.statcount-1):
            self.stats[(self.statcount-1)-i] = self.stats[(self.statcount-1)-(i+1)]
        self.stats[0] = "[{}] The time is {}".format(strftime("%H:%M:%S"),round(bct.EstimatedGameTime()))
        call(["./query-time.bash"])
        sleep(0.5)
