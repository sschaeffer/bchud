#!/usr/bin/python3

from nbt import NBTFile

from time import time, sleep , strftime, strptime
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import call

class BCLevelFile(NBTFile):

    DAWN=0           # BRIGHT YELLOW (1min 40secs)
    WORKDAY=1        # YELLOW (5mins 50secs)
    HAPPYHOUR=2      # LIGHT BLUE/PURPLE (2mins 30secs)
    TWILIGHT=3       # PURPLE (27secs)
    SLEEP=4          # DARK BLUE PURPLE (21secs)
    RAINMONSTERS=5   # DARK BLUE (11secs)
    MONSTERS=6       # DARKEST BLUE/BLACK (8mins 1secs)
    NOMONSTERS=7     # LIGHT BLUE (11 secs)
    NORAINMONSTERS=8 # LIGHTER BLUE/PINK (22secs)
    NOSLEEP=9        # PINK (27secs)

    DAY_DAWN=0               #     0 DAWN Wakeup and Wander (0:00)
    DAY_WORKDAY=2000         #  2000 WORKDAY (1:40)
    DAY_HAPPYHOUR=9000       #  9000 HAPPY-HOUR (7:30)
    DAY_TWILIGHT=12000       # 12000 TWILIGHT/villagers sleep (10:00) - 12010 sleep on rainy days
    DAY_SLEEP=12542          # 12542 SLEEP on normal days/mobs don't burn (10:27.1/0)
    DAY_RAINMONSTERS=12969   # 12969 Rainy day monsters (10:48.45/21)
    DAY_MONSTERS=13188       # 13188 Monsters (10:59.4/32)
    DAY_NOMONSTERS=22812     # 22812 No more monsters (19:00.6/8:33)
    DAY_NORAINMONSTERS=23031 # 12969 No more rainy day monsters(19:11.55/8:44)
    DAY_NOSLEEP=23460        # 23460 No sleeping on normal days (19:33/9:06)
    DAY_FULLDAY=24000        # 23992 No sleeping rainy days (19:59/9:33)
    def __init__(self, levelfilename="snapshot/level.dat", serverdir="", logresults=False):
        if(serverdir!=""):
            self.serverdir = serverdir
        else:
            self.serverdir = "/media/deflection/Minecraft/server/snapshot"
        self.levelfilename=levelfilename

        self.lastupdatetime=0
        self.lastcheckedtime=0

        self.gametime=0
        self.daytime=0
        self.clearweathertime=0
        self.raining=False
        self.raintime=0
        self.thundering=False
        self.thundertime=0
        self.wanderingtraderid="<empty>"
        self.wanderingtraderchance=0
        self.wanderingtradertime=0

        self.logresults = logresults
        if logresults:
            self.logfh = open("{}.{}".format("/tmp/bchud",strftime("%H%M%S")),"w+")

    def ReadLevelFile(self):
        levelfilepath = Path(self.serverdir+"/"+self.levelfilename)
        self.lastcheckedtime = time()
        if levelfilepath.exists():
            if self.lastupdatetime != levelfilepath.stat().st_mtime:
            # file has changed so lets save the previous results

                self.lastupdatetime = levelfilepath.stat().st_mtime
                super(BCLevelFile, self).__init__(levelfilepath)

                if "Time" in self["Data"]:
                    self.gametime=int(str(self["Data"]["Time"]))

                if "DayTime" in self["Data"]:
                    self.daytime=int(str(self["Data"]["DayTime"]))

                if "ClearWeatherTime" in self["Data"]:
                    self.clearweathertime=int(str(self["Data"]["ClearWeatherTime"]))

                if "rainTime" in self["Data"]:
                    self.raintime=int(str(self["Data"]["rainTime"]))

                if "thunderTime" in self["Data"]:
                    self.thundertime=int(str(self["Data"]["thunderTime"]))

                if "WanderingTraderSpawnDelay" in self["Data"]:
                    self.wanderingtraderspawndelay=int(str(self["Data"]["WanderingTraderSpawnDelay"]))

                if "WanderingTraderSpawnChance" in self["Data"]:
                    self.wanderingtraderspawnchance=int(str(self["Data"]["WanderingTraderSpawnChance"]))

                if "WanderingTraderId" in self["Data"]:
                    self.wanderingtraderid=str(self["Data"]["WanderingTraderId"])
                else:
                    self.wanderingtraderid="<empty>"

                if "raining" in self["Data"]:
                    self.raining=bool(int(str(self["Data"]["raining"])))

                if "thundering" in self["Data"]:
                    self.thundering=bool(int(str(self["Data"]["thundering"])))

                if self.logresults:
                    self.logfh.write("{},".format(datetime.fromtimestamp(self.lastupdatetime).strftime("%H:%M:%S")))
                    self.logfh.write("{},".format(self.gametime))
                    self.logfh.write("{},".format(self.daytime))
                    self.logfh.write("{},".format(self.clearweathertime))
                    self.logfh.write("{},".format(self.raining))
                    self.logfh.write("{},".format(self.raintime))
                    self.logfh.write("{},".format(self.thundering))
                    self.logfh.write("{},".format(self.thundertime))
                    self.logfh.write("{},".format(self.wanderingtraderspawndelay))
                    self.logfh.write("{},".format(self.wanderingtraderspawnchance))
                    self.logfh.write("{}\n".format(self.wanderingtraderid))
                    self.logfh.flush()

    def EstimatedGameTime(self):
        result = 0
        if self.gametime > 0:
            result = round(self.gametime+((time()-self.lastupdatetime)*20))
        return result

    def EstimatedDayTime(self):
        result = 0
        if self.daytime > 0:
            result = round(self.daytime+((time()-self.lastupdatetime)*20))
        return result

    def EstimatedClearWeatherTime(self):
        result = round(self.clearweathertime-((time()-self.lastupdatetime)*20))
        if result < 0:
            result = 0
        return result

    def EstimatedRainTime(self):
        result = round(self.raintime-((time()-self.lastupdatetime)*20))
        if result < 0:
            result = 0
        return result

    def EstimatedThunderTime(self):
        result = round(self.thundertime-((time()-self.lastupdatetime)*20))
        if result < 0:
            result = 0
        return result

    def EstimatedWanderingTraderSpawnDelay(self):
        result = round(self.wanderingtraderspawndelay-((time()-self.lastupdatetime)*20))
        if result < 0:
            result = 0
        return result


def main():
    print("BCLevelFile: Unit Testing")
    bclevelfile = BCLevelFile(logresults=True)
    bclevelfile.ReadLevelFile()

    print(bclevelfile.pretty_tree())
    print("Last Checked Time:   {}".format(datetime.fromtimestamp(bclevelfile.lastcheckedtime)))
    print("Last Update Time:    {}".format(datetime.fromtimestamp(bclevelfile.lastupdatetime)))
    print("Game Time:           {}".format(bclevelfile.gametime))
    print("Estimated Game Time: {}".format(bclevelfile.EstimatedGameTime()))
    print("Day Time:            {}".format(bclevelfile.daytime))
    print("Estimated Day Time:  {}".format(bclevelfile.EstimatedDayTime()))
    print("Clear Weather Time:  {}".format(bclevelfile.clearweathertime))
    print("Estimated Clear Wea: {}".format(bclevelfile.EstimatedClearWeatherTime()))
    print("Raining:             {}".format(bclevelfile.raining))
    print("Rain Time:           {}".format(bclevelfile.raintime))
    print("Estimated Rain Time: {}".format(bclevelfile.EstimatedRainTime()))
    print("Thundering:          {}".format(bclevelfile.thundering))
    print("Thunder Time:        {}".format(bclevelfile.thundertime))
    print("Estimated Thunder T: {}".format(bclevelfile.EstimatedThunderTime()))
    print("Wandering Trader Sp: {}".format(bclevelfile.wanderingtraderspawndelay))
    print("Estimated Wandering: {}".format(bclevelfile.EstimatedWanderingTraderSpawnDelay()))
    print("Wandering Trader Sp: {}".format(bclevelfile.wanderingtraderspawnchance))
    print("Wandering Trader Id: {}".format(bclevelfile.wanderingtraderid))

if __name__ == '__main__':
    main()