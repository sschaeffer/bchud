#!/usr/bin/env python3

from pathlib import Path
from datetime import date, datetime, timedelta
from time import time, strptime, sleep
from os import listdir
import re
import gzip

REGEX_LOGIN_USERNAME = re.compile("\[Server thread\/INFO\]: ([^]]+)\[")
REGEX_LOGOUT_USERNAME = re.compile("\[Server thread\/INFO\]: ([^ ]+) lost connection")
REGEX_KICK_USERNAME = re.compile("\[INFO\] CONSOLE: Kicked player ([^ ]*)")
REGEX_NETHER_USERNAME = re.compile("\[Server threads\/INFO\] ([^ ]*) has made the advancement \[We Need To Go Deeper\]")
DEATH_MESSAGES = (
    "was squashed by.*",
    "was pricked to death",
    "walked into a cactus whilst trying to escape.*",
    "drowned.*",
    "blew up",
    "was blown up by.*",
    "fell from a high place.*",
    "hit the ground too hard",
    "fell off a ladder",
    "fell off some vines",
    "fell out of the water",
    "fell into a patch of.*",
    "was doomed to fall.*",
    "was shot off.*",
    "was blown from a high place.*",
    "went up in flames",
    "burned to death",
    "was burnt to a crisp whilst fighting.*",
    "walked into a fire whilst fighting.*",
    "was slain by.*",
    "was shot by.*",
    "was fireballed by.*",
    "was killed.*",
    "got finished off by.*",
    "tried to swim in lava.*",
    "died",
    "was struck by lighting",
    "starved to death",
    "suffocated in a wall",
    "was pummeled by.*",
    "fell out of the world",
    "was knocked into the void.*",
    "withered away",
)
REGEX_DEATH_MESSAGES = set()
for message in DEATH_MESSAGES:
    REGEX_DEATH_MESSAGES.add(re.compile("\Server thread\/INFO\]: ([^ ]+) (" + message + ")"))

class BCUserStats:
    def __init__(self, username=""):
        self._username = username
        self._logins = 0
        self._timeplayed = 0.0
        self._deathcount = 0
        self._deathtypes = {}
        self._prevlogin = None

    def Login(self, date):
        self._logins += 1
        self._prevlogin = date

    def Logout(self, date):
        if self._prevlogin is None:
            return
        session = date - self._prevlogin
        self._timeplayed += session
        self._prevlogin = None

    def NetherEntry(self, date):
        if self._prevlogin is not None and self._netherentry is None:
            currentsession = date - self._prevlogin
            self._netherentry = self._timeplayed + currentsession

    @property
    def username(self):
        return self._username

    @property
    def logins(self):
        return self._logins


class BCGameSession():
    def __init__(self, starttime, endtime=0):
        self._starttime = starttime
        self._endtime = endtime

    def SetEndTime(self,endtime):
        self._endtime = endtime

    @property
    def starttime(self):
        self._starttime

    @property
    def starttime(self):
        self._endtime

class BCLogFilesTimeUpdate():

    def __init__(self, updatetime, gametime=0):
        self._updatetime = updatetime
        self._gametime = gametime

    @property
    def updatetime(self):
        self._updatetime

    @property
    def gametime(self):
        self._gametime

    def EstimatedGameTime(self):
        return(self._gametime+round((time()-self._updatetime.timestamp())*20))

    def EstimatedStartTime(self):
        return(self._updatetime.timestamp()-(self._gametime/20))

class BCLogFiles():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot"):

        self.minecraftdir=minecraftdir
        self.servername=servername

        self.gamesessions = [] 
        self.timeupdates = [] 
        self.lastfileupdate=0
        self.currentserversessionstart=0
        self.currentserversessionend=0

        self.users={}

        self.fileBytePosition = 0

    def LogFilename(self):
        return(self.minecraftdir+"/"+self.servername+"/logs/latest.log")

    def ParseLine(self, line, logdate):
        line = line.rstrip()
#        print(line)


        if "For help, type" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            self.currentserversessionstart = logdatetime
            self.currentserversessionend = 0
            self.gamesessions.append(BCGameSession(logdatetime))
#           self.bclog.Write(f"Server boot time: {datetime.fromtimestamp(starttime)}\n")

        if "Stopping the server" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            self.currentserversessionend = logdatetime
            gamesession = self.gamesessions[len(self.gamesessions)-1]
            gamesession.SetEndTime(logdatetime)

        if "The time is" in line:
            updatetime = datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()
            updatedatetime = datetime.combine(date.today(),updatetime)
            gametime = int(line.split(" ")[6])
            self.timeupdates.append(BCLogFilesTimeUpdate(updatedatetime,gametime))


        if "logged in with entity id" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_LOGIN_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username not in self.users:
                self.users[username] = BCUserStats(username)
            user = self.users[username]
            user.Login(logdatetime)

        if "lost connection" in line or "[INFO] CONSOLE: Kicked player" in line:
            username = "" 
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            if "lost connection" in line:
                username = (REGEX_LOGOUT_USERNAME.search(line)).group(1).lstrip().rstrip()
            else:
                username = (REGEX_KICK_USERNAME.search(line)).group(1).lstrip().rstrip()

            if username in self.users:
                user = self.users[username]
                user.Logout(logdatetime)

        if "We Need to Go Deeper" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_NETHER_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in users:
                user = user[username]
                user.NetherEntry(logdatetime)


    def ReadPreviousLogFiles(self):
        for logname in sorted(listdir(self.minecraftdir+"/"+self.servername+"/logs")):
            if not re.match("\d{4}-\d{2}-\d{2}-\d+\.log\.gz", logname):
                continue
            d = strptime("-".join(logname.split("-")[:3]), "%Y-%m-%d")
            day = date(*(d[0:3]))
            logfile = gzip.open(Path(self.minecraftdir+"/"+self.servername+"/logs",logname), 'rt')
            for line in logfile:
                self.ParseLine(line, day)
            logfile.close()

    def ReadLogFile(self, logfilepath):

        if self.fileBytePosition > logfilepath.stat().st_size:
            # Server might have restarted so we need to reinit
            self.fileBytePosition = 0
            self.UpdateLogInfo()
        else:
            if self.lastfileupdate != logfilepath.stat().st_mtime and self.fileBytePosition < logfilepath.stat().st_size:
                self.lastfileupdate = logfilepath.stat().st_mtime
                logfile = open(logfilepath,'r')
                logfile.seek(self.fileBytePosition)
                for line in logfile:
                    self.ParseLine(line,date.today())
                self.fileBytePosition = logfile.tell()
                logfile.close()

    def UpdateLogInfo(self):
        logfilepath = Path(self.LogFilename())
        if not logfilepath.exists():
            # Log file was deleted so re-init the stats
            self.__init__(self.minecraftdir,self.servername)
        else:
            if(self.fileBytePosition==0):
                # First time reading the file so re-init and read previous logs (if any) 
                self.__init__(self.minecraftdir,self.servername)
                self.ReadPreviousLogFiles()
            self.ReadLogFile(logfilepath)

    def NumLogTimeUpdates(self):
        return len(self.timeupdates)

    def GetLogTimeUpdate(self,i):
        result = None
        if i >= 0:
            if i < len(self.timeupdates):
                result = self.timeupdates[i]
        return result

    def GetLastLogTimeUpdate(self):
        return self.GetLogTimeUpdate(self.NumLogTimeUpdates()-1)

    def GetCurrentServerSessionStartTime(self):
        return self.currentserversessionstart

    def GetCurrentServerSessionEndTime(self):
        return self.currentserversessionend

    def ServerActive(self):
        if(self.currentserversessionend==0):
            return True
        else:
            return False

    def PrintDebug(self):
        print(f"Current Server Session Start Time is: {datetime.fromtimestamp(self.GetCurrentServerSessionStartTime())}")
        if(not self.ServerActive()):
           print(f"Current Server Session End Time is:   {datetime.fromtimestamp(self.GetCurrentServerSessionEndTime())}")

        for username in self.users:
            user = self.users[username]
            print(f"{user._username} - {user._logins} - {user._timeplayed} - {user._deathcount}")
            #self._death_types = {}
        for sessions in self.gamesessions:
            print(f"{sessions._starttime} - {sessions._endtime}")
#        for timeupdate in self.timeupdates:
#            print("{} - {} - {} - {}".format(timeupdate._updatetime,timeupdate._gametime,timeupdate.estgametime(),timeupdate.eststarttime()))



def main():
    print("BCLogFiles: Unit Testing")
    bclf = BCLogFiles()
    while(True):
        bclf.UpdateLogInfo()
        bclf.PrintDebug()
        sleep(2)


if __name__ == '__main__':
    main()