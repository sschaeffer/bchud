#!/usr/bin/env python3

from bclevelfile import BCLevelFile
from bclogfiles import BCLogFiles
from bclog import BCLog

from time import sleep

class BCGameInstance():

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

    def Thundering(self):
        return(self._bclevelfile.Thundering())

    def ThunderTime(self):
        return(self._bclevelfile.ThunderTime())

    def EstimatedThunderTime(self):
        return(self._bclevelfile.EstimatedThunderTime())

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

    def UpdateGameInfo(self):
        self._bclevelfile.UpdateLevelInfo()
        self._bclogfiles.UpdateLogInfo()

        if(self._logresults):
            self._bclog.LogResults(self._bclevelfile,self._bclogfiles)

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