#!/usr/bin/env python3

from pathlib import Path
from datetime import date, datetime, timedelta
from time import time, strptime
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

class UserStats:
    def __init__(self, username=""):
        self._username = username
        self._logins = 0
        self._time = timedelta()
        
        self.death_count = 0
        self._death_types = {}

    def logout(self, date):
        if self._prev_login is None:
            return
        session = date - self._prev_login
        self._time += session
        self._prev_login = None

    @property
    def username(self):
        return self._username

    @property
    def logins(self):
        return self._logins

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

    def estgametime(self):
        return(self._gametime+round((time()-self._updatetime.timestamp())*20))

    def eststarttime(self):
        return(self._updatetime.timestamp()-(self._gametime/20))

class BCLogFiles():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot"):

        self.minecraftdir=minecraftdir
        self.servername=servername

        self.updates = [] 
        self.updatetimes = [] 
        self.lastupdatetime=0
        self.starttime=0
        self.users={}

        self.fileBytePosition = 0

    def ParseLine(self, line, logdate):
        line = line.rstrip()
        print(line)

        if "logged in with entity id" in line:
            username = (REGEX_LOGIN_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username not in self.users:
                self.users[username] = UserStats(username)
            user = self.users[username]
            user._logins += 1
            user._prev_login = logdate

        if "lost connection" in line or "[INFO] CONSOLE: Kicked player" in line:
            username = "" 
            if "lost connection" in line:
                username = (REGEX_LOGOUT_USERNAME.search(line)).group(1).lstrip().rstrip()
            else:
                username = (REGEX_KICK_USERNAME.search(line)).group(1).lstrip().rstrip()

            if username in users:
                user = user[username]
                user.handle_logout(logdate)

        if "For help, type" in line:
            starttime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            if starttime != self.starttime:
                self.starttime = starttime
#                self.bclog.Write(f"Server boot time: {datetime.fromtimestamp(starttime)}\n")

        if "We Need to Go Deeper" in line:
            username = (REGEX_NETHER_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in users:
                user = user[username]
                user.handle_logout(logdate)

        if "The time is" in line:
            updatetime = datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()
            updatedatetime = datetime.combine(date.today(),updatetime)
            if updatedatetime not in self.updatetimes:
                gametime = int(line.split(" ")[6])
                self.updatetimes.append(updatedatetime)
                self.updates.append(BCLogFilesTimeUpdate(updatedatetime,gametime))

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

    def ReadLogFile(self):
        logfilepath = Path(self.minecraftdir+"/"+self.servername+"/logs/latest.log")
        if logfilepath.exists():
            if self.lastupdatetime != logfilepath.stat().st_mtime:
                self.lastupdatetime = logfilepath.stat().st_mtime
                logfile = open(logfilepath,'r')
                logfile.seek(self.fileBytePosition)
                for line in logfile:
                   self.ParseLine(line,date.today())
                self.fileBytePosition = logfile.tell()
                logfile.close()

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
    print("BCLogFiles: Unit Testing")
    bclf = BCLogFiles()
    bclf.ReadPreviousLogFiles()
    bclf.ReadLogFile()
    
if __name__ == '__main__':
    main()