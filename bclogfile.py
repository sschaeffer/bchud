#!/usr/bin/env python3

from bclog import BCLog
from pathlib import Path
from datetime import date, datetime, timedelta
from time import time

class BCLogFileUpdate():

    def __init__(self, updatetime, gametime=0):
        self._updatetime = updatetime
        self._gametime = gametime

    @property
    def updatetime(self):
        self._updatetime

    @property
    def gametime(self):
        self._gametime

    def estgametime(self):
        return(self._gametime+round((time()-self._updatetime.timestamp())*20))

    def eststarttime(self):
        return(self._updatetime.timestamp()-(self._gametime/20))


class BCLogFile():

    def __init__(self, logfilename="logs/latest.log", bclog=None):

        self.logfilename=logfilename
        self.updates = [] 
        self.updatetimes = [] 
        self.lastupdatetime=0
        self.starttime=0
        self.nethertime=0
        self.bclog = BCLog()
        if(self.bclog == None):
            self.bclog = BCLog()

    def ReadLogFile(self):
        logfilepath = Path(self.bclog.ServerDir()+"/"+self.logfilename)
        if logfilepath.exists():
            if self.lastupdatetime != logfilepath.stat().st_mtime:
                self.lastupdatetime = logfilepath.stat().st_mtime
                with open(logfilepath) as logfh:
                    line = logfh.readline()
                    while line:
                        if "The time is" in line:
                            updatetime = datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()
                            updatedatetime = datetime.combine(date.today(),updatetime)
                            if updatedatetime not in self.updatetimes:
                                gametime = int(line.split(" ")[6])
                                self.updatetimes.append(updatedatetime)
                                self.updates.append(BCLogFileUpdate(updatedatetime,gametime))
                        elif "For help, type" in line:
                            starttime = datetime.combine(date.today(),datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
                            if starttime != self.starttime:
                               self.starttime = starttime
                               self.bclog.Write(f"Server boot time: {datetime.fromtimestamp(starttime)}\n")
                        elif "We Need to Go Deeper" in line:
                            nethertime = datetime.combine(date.today(),datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
                            if nethertime != self.nethertime:
                               self.nethertime = nethertime
                               self.bclog.Write(f"Nether time: {timedelta(seconds=round(nethertime-self.starttime))} {datetime.fromtimestamp(nethertime)}\n")
                        line = logfh.readline()
                    logfh.close()

    def PrintLogFileUpdates(self):
        print(f"Start Time is: {self.GetStarttime()}")
        for updates in self.updates:
            print("{} - {} - {} - {}".format(updates._updatetime,updates._gametime,updates.estgametime(),updates.eststarttime()))

    def NumLogUpdates(self):
        return len(self.updates)

    def GetLogUpdate(self,i):
        result = None
        if i >= 0:
            if i < len(self.updates):
                result = self.updates[i]
        return result

    def GetLastLogUpdate(self):
        return self.GetLogUpdate(self.NumLogUpdates()-1)

    def GetStarttime(self):
        return self.starttime

def main():
    print("BCLogFile: Unit Testing")
    bclf = BCLogFile()
    bclf.ReadLogFile()
    bclf.PrintLogFileUpdates()
    bclfu_test = bclf.GetLastLogUpdate()

    
if __name__ == '__main__':
    main()