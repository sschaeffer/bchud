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

    def login(self, timestamp):
        self._logins += 1
        self._prevlogin = timestamp

    def logout(self, timestamp):
        if self._prevlogin is None:
            return
        session = timestamp - self._prevlogin
        self._timeplayed += session
        self._prevlogin = None

    def nether_entry(self, timestamp):
        if self._prevlogin is not None and self._netherentry is None:
            currentsession = timestamp - self._prevlogin
            self._netherentry = self._timeplayed + currentsession

    def end_entry(self, timestamp):
        if self._prevlogin is not None and self._endentry is None:
            currentsession = timestamp - self._prevlogin
            self._endentry = self._timeplayed + currentsession

    def killed_the_dragon(self, timestamp):
        if self._prevlogin is not None and self._dragonkilled is None:
            currentsession = timestamp - self._prevlogin
            self._dragonkilled = self._timeplayed + currentsession

    def death(self, timestamp, typeofdeath):
        if self._prevlogin is not None:
            currentsession = timestamp - self._prevlogin
            self._deathtime = self._timeplayed + currentsession
            self._deathcount += 1
            if typeofdeath not in self._deathtypes:
                self._deathtypes[typeofdeath] = 0
            self._deathtypes[typeofdeath] += 1

    def print_time_played(self):
        return(f"{timedelta(seconds=self._timeplayed)}")

    def print_nether_entry(self):
        return(f"{timedelta(seconds=self._netherentry)}")

    def print_end_entry(self):
        return(f"{timedelta(seconds=self._endentry)}")

    def print_dragon_killed(self):
        return(f"{timedelta(seconds=self._dragonkilled)}")

    def print_death_time(self):
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

    def estimated_game_time(self):
        return(self._gametime+round((time()-self._updatetime.timestamp())*20))

    def estimated_start_time(self):
        return(self._updatetime.timestamp()-(self._gametime/20))

class BCLogEvent():

    def __init__(self, timestamp, logeventmessage):
        self._timestamp = timestamp
        self._logeventmessage = logeventmessage 

    def print_time_stamp(self):
        return(f"{datetime.fromtimestamp(self._timestamp).strftime('%Y-%m-%d %H:%M:%S')}")

    def print_event_message(self):
        return(self._logeventmessage)


class BCLogFiles():

    def __init__(self, minecraftdir="/media/local/Minecraft", servername="fury"):

        self._minecraftdir=minecraftdir
        self._servername=servername

        self._logevents = [] 
        self._timeupdates = [] 
        self._lastfileupdate=0
        self._currentserversessionstart=0
        self._currentserversessionend=0

        self._users={}

        self._filebyteposition = 0

    def log_filename(self):
        return(self._minecraftdir+"/saves/"+self._servername+"/logs/latest.log")

    def grep_for_death_message(self,line):
        for regex in REGEX_DEATH_MESSAGES:
            search = regex.search(line)
            if search:
                return search.group(1), search.group(2)
        return None, None

    def parse_line(self, line, logdate):
        line = line.rstrip()

        if "For help, type" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            self._currentserversessionstart = logdatetime
            self._currentserversessionend = 0
            self._logevents.append(BCLogEvent(logdatetime,"Server session started"))

        elif "Stopping the server" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            self._currentserversessionend = logdatetime
            self._logevents.append(BCLogEvent(logdatetime,"Server session ended"))

        elif "The time is" in line:
            updatetime = datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()
            updatedatetime = datetime.combine(date.today(),updatetime)
            gametime = int(line.split(" ")[6])
            self._timeupdates.append(BCLogFilesTimeUpdate(updatedatetime,gametime))

        elif "logged in with entity id" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            search = REGEX_LOGIN_USERNAME.search(line)
            if(search):
                username = search.group(1).lstrip().rstrip()
                if username not in self._users:
                    self._users[username] = BCUserStats(username)
                user: BCUserStats = self._users[username]
                user.login(logdatetime)
                self._logevents.append(BCLogEvent(logdatetime,f"{user._username} logged in {user.print_time_played()}"))

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

            if username in self._users:
                user = self._users[username]
                user.logout(logdatetime)
                self._logevents.append(BCLogEvent(logdatetime,f"{user._username} logged out {user.print_time_played()}"))

        elif "We Need to Go Deeper" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_NETHER_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in self._users:
                user = self._users[username]
                user.nether_entry(logdatetime)
                self._logevents.append(BCLogEvent(logdatetime,
                    f"{user._username} entered the nether at {user.print_nether_entry()}"))

        elif "The End?" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_THEEND_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in self._users:
                user = self._users[username]
                user.end_entry(logdatetime)
                self._logevents.append(BCLogEvent(logdatetime,
                                    f"{user._username} entered the end at {user.print_end_entry()}"))

        elif "Free the End" in line:
            logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
            username = (REGEX_KILL_DRAGON_USERNAME.search(line)).group(1).lstrip().rstrip()
            if username in self._users:
                user = self._users[username]
                user.killed_the_dragon(logdatetime)
                self._logevents.append(BCLogEvent(logdatetime,
                                            f"{user._username} win - killed the dragon at {user.print_dragon_killed()}"))

        else:
            username, typeofdeath = self.grep_for_death_message(line)
            if(username != None):
                logdatetime = datetime.combine(logdate,datetime.strptime(line.split(" ")[0], "[%H:%M:%S]").time()).timestamp()
                if username in self._users:
                    user = self._users[username]
                    user.death(logdatetime,typeofdeath)
                    self._logevents.append(BCLogEvent(logdatetime,
                                                        f"{username} death - {typeofdeath} {user.print_death_time()}"))

    def read_previous_log_files(self):
        for logname in sorted(listdir(self._minecraftdir+"/saves/"+self._servername+"/logs")):
            if not re.match("\d{4}-\d{2}-\d{2}-\d+\.log\.gz", logname):
                continue
            d = strptime("-".join(logname.split("-")[:3]), "%Y-%m-%d")
            day = date(*(d[0:3]))
            logfile = gzip.open(Path(self._minecraftdir+"/"+self._servername+"/logs",logname), 'rt')
            for line in logfile:
                self.parse_line(line, day)
            logfile.close()

    def read_log_file(self, logfilepath):

        if self._filebyteposition > logfilepath.stat().st_size:
            # Server might have restarted so we need to reinit
            self._filebyteposition = 0
            self.update_log_info()
        else:
            if self._lastfileupdate != logfilepath.stat().st_mtime and self._filebyteposition < logfilepath.stat().st_size:
                self._lastfileupdate = logfilepath.stat().st_mtime
                logfile = open(logfilepath,'r')
                logfile.seek(self._filebyteposition)
                for line in logfile:
                    self.parse_line(line,date.today())
                self._filebyteposition = logfile.tell()
                logfile.close()

    def update_log_info(self):
        logfilepath = Path(self.log_filename())
        if not logfilepath.exists():
            # Log file was deleted so re-init the stats
            self.__init__(self._minecraftdir,self._servername)
        else:
            if(self._filebyteposition == 0):
                # First time reading the file so re-init and read previous logs (if any) 
                self.__init__(self._minecraftdir,self._servername)
                self.read_previous_log_files()
            self.read_log_file(logfilepath)

    def num_log_time_updates(self):
        return len(self._timeupdates)

    def get_log_time_update(self,i):
        result = None
        if i >= 0:
            if i < len(self._timeupdates):
                result = self._timeupdates[i]
        return result

    def get_last_log_time_update(self):
        return self.get_log_time_update(self.num_log_time_updates()-1)

    def server_start_time(self):
        return self._currentserversessionstart

    def server_active(self):
        if(self._currentserversessionend==0):
            return True
        else:
            return False

    def server_started(self):
        if(self._currentserversessionstart==0):
            return False
        else:
            return True

    def num_log_events(self):
        return len(self._logevents)

    def get_log_event(self,eventid):
        return f"{self._logevents[eventid].print_time_stamp()} LogEvent: {eventid+1}, {self._logevents[eventid].print_event_message()}"

    def print_debug(self):

        if(not self.server_started()):
            print("Server isn't started")
        else:
            print(f"Current Server Session Start Time is: {datetime.fromtimestamp(self._currentserversessionstart)}")
            if(not self.server_active()):
               print(f"Current Server Session End Time is:   {datetime.fromtimestamp(self._currentserversessionend)}")
        for i in range(self.num_log_events()):
            print(self.get_log_event(i))


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
    bclf.update_log_info()
    bclf.print_debug()

#    while(True):
#        bclf.UpdateLogInfo()
#        bclf.PrintDebug()
#        sleep(2)


if __name__ == '__main__':
    main()