#!/usr/bin/env python3

from re import X
from bclevelfile import BCLevelFile
from bclogfiles import BCLogFiles
from bclog import BCLog

class BCGameInstance():

    def __init__(self, logresults=True, minecraftdir="/media/local/Minecraft/server", servername="snapshot", worldname="snapshot"):

        self.minecraftdir=minecraftdir
        self.servername=servername
        self.worldname=worldname

        self.bclevelfile = BCLevelFile(minecraftdir, servername, worldname)
        self.bclogfiles = BCLogFiles(minecraftdir, servername)
        self.bclog = BCLog(minecraftdir,servername)

        #self.bcalladvancements = BCAllAdancements(minecraftdir, servername)
        #self.bcuseradvancements = BCUserAdancements(minecraftdir, servername)

    def LogFilename(self):
        return(self.bclogfiles.LogFilename())

    def LevelFilename(self):
        return(self.bclevelfile.LevelFilename())

    def LevelFileLastUpdate(self):
        return(self.bclevelfile.LevelFileLastUpdate())

    def Seed(self):
        return(self.bclevelfile.Seed())

    def GameTime(self):
        return(self.bclevelfile.GameTime())

    def EstimatedGameTime(self):
        return(self.bclevelfile.EstimatedGameTime())

    def DayTime(self):
        return(self.bclevelfile.DayTime())

    def EstimatedDayTime(self):
        return(self.bclevelfile.EstimatedDayTime())

    def ClearWeatherTime(self):
        return(self.bclevelfile.ClearWeatherTime())

    def EstimatedClearWeatherTime(self):
        return(self.bclevelfile.EstimatedClearWeatherTime())

    def Raining(self):
        return(self.bclevelfile.Raining())

    def RainTime(self):
        return(self.bclevelfile.RainTime())

    def EstimatedRainTime(self):
        return(self.bclevelfile.EstimatedRainTime())

    def Thundering(self):
        return(self.bclevelfile.Thundering())

    def ThunderTime(self):
        return(self.bclevelfile.ThunderTime())

    def EstimatedThunderTime(self):
        return(self.bclevelfile.EstimatedThunderTime())

    def WanderingTraderSpawnDelay(self):
        return(self.bclevelfile.WanderingTraderSpawnDelay())

    def EstimatedWanderingTraderSpawnDelay(self):
        return(self.bclevelfile.EstimatedWanderingTraderSpawnDelay())

    def WanderingTraderSpawnChance(self):
        return(self.bclevelfile.WanderingTraderSpawnChance())

    def WanderingTraderID(self):
        return(self.bclevelfile.WanderingTraderID())

    def EstimatedTimeOfDay(self):
        return(self.bclevelfile.EstimatedTimeOfDay())

    def UpdateGameInfo(self):
        self.bclevelfile.UpdateLevelInfo()
        self.bclogfiles.UpdateLogInfo()

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
     
        print(f"\n\n")
        print(f"Log File:            {self.LogFilename()}")



def main():

    print("BCGameInstance: Unit Testing")
    bcgame = BCGameInstance()

    bcgame.UpdateGameInfo()
    bcgame.PrintDebug()

#    if bclevelfile.lastupdatetime == 0:
#        print("No level.dat file")
#    else:
#        print("Seed:                {}".format(bclevelfile.seed))
##        print(bclevelfile.pretty_tree())
#

if __name__ == '__main__':
    main()