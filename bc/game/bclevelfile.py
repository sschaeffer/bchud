#!/usr/bin/env python3
import sys
sys.path.append("/home/integ/Code/bchud")

from bc.common.constants import Constants
from nbt import NBTFile

from time import time
from pathlib import Path
from datetime import datetime

class BCLevelFile(NBTFile):

    def __init__(self, minecraftdir="/home/integ/.minecraft", worldname="New World"):

        self._minecraftdir=minecraftdir
        self._worldname=worldname
        self._level_filename="level.dat"

        self._last_update_time=0
        self._seed=None
        self._game_time=0
        self._day_time=0
        self._clear_weather_time=0
        self._raining=False
        self._rain_time=0
        self._thundering=False
        self._thunder_time=0
        self._wandering_trader_id="<empty>"
        self._wandering_trader_spawn_chance=0
        self._wandering_trader_spawn_delay=0

    def reset_level_info(self, minecraftdir, worldname):
        self.__init__(minecraftdir,worldname)

    def update_level_info(self):

        level_file_path = Path(self.level_filename())

        if not level_file_path.exists():
            # game was reset or hasn't started yet. level_dat doesn't exist
            # also re-read the logs from scratch
            self.reset_level_info(self._minecraftdir, self._worldname)

        elif self._last_update_time != level_file_path.stat().st_mtime:
            # file has changed so lets read it

            self._last_update_time = level_file_path.stat().st_mtime
            super(BCLevelFile, self).__init__(level_file_path)

            if "seed" in self["Data"]["WorldGenSettings"]:
                self._seed=str(self["Data"]["WorldGenSettings"]["seed"])

            if "Time" in self["Data"]:
                self._game_time=int(str(self["Data"]["Time"]))

            if "DayTime" in self["Data"]:
                self._day_time=int(str(self["Data"]["DayTime"]))

            if "ClearWeatherTime" in self["Data"]:
                self._clear_weather_time=int(str(self["Data"]["ClearWeatherTime"]))

            if "rainTime" in self["Data"]:
                self._rain_time=int(str(self["Data"]["rainTime"]))

            if "thunderTime" in self["Data"]:
                self._thunder_time=int(str(self["Data"]["thunderTime"]))

            if "WanderingTraderSpawnDelay" in self["Data"]:
                self._wandering_trader_spawn_delay=int(str(self["Data"]["WanderingTraderSpawnDelay"]))

            if "WanderingTraderSpawnChance" in self["Data"]:
                self._wandering_trader_spawn_chance=int(str(self["Data"]["WanderingTraderSpawnChance"]))

            if "WanderingTraderId" in self["Data"]:
                self._wandering_trader_id=str(self["Data"]["WanderingTraderId"])
            else:
                self._wandering_trader_id="<empty>"

            if "raining" in self["Data"]:
                self._raining=bool(int(str(self["Data"]["raining"])))

            if "thundering" in self["Data"]:
                self._thundering=bool(int(str(self["Data"]["thundering"])))

    def level_filename(self):
        return(self._minecraftdir+"/saves/"+self._worldname+"/"+self._level_filename)

    def level_file_last_update(self):
        return(self._last_update_time)

    def seed(self):
        return(self._seed)

    def game_time(self):
        return(self._game_time)

    def day_time(self):
        return(self._day_time)

    def clear_weather_time(self):
        return(self._clear_weather_time)

    def raining(self):
        return(self._raining)

    def rain_time(self):
        return(self._rain_time)

    def thundering(self):
        return(self._thundering)

    def thunder_time(self):
        return(self._thunder_time)

    def wandering_trader_spawn_delay(self):
        return(self._wandering_trader_spawn_delay)

    def wandering_trader_spawn_chance(self):
        return(self._wandering_trader_spawn_chance)

    def wandering_trader_id(self):
        return(self._wandering_trader_id)

    """
    These are all the estimation functions
    """

    def estimated_game_time(self):
        result = 0
        if self._game_time > 0:
            result = round(self._game_time+((time()-self._last_update_time)*20))
        return result


    def estimated_day_time(self):
        result = 0
        if self._day_time > 0:
            result = round(self._day_time+((time()-self._last_update_time)*20))
        return result

    def estimated_clear_weather_time(self):
        result=0
        if self._clear_weather_time > 0:
            result = round(self._clear_weather_time-((time()-self._last_update_time)*20))
        return result

    def estimated_rain_time(self):
        result = 0
        if self._rain_time != 0:
            result = round(self._rain_time-((time()-self._last_update_time)*20))
        return result

    def estimated_thunder_time(self):
        result = 0
        if self._thunder_time != 0:
            result = round(self._thunder_time-((time()-self._last_update_time)*20))
        return result

    def estimated_wandering_trader_spawn_delay(self):
        result = 0
        if self._wandering_trader_spawn_delay != 0:
            result = round(self._wandering_trader_spawn_delay-((time()-self._last_update_time)*20))
        return result

    def estimated_is_raining(self):
        result = False 
        if self.raining() and self.estimated_rain_time() > 0:
            result = True
        elif not self.raining() and self.estimated_rain_time() < 0:
            result = True
        return(result)

    def estimated_is_thundering(self):
        result = False 
        if self.estimated_is_raining() and self.thundering() and self.estimated_thunder_time() > 0:
            result = True
        elif self.estimated_is_raining() and not self.thundering() and self.estimated_thunder_time() < 0:
            result = True
        return(result)

    def estimated_is_monsters(self):
        estdaytime = self.estimated_day_time()%Constants.DAY_FULLDAY
        result = False
        if estdaytime >= Constants.DAY_MONSTERS and estdaytime <= Constants.DAY_NO_MONSTERS:
            result = True 
        return result 

    def estimated_is_bed_usable(self):
        estdaytime = self.estimated_day_time()%Constants.DAY_FULLDAY
        result = False
        if estdaytime >= Constants.DAY_SLEEP and estdaytime <= Constants.DAY_NO_SLEEP:
            result = True 
        return result

    def estimated_time_of_day(self):
        estdaytime = self.estimated_day_time()%Constants.DAY_FULLDAY
        if estdaytime > Constants.DAY_NO_SLEEP:
            result = Constants.COLOR_NO_SLEEP
        elif estdaytime > Constants.DAY_NO_MONSTERS:
            result = Constants.COLOR_NO_MONSTERS     # LIGHT BLUE (11 secs)
        elif estdaytime > Constants.DAY_MONSTERS:
            result = Constants.COLOR_MONSTERS       # DARKEST BLUE/BLACK (8mins 1secs)
        elif estdaytime > Constants.DAY_SLEEP:
            result = Constants.COLOR_SLEEP          # DARK BLUE PURPLE (21secs)
        elif estdaytime > Constants.DAY_TWILIGHT:
            result = Constants.COLOR_TWILIGHT       # PURPLE (27secs)
        elif estdaytime > Constants.DAY_HAPPYHOUR:
            result = Constants.COLOR_HAPPYHOUR      # LIGHT BLUE/PURPLE (2mins 30secs) elif estdaytime > Constants.DAY_WORKDAY:
            result = Constants.COLOR_WORKDAY        # YELLOW (5mins 50secs)
        else:
            result = Constants.COLOR_DAWN           # BRIGHT YELLOW (1min 40secs)
        return(result)

#        elif estdaytime > self.DAY_NORAINMONSTERS:
#            result = self.NORAINMONSTERS # LIGHTER BLUE/PINK (22secs)
#        elif estdaytime > self.DAY_RAINMONSTERS:
#            result = self.RAINMONSTERS   # DARK BLUE (11secs)

def main(minecraftdir,worldname):

    print("BCLevelFile: Unit Testing")
    print()
    bclevelfile = BCLevelFile(minecraftdir,worldname)

    bclevelfile.update_level_info()
    if bclevelfile.level_file_last_update() == 0:
        print(f"Level Filename:      {bclevelfile.level_filename()}")
        print("No level.dat file")
#        print(bclevelfile.pretty_tree())
    else:
        print(f"Level Filename:      {bclevelfile.level_filename()}")
        print(f"Last Update Time:    {datetime.fromtimestamp(bclevelfile.level_file_last_update())} (Current Time: {datetime.now()}")
        print()
        print(f"Seed:                {bclevelfile.seed()}")
        print(f"Game Time:           {bclevelfile.game_time()}")
        print(f"Day Time:            {bclevelfile.day_time()}")
        print(f"Raining:             {bclevelfile.raining()}")
        print(f"Rain Time:           {bclevelfile.rain_time()}")
        print(f"Thundering:          {bclevelfile.thundering()}")
        print(f"Thunder Time:        {bclevelfile.thunder_time()}")
        print(f"Clear Weather Time:  {bclevelfile.clear_weather_time()}")
        print(f"Wandering Trader Sp: {bclevelfile.wandering_trader_spawn_delay()}")
        print(f"Wandering Trader Sp: {bclevelfile.wandering_trader_spawn_chance()}")
        print(f"Wandering Trader Id: {bclevelfile.wandering_trader_id()}")
        print()
        print(f"Estimated Game Time: {bclevelfile.estimated_game_time()}")
        print(f"Estimated Day Time:  {bclevelfile.estimated_day_time()}")
        print(f"Estimated Is Rainin: {bclevelfile.estimated_is_raining()}")
        print(f"Estimated Rain Time: {bclevelfile.estimated_rain_time()}")
        print(f"Estimated Is Thunde: {bclevelfile.estimated_is_thundering()}")
        print(f"Estimated Thunder T: {bclevelfile.estimated_thunder_time()}")
        print(f"Estimated Clear Wea: {bclevelfile.estimated_clear_weather_time()}")
        print(f"Estimated Wandering: {bclevelfile.estimated_wandering_trader_spawn_delay()}")
        print(f"Estimated Is Bed Us: {bclevelfile.estimated_is_bed_usable()}")
        print(f"Estimated Is Monste: {bclevelfile.estimated_is_monsters()}")
        estdaytime = bclevelfile.estimated_day_time()%Constants.DAY_FULLDAY
        if estdaytime > Constants.DAY_NO_SLEEP:
            estdaytimestring = "COLOR_NO_SLEEP"
        elif estdaytime > Constants.DAY_NO_MONSTERS:
            estdaytimestring = "COLOR_NO_MONSTERS"
        elif estdaytime > Constants.DAY_MONSTERS:
            estdaytimestring = "COLOR_MONSTERS"
        elif estdaytime > Constants.DAY_SLEEP:
            estdaytimestring = "COLOR_SLEEP"
        elif estdaytime > Constants.DAY_TWILIGHT:
            estdaytimestring = "COLOR_TWILIGHT"
        elif estdaytime > Constants.DAY_HAPPYHOUR:
            estdaytimestring = "COLOR_HAPPYHOUR"
        elif estdaytime > Constants.DAY_WORKDAY:
            estdaytimestring = "COLOR_WORKDAY"
        else:
            estdaytimestring = "COLOR_DAWN"
        print(f"Estimated Time of D: {bclevelfile.estimated_time_of_day()}={estdaytimestring}")


if __name__ == '__main__':
    (minecraftdir,worldname,singleplayer) = Constants.init_server("/home/integ/Code/bchud/config.json")
    main(minecraftdir,worldname)
    