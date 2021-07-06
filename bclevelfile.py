#!/usr/bin/env python3

from nbt import NBTFile

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

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot", worldname="snapshot", serveractive=False, serverstarttime=0):

        self.minecraftdir=minecraftdir
        self.servername=servername
        self.worldname=worldname
        self.levelfilename="level.dat"

        self._serveractive=serveractive
        self._serverstarttime=serverstarttime

        self.lastupdatetime=0
        self.seed=None
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
        self.bclogfile = None

    def LevelFilename(self):
        return(self.minecraftdir+"/"+self.servername+"/"+self.worldname+"/"+self.levelfilename)

    def LevelFileLastUpdate(self):
        return(self.lastupdatetime)

    def Seed(self):
        return(self.seed)

    def GameTime(self):
        return(self.gametime)

    def DayTime(self):
        return(self.daytime)

    def ClearWeatherTime(self):
        return(self.clearweathertime)

    def Raining(self):
        return(self.raining)

    def RainTime(self):
        return(self.raintime)

    def Thundering(self):
        return(self.thundering)

    def ThunderTime(self):
        return(self.thundertime)

    def WanderingTraderSpawnDelay(self):
        return(self.wanderingtraderspawndelay)

    def WanderingTraderSpawnChance(self):
        return(self.wanderingtraderspawnchance)

    def WanderingTraderID(self):
        return(self.wanderingtraderid)


    def ReadLevelFile(self, levelfilepath):

        if self.lastupdatetime != levelfilepath.stat().st_mtime:
        # file has changed so lets save the previous results

            self.lastupdatetime = levelfilepath.stat().st_mtime
            super(BCLevelFile, self).__init__(levelfilepath)

            if "seed" in self["Data"]["WorldGenSettings"]:
                self.seed=str(self["Data"]["WorldGenSettings"]["seed"])

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

 
    def UpdateLevelInfo(self,serveractive,serverstarttime):
        levelfilepath = Path(self.LevelFilename())
        if not levelfilepath.exists():
            # game was reset or hasn't started yet. level_dat doesn't exist
            # also re-read the logs from scratch
            self.__init__(serveractive=serveractive,serverstarttime=serverstarttime)
        else:
            self._serveractive = serveractive
            self._serverstarttime = serverstarttime
            self.ReadLevelFile(levelfilepath)

    def EstimatedGameTime(self):
        result = 0
        if not self._serveractive:
            result = self.GameTime()
        elif self.gametime > 0:
            result = round(self.gametime+((time()-self.lastupdatetime)*20))
        elif self._serverstarttime > 0:
            result = round(time()-self._serverstarttime)*20
        return result


    def EstimatedDayTime(self):
        result = 0
        if not self._serveractive:
            result = self.DayTime()
        elif self.daytime > 0:
            # if self.daytime is less than zero or zero it means the game is still starting
            result = round(self.daytime+((time()-self.lastupdatetime)*20))
        elif self._serverstarttime > 0:
            result = round(time()-self._serverstarttime)*20
        return result

    def EstimatedClearWeatherTime(self):
        result=0
        if self.clearweathertime > 0:
            result = round(self.clearweathertime-((time()-self.lastupdatetime)*20))
        return result

    def EstimatedRainTime(self):
        result = 0
        if self.raintime != 0:
            result = round(self.raintime-((time()-self.lastupdatetime)*20))
        return result

    def EstimatedThunderTime(self):
        result = 0
        if self.thundertime != 0:
            result = round(self.thundertime-((time()-self.lastupdatetime)*20))
        return result

    def EstimatedWanderingTraderSpawnDelay(self):
        result = 0
        if self.wanderingtraderspawndelay != 0:
            result = round(self.wanderingtraderspawndelay-((time()-self.lastupdatetime)*20))
        return result

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

    bclevelfile.UpdateLevelInfo(False,0)
    if bclevelfile.LevelFileLastUpdate() == 0:
        print("No level.dat file")
#        print(bclevelfile.pretty_tree())

    print(f"Level Filename:      {bclevelfile.LevelFilename()}")
    print(f"Last Update Time:    {datetime.fromtimestamp(bclevelfile.LevelFileLastUpdate())}")
    print(f"Seed:                {bclevelfile.Seed()}")
    print(f"Game Time:           {bclevelfile.GameTime()}")
    print(f"Estimated Game Time: {bclevelfile.EstimatedGameTime()}")
    print(f"Day Time:            {bclevelfile.DayTime()}")
    print(f"Estimated Day Time:  {bclevelfile.EstimatedDayTime()}")
    print(f"Clear Weather Time:  {bclevelfile.ClearWeatherTime()}")
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

if __name__ == '__main__':
    main()