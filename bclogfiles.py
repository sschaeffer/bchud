#!/usr/bin/env python3

from pathlib import Path
from datetime import date, datetime, timedelta
from time import time, strptime
from os import kill, listdir
import re
import gzip

REGEX_LOGIN_USERNAME = re.compile("\[Server thread\/INFO\]: ([^]]+)\[")
REGEX_LOGOUT_USERNAME = re.compile("\[Server thread\/INFO\]: ([^ ]+) lost connection")
REGEX_KICK_USERNAME = re.compile("\[INFO\] CONSOLE: Kicked player ([^ ]*)")
REGEX_NETHER_USERNAME = re.compile("\[Server thread\/INFO\]: ([^ ]+) has reached the goal \[We Need to Go Deeper\]")
REGEX_THEEND_USERNAME = re.compile("\[Server thread\/INFO\]: ([^ ]+) has reached the goal \[The End\?\]")
REGEX_KILL_DRAGON_USERNAME = re.compile("\[Server thread\/INFO\]: ([^ ]+) has reached the goal \[Free the End\]")
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
    "was impaled.*",
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
        self._deathtime = 0
        self._deathcount = 0
        self._deathtypes = {}
        self._prevlogin = None
        self._netherentry = None
        self._endentry = None
        self._dragonkilled = None

    def Login(self, timestamp):
        self._logins += 1
        self._prevlogin = timestamp

    def Logout(self, timestamp):
        if self._prevlogin is None:
            return
        session = timestamp - self._prevlogin
        self._timeplayed += session
        self._prevlogin = None

    def NetherEntry(self, timestamp):
        if self._prevlogin is not None and self._netherentry is None:
            currentsession = timestamp - self._prevlogin
            self._netherentry = self._timeplayed + currentsession

    def EndEntry(self, timestamp):
        if self._prevlogin is not None and self._endentry is None:
            currentsession = timestamp - self._prevlogin
            self._endentry = self._timeplayed + currentsession

    def KilledTheDragon(self, timestamp):
        if self._prevlogin is not None and self._dragonkilled is None:
            currentsession = timestamp - self._prevlogin
            self._dragonkilled = self._timeplayed + currentsession

    def Death(self, timestamp, typeofdeath):
        if self._prevlogin is not None:
            currentsession = timestamp - self._prevlogin
            self._deathtime = self._timeplayed + currentsession
            self._deathcount += 1
            if typeofdeath not in self._deathtypes:
                self._deathtypes[typeofdeath] = 0
            self._deathtypes[typeofdeath] += 1

    def PrintTimePlayed(self):
        return(f"{timedelta(seconds=self._timeplayed)}")

    def PrintNetherEntry(self):
        return(f"{timedelta(seconds=self._netherentry)}")

    def PrintEndEntry(self):
        return(f"{timedelta(seconds=self._endentry)}")

    def PrintDragonKilled(self):
        return(f"{timedelta(seconds=self._dragonkilled)}")

    def PrintDeathTime(self):
        return(f"{timedelta(seconds=self._deathtime)}")

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

    def EstimatedGameTime(self):
        return(self._gametime+round((time()-self._updatetime.timestamp())*20))

    def EstimatedStartTime(self):
        return(self._updatetime.timestamp()-(self._gametime/20))

class BCLogEvent():

    def __init__(self, timestamp, logeventmessage):
        self._timestamp = timestamp
        self._logeventmessage = logeventmessage 

    def PrintTimeStamp(self):
        return(f"{datetime.fromtimestamp(self._timestamp).strftime('%Y-%m-%d %H:%M:%S')}")

    def PrintEventMessage(self):
        return(self._logeventmessage)


class BCLogFiles():

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot", bclog=None):

        self.minecraftdir=minecraftdir
        self.servername=servername

        self.logevents = [] 
        self.timeupdates = [] 
        self.lastfileupdate=0
        self.currentserversessionstart=0
        self.currentserversessionend=0

        self.users={}

        self.fileBytePosition = 0

    def LogFilename(self):
        return(self.minecraftdir+"/"+self.servername+"/logs/latest.log")

    def GrepForDeathMessage(self,line):
        for regex in REGEX_DEATH_MESSAGES:
            search = regex.search(line)
            if search:
                return search.group(1), search.group(2)
        return None, None

    def ParseLine(self, line, logdate):
        line = line.rstrip()
#        print(line)


        if "For help, type" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            self.currentserversessionstart = logdatetime
            self.currentserversessionend = 0
            self.logevents.append(BCLogEvent(logdatetime,"Server session started"))

        elif "Stopping the server" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            self.currentserversessionend = logdatetime
            self.logevents.append(BCLogEvent(logdatetime,"Server session ended"))

        elif "The time is" in line:
            updatetime = datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()
            updatedatetime = datetime.combine(date.today(),updatetime)
            gametime = int(line.split(" ")[6])
            self.timeupdates.append(BCLogFilesTimeUpdate(updatedatetime,gametime))

        elif "logged in with entity id" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            search = REGEX_LOGIN_USERNAME.search(line)
            if(search):
                username = search.group(1).lstrip().rstrip()
                if username not in self.users:
                    self.users[username] = BCUserStats(username)
                user: BCUserStats = self.users[username]
                user.Login(logdatetime)
                self.logevents.append(BCLogEvent(logdatetime,f"{user._username} logged in {user.PrintTimePlayed()}"))

        elif "lost connection" in line or "[INFO] CONSOLE: Kicked player" in line:
            username = "" 
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            if "lost connection" in line:
                search = REGEX_LOGOUT_USERNAME.search(line)
                if(search):
                    username = search.group(1).lstrip().rstrip()
            else:
                search = REGEX_KICK_USERNAME.search(line)
                if(search):
                    username = search.group(1).lstrip().rstrip()

            if username in self.users:
                user = self.users[username]
                user.Logout(logdatetime)
                self.logevents.append(BCLogEvent(logdatetime,f"{user._username} logged out {user.PrintTimePlayed()}"))

        elif "We Need to Go Deeper" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_NETHER_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in self.users:
                user = self.users[username]
                user.NetherEntry(logdatetime)
                self.logevents.append(BCLogEvent(logdatetime,f"{user._username} entered the nether at {user.PrintNetherEntry()}"))

        elif "The End?" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_THEEND_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in self.users:
                user = self.users[username]
                user.EndEntry(logdatetime)
                self.logevents.append(BCLogEvent(logdatetime,f"{user._username} entered the end at {user.PrintEndEntry()}"))

        elif "Free the End" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_KILL_DRAGON_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in self.users:
                user = self.users[username]
                user.KilledTheDragon(logdatetime)
                self.logevents.append(BCLogEvent(logdatetime,f"{user._username} win - killed the dragon at {user.PrintDragonKilled()}"))

        else:
            username, typeofdeath = self.GrepForDeathMessage(line)
            if(username != None):
                logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
                if username in self.users:
                    user = self.users[username]
                    user.Death(logdatetime,typeofdeath)
                    self.logevents.append(BCLogEvent(logdatetime,f"{username} death - {typeofdeath} {user.PrintDeathTime()}"))

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
            if(self.fileBytePosition == 0):
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

    def ServerStartTime(self):
        return self.currentserversessionstart

    def ServerActive(self):
        if(self.currentserversessionend==0):
            return True
        else:
            return False

    def ServerStarted(self):
        if(self.currentserversessionstart==0):
            return False
        else:
            return True

    def NumLogEvents(self):
        return len(self.logevents)

    def GetLogEvent(self,eventid):
        return f"{self.logevents[eventid].PrintTimeStamp()} LogEvent: {eventid+1}, {self.logevents[eventid].PrintEventMessage()}"

    def PrintDebug(self):

        if(not self.ServerStarted()):
            print("Server isn't started")
        else:
            print(f"Current Server Session Start Time is: {datetime.fromtimestamp(self.currentserversessionstart)}")
            if(not self.ServerActive()):
               print(f"Current Server Session End Time is:   {datetime.fromtimestamp(self.GetCurrentServerSessionEndTime())}")
            for i in range(self.NumLogEvents()):
                print(self.GetLogEvent(i))


    #    for username in self.users:
#
#            user: BCUserStats = self.users[username]
#            print(f"{user._username} - {user._logins} - {user._timeplayed} - {user._deathcount}")
#            if(not user._prevlogin):
#                print(f"{user._username} is not currently logged in")
#            #self._death_types = {}
#        for sessions in self.gamesessions:
#            print(f"{sessions._starttime} - {sessions._endtime}")
##        for timeupdate in self.timeupdates:
#            print("{} - {} - {} - {}".format(timeupdate._updatetime,timeupdate._gametime,timeupdate.estgametime(),timeupdate.eststarttime()))



def main():
    print("BCLogFiles: Unit Testing")
    bclf = BCLogFiles()
    bclf.UpdateLogInfo()
    bclf.PrintDebug()

#    while(True):
#        bclf.UpdateLogInfo()
#        bclf.PrintDebug()
#        sleep(2)


if __name__ == '__main__':
    main()