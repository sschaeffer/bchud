#!/usr/bin/env python3

from bclevelfile import BCLevelFile
from bclogfiles import BCLogFiles
from bclog import BCLog

from time import sleep, time
from subprocess import call

class BCGameInstance():

    DAWN=BCLevelFile.DAWN           # LIGHT ORANGE (1min 40secs)
    WORKDAY=BCLevelFile.WORKDAY        # LIGHT YELLOW (5mins 50secs)
    HAPPYHOUR=BCLevelFile.HAPPYHOUR      # LIGHT MAROON (2mins 30secs)
    TWILIGHT=BCLevelFile.TWILIGHT       # LIGHT PURPLE (27secs)
    SLEEP=BCLevelFile.SLEEP          # DARK BLUE (21secs)
    MONSTERS=BCLevelFile.MONSTERS       # DARKEST BLUE/BLACK (8mins 1secs)
    NOMONSTERS=BCLevelFile.NOMONSTERS     # BLUE (11 secs)
    NOSLEEP=BCLevelFile.NOSLEEP        # MAUVE (27secs)

    DAY_DAWN=BCLevelFile.DAY_DAWN               #     0 DAWN Wakeup and Wander (0:00)
    DAY_WORKDAY=BCLevelFile.DAY_WORKDAY        #  2000 WORKDAY (1:40)
    DAY_HAPPYHOUR=BCLevelFile.DAY_HAPPYHOUR      #  9000 HAPPY-HOUR (7:30)
    DAY_TWILIGHT=BCLevelFile.DAY_TWILIGHT     # 12000 TWILIGHT/villagers sleep (10:00)
    RAIN_SLEEP=BCLevelFile.RAIN_SLEEP         # 12010 SLEEP on rainy days (10:00)
    DAY_SLEEP=BCLevelFile.DAY_SLEEP       # 12542 SLEEP on normal days/mobs don't burn (10:27.1/0)
    RAIN_MONSTERS=BCLevelFile.RAIN_MONSTERS      # 12969 Rainy day monsters (10:48.45/21)
    DAY_MONSTERS=BCLevelFile.DAY_MONSTERS       # 13188 Monsters (10:59.4/32)
    DAY_NOMONSTERS=BCLevelFile.DAY_NOMONSTERS     # 22812 No more monsters (19:00.6/8:33)
    RAIN_NOMONSTERS=BCLevelFile.RAIN_NOMONSTERS    # 23031 No more rainy day monsters(19:11.55/8:44)
    DAY_NOSLEEP=BCLevelFile.DAY_NOSLEEP        # 23460 No sleeping on normal days (19:33/9:06)
    RAIN_NOSLEEP=BCLevelFile.RAIN_NOSLEEP        # 23992 No sleeping rainy days (19:59/9:33)
    DAY_FULLDAY=BCLevelFile.DAY_FULLDAY        # 24000 Full-day

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="snapshot", worldname="snapshot", logresults=True):

        self._logresults=logresults
        self._minecraftdir=minecraftdir
        self._servername=servername
        self._worldname=worldname

        self._bclevelfile = BCLevelFile(minecraftdir, servername, worldname)
        self._bclogfiles = BCLogFiles(minecraftdir, servername)
        #self.bcalladvancements = BCAllAdancements(minecraftdir, servername)
        #self.bcuseradvancements = BCUserAdancements(minecraftdir, servername)

        self._bclog = BCLog(minecraftdir,servername)

    def LogFilename(self):
        return(self._bclogfiles.LogFilename())

    def LevelFilename(self):
        return(self._bclevelfile.LevelFilename())

    def LevelFileLastUpdate(self):
        return(self._bclevelfile.LevelFileLastUpdate())

    def Seed(self):
        return(self._bclevelfile.Seed())

    def GameTime(self):
        return(self._bclevelfile.GameTime())

    def EstimatedGameTime(self):
        return(self._bclevelfile.EstimatedGameTime())

    def DayTime(self):
        return(self._bclevelfile.DayTime())

    def EstimatedDayTime(self):
        return(self._bclevelfile.EstimatedDayTime())

    def ClearWeatherTime(self):
        return(self._bclevelfile.ClearWeatherTime())

    def EstimatedClearWeatherTime(self):
        return(self._bclevelfile.EstimatedClearWeatherTime())

    def Raining(self):
        return(self._bclevelfile.Raining())

    def RainTime(self):
        return(self._bclevelfile.RainTime())

    def EstimatedRainTime(self):
        return(self._bclevelfile.EstimatedRainTime())

    def EstimatedIsRaining(self):
        return(self._bclevelfile.EstimatedIsRaining())

    def Thundering(self):
        return(self._bclevelfile.Thundering())

    def ThunderTime(self):
        return(self._bclevelfile.ThunderTime())

    def EstimatedThunderTime(self):
        return(self._bclevelfile.EstimatedThunderTime())

    def EstimatedIsThundering(self):
        return(self._bclevelfile.EstimatedIsThundering())

    def WanderingTraderSpawnDelay(self):
        return(self._bclevelfile.WanderingTraderSpawnDelay())

    def EstimatedWanderingTraderSpawnDelay(self):
        return(self._bclevelfile.EstimatedWanderingTraderSpawnDelay())

    def WanderingTraderSpawnChance(self):
        return(self._bclevelfile.WanderingTraderSpawnChance())

    def WanderingTraderID(self):
        return(self._bclevelfile.WanderingTraderID())

    def EstimatedTimeOfDay(self):
        return(self._bclevelfile.EstimatedTimeOfDay())

    def EstimatedIsMonsters(self):
        return(self._bclevelfile.EstimatedIsMonsters())

    def EstimatedIsBedUsable(self):
        return(self._bclevelfile.EstimatedIsBedUsable())

    def ServerActive(self):
        return(self._bclogfiles.ServerActive())

    def ServerStartTime(self):
        return(self._bclogfiles.ServerStartTime())

    def UpdateGameInfo(self):

        self._bclogfiles.UpdateLogInfo()
        self._bclevelfile.UpdateLevelInfo(self.ServerActive(),self.ServerStartTime())

        if(self._logresults):
            self._bclog.LogResults(self._bclevelfile,self._bclogfiles)

    def SaveAllFiles():
        call(["./save-it-all.bash"])
        sleep(0.5)

    def QueryTime():
        call(["./query-time.bash"])
        sleep(0.5)

    def PrintDebug(self):
        print(f"Level File:          {self.LevelFilename()}")
        print(f"Last Update Time:    {self.LevelFileLastUpdate()}")
        print(f"Seed:                {self.Seed()}")
        print(f"Game Time:           {self.GameTime()}")
        print(f"Estimated Game Time: {self.EstimatedGameTime()}")
        print(f"Day Time:            {self.DayTime()}")
        print(f"Estimated Day Time:  {self.EstimatedDayTime()}")
        print(f"Clear Weather Time:  {self.ClearWeatherTime()}")
        print(f"Estimated Clear Wea: {self.EstimatedClearWeatherTime()}")
        print(f"Raining:             {self.Raining()}")
        print(f"Rain Time:           {self.RainTime()}")
        print(f"Estimated Rain Time: {self.EstimatedRainTime()}")
        print(f"Thundering:          {self.Thundering()}")
        print(f"Thunder Time:        {self.ThunderTime()}")
        print(f"Estimated Thunder T: {self.EstimatedThunderTime()}")
        print(f"Wandering Trader Sp: {self.WanderingTraderSpawnDelay()}")
        print(f"Estimated Wandering: {self.EstimatedWanderingTraderSpawnDelay()}")
        print(f"Wandering Trader Sp: {self.WanderingTraderSpawnChance()}")
        print(f"Wandering Trader Id: {self.WanderingTraderID()}")
        print(f"Estimated Time of D: {self.EstimatedTimeOfDay()}")

def main():

    print("BCGameInstance: Unit Testing")
    bcgame = BCGameInstance()

    bcgame.UpdateGameInfo()
    while True:
        bcgame.UpdateGameInfo()
        sleep(2)
#    bcgame.PrintDebug()


if __name__ == '__main__':
    main()