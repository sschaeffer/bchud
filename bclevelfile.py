#!/usr/bin/python3

from nbt import NBTFile
from bclogfile import BCLogFile
from bclog import BCLog

from time import time, sleep , strftime, strptime
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import call

class BCLevelFile(NBTFile):

    DAWN=1           # LIGHT ORANGE (1min 40secs)
    WORKDAY=2        # LIGHT YELLOW (5mins 50secs)
    HAPPYHOUR=3      # LIGHT MAROON (2mins 30secs)
    TWILIGHT=4       # LIGHT PURPLE (27secs)
    SLEEP=5          # DARK BLUE (21secs)
    MONSTERS=6       # DARKEST BLUE/BLACK (8mins 1secs)
    NOMONSTERS=7     # BLUE (11 secs)
    NOSLEEP=8        # MAUVE (27secs)

    DAY_DAWN=0               #     0 DAWN Wakeup and Wander (0:00)
    DAY_WORKDAY=2000         #  2000 WORKDAY (1:40)
    DAY_HAPPYHOUR=9000       #  9000 HAPPY-HOUR (7:30)
    DAY_TWILIGHT=12000       # 12000 TWILIGHT/villagers sleep (10:00)
    RAIN_SLEEP=12010         # 12010 SLEEP on rainy days (10:00)
    DAY_SLEEP=12542          # 12542 SLEEP on normal days/mobs don't burn (10:27.1/0)
    RAIN_MONSTERS=12969      # 12969 Rainy day monsters (10:48.45/21)
    DAY_MONSTERS=13188       # 13188 Monsters (10:59.4/32)
    DAY_NOMONSTERS=22812     # 22812 No more monsters (19:00.6/8:33)
    RAIN_NOMONSTERS=23031    # 23031 No more rainy day monsters(19:11.55/8:44)
    DAY_NOSLEEP=23460        # 23460 No sleeping on normal days (19:33/9:06)
    RAIN_NOSLEEP=23992        # 23992 No sleeping rainy days (19:59/9:33)
    DAY_FULLDAY=24000        # 24000 Full-day 

#    RAINMONSTERS=6   # DARK BLUE (11secs)
#    NORAINMONSTERS=9 # LIGHTER BLUE/PINK (22secs)

    def __init__(self, bclf=None, bclog=None, levelfilename="level.dat"):

        self.levelfilename=levelfilename

        self.bclf=bclf
        self.bclog=bclog
        if(self.bclog == None):
            self.bclog = BCLog()

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
        self.wanderingtraderspawnchance=0
        self.wanderingtraderspawndelay=0

    def ReadLevelFile(self):
        levelfilepath = Path(self.bclog.ServerWorldDir()+"/"+self.levelfilename)
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

                self.bclog.Write("{},".format(datetime.fromtimestamp(self.lastupdatetime).strftime("%H:%M:%S")))
                self.bclog.Write("{},".format(self.gametime))
                self.bclog.Write("{},".format(self.daytime))
                self.bclog.Write("{},".format(self.clearweathertime))
                self.bclog.Write("{},".format(self.raining))
                self.bclog.Write("{},".format(self.raintime))
                self.bclog.Write("{},".format(self.thundering))
                self.bclog.Write("{},".format(self.thundertime))
                self.bclog.Write("{},".format(self.wanderingtraderspawndelay))
                self.bclog.Write("{},".format(self.wanderingtraderspawnchance))
                self.bclog.Write("{}\n".format(self.wanderingtraderid))

    def EstimatedGameTime(self):
        result = 0
        if self.gametime > 0:
            result = round(self.gametime+((time()-self.lastupdatetime)*20))
        elif self.bclf.GetStarttime() > 0:
            result = round(time()-self.bclf.GetStarttime())*20
        return result

    def EstimatedDayTime(self):
        result = 0
        if self.daytime > 0:
            # if self.daytime is less than zero or zero it means the game is still starting
            result = round(self.daytime+((time()-self.lastupdatetime)*20))
        elif self.bclf.GetStarttime() > 0:
            result = round(time()-self.bclf.GetStarttime())*20
        return result

    def EstimatedClearWeatherTime(self):
        return round(self.clearweathertime-((time()-self.lastupdatetime)*20))

    def EstimatedRainTime(self):
        result = 0
        if self.raintime != 0:
            result = round(self.raintime-((time()-self.lastupdatetime)*20))
        return result

    def EstimatedThunderTime(self):
        result = 0
        if self.raintime != 0:
            result = round(self.thundertime-((time()-self.lastupdatetime)*20))
        return result

    def EstimatedWanderingTraderSpawnDelay(self):
        return round(self.wanderingtraderspawndelay-((time()-self.lastupdatetime)*20))

    def EstimatedIsRaining(self):
        result = False 
        if self.raining and self.EstimatedRainTime() > 0:
            result = True
        elif not self.raining and self.EstimatedRainTime() < 0:
            result = True
        return(result)

    def EstimatedIsThundering(self):
        result = False 
        if self.EstimatedIsRaining() and self.thundering and self.EstimatedThunderTime() > 0:
            result = True
        elif self.EstimatedIsRaining() and not self.thundering and self.EstimatedThunderTime() < 0:
            result = True
        return(result)

    def EstimatedIsMonsters(self):
        estdaytime = self.EstimatedDayTime()%self.DAY_FULLDAY
        result = False
        if estdaytime >= self.DAY_MONSTERS and estdaytime <= self.DAY_NOMONSTERS:
            result = True 
        return result 

    def EstimatedIsBedUsable(self):
        estdaytime = self.EstimatedDayTime()%self.DAY_FULLDAY
        result = False
        if estdaytime >= self.DAY_SLEEP and estdaytime <= self.DAY_NOSLEEP:
            result = True 
        return result

    def EstimatedTimeOfDay(self):
        estdaytime = self.EstimatedDayTime()%self.DAY_FULLDAY
        if estdaytime > self.DAY_NOSLEEP:
            result = self.NOSLEEP
        elif estdaytime > self.DAY_NOMONSTERS:
            result = self.NOMONSTERS     # LIGHT BLUE (11 secs)
        elif estdaytime > self.DAY_MONSTERS:
            result = self.MONSTERS       # DARKEST BLUE/BLACK (8mins 1secs)
        elif estdaytime > self.DAY_SLEEP:
            result = self.SLEEP          # DARK BLUE PURPLE (21secs)
        elif estdaytime > self.DAY_TWILIGHT:
            result = self.TWILIGHT       # PURPLE (27secs)
        elif estdaytime > self.DAY_HAPPYHOUR:
            result = self.HAPPYHOUR      # LIGHT BLUE/PURPLE (2mins 30secs)
        elif estdaytime > self.DAY_WORKDAY:
            result = self.WORKDAY        # YELLOW (5mins 50secs)
        else:
            result = self.DAWN           # BRIGHT YELLOW (1min 40secs)
        return(result)

#        elif estdaytime > self.DAY_NORAINMONSTERS:
#            result = self.NORAINMONSTERS # LIGHTER BLUE/PINK (22secs)
#        elif estdaytime > self.DAY_RAINMONSTERS:
#            result = self.RAINMONSTERS   # DARK BLUE (11secs)
def main():
    print("BCLevelFile: Unit Testing")
    bclevelfile = BCLevelFile()
    bclevelfile.ReadLevelFile()

    if bclevelfile.lastupdatetime != 0:
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
        print("Estimated Time of D: {}".format(bclevelfile.EstimatedTimeOfDay()))
    else:
        print("No level.dat file")


if __name__ == '__main__':
    main()