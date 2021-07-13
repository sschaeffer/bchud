#!/usr/bin/env python3

from bclevelfile import BCLevelFile
from bclogfiles import BCLogFiles
from bclog import BCLog
from bcalladvancements import BCAllAdvancements

from time import sleep, time
from subprocess import call

class BCGameInstance():

#    DAWN=BCLevelFile.DAWN           # LIGHT ORANGE (1min 40secs)
#    WORKDAY=BCLevelFile.WORKDAY        # LIGHT YELLOW (5mins 50secs)
#    HAPPYHOUR=BCLevelFile.HAPPYHOUR      # LIGHT MAROON (2mins 30secs)
#    TWILIGHT=BCLevelFile.TWILIGHT       # LIGHT PURPLE (27secs)
#    SLEEP=BCLevelFile.SLEEP          # DARK BLUE (21secs)
#    MONSTERS=BCLevelFile.MONSTERS       # DARKEST BLUE/BLACK (8mins 1secs)
#    NOMONSTERS=BCLevelFile.NOMONSTERS     # BLUE (11 secs)
#    NOSLEEP=BCLevelFile.NOSLEEP        # MAUVE (27secs)
#
#    DAY_DAWN=BCLevelFile.DAY_DAWN               #     0 DAWN Wakeup and Wander (0:00)
#    DAY_WORKDAY=BCLevelFile.DAY_WORKDAY        #  2000 WORKDAY (1:40)
#    DAY_HAPPYHOUR=BCLevelFile.DAY_HAPPYHOUR      #  9000 HAPPY-HOUR (7:30)
#    DAY_TWILIGHT=BCLevelFile.DAY_TWILIGHT     # 12000 TWILIGHT/villagers sleep (10:00)
#    RAIN_SLEEP=BCLevelFile.RAIN_SLEEP         # 12010 SLEEP on rainy days (10:00)
#    DAY_SLEEP=BCLevelFile.DAY_SLEEP       # 12542 SLEEP on normal days/mobs don't burn (10:27.1/0)
#    RAIN_MONSTERS=BCLevelFile.RAIN_MONSTERS      # 12969 Rainy day monsters (10:48.45/21)
#    DAY_MONSTERS=BCLevelFile.DAY_MONSTERS       # 13188 Monsters (10:59.4/32)
#    DAY_NOMONSTERS=BCLevelFile.DAY_NOMONSTERS     # 22812 No more monsters (19:00.6/8:33)
#    RAIN_NOMONSTERS=BCLevelFile.RAIN_NOMONSTERS    # 23031 No more rainy day monsters(19:11.55/8:44)
#    DAY_NOSLEEP=BCLevelFile.DAY_NOSLEEP        # 23460 No sleeping on normal days (19:33/9:06)
#    RAIN_NOSLEEP=BCLevelFile.RAIN_NOSLEEP        # 23992 No sleeping rainy days (19:59/9:33)
#    DAY_FULLDAY=BCLevelFile.DAY_FULLDAY        # 24000 Full-day
#
    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="fury", worldname="fury", logresults=True):

        self._logresults=logresults
        self._minecraftdir=minecraftdir
        self._servername=servername
        self._worldname=worldname

        self._bclevelfile = BCLevelFile(minecraftdir, servername, worldname)
        self._bclogfiles = BCLogFiles(minecraftdir, servername)
        self._bcalladvancements = BCAllAdvancements(minecraftdir, servername, worldname)

        self._bclog = BCLog(minecraftdir,servername)

    def log_filename(self):
        return(self._bclogfiles.log_filename())

    def level_filename(self):
        return(self._bclevelfile.level_filename())

    def advancement_dir(self):
        return(self._bcalladvancements.advancement_dir())

    def level_file_last_update(self):
        return(self._bclevelfile.level_file_last_update())

    def seed(self):
        return(self._bclevelfile.seed())

    def game_time(self):
        return(self._bclevelfile.game_time())

    def estimated_game_time(self):
        return(self._bclevelfile.estimated_game_time())

    def day_time(self):
        return(self._bclevelfile.day_time())

    def estimated_day_time(self):
        return(self._bclevelfile.estimated_day_time())

    def clear_weather_time(self):
        return(self._bclevelfile.clear_weather_time())

    def estimated_clear_weather_time(self):
        return(self._bclevelfile.estimated_clear_weather_time())

    def raining(self):
        return(self._bclevelfile.raining())

    def rain_time(self):
        return(self._bclevelfile.rain_time())

    def estimated_rain_time(self):
        return(self._bclevelfile.estimated_rain_time())

    def estimated_is_raining(self):
        return(self._bclevelfile.estimated_is_raining())

    def thundering(self):
        return(self._bclevelfile.thundering())

    def thunder_time(self):
        return(self._bclevelfile.thunder_time())

    def estimated_thunder_time(self):
        return(self._bclevelfile.estimated_thunder_time())

    def estimated_is_thundering(self):
        return(self._bclevelfile.estimated_is_thundering())

    def wandering_trader_spawn_delay(self):
        return(self._bclevelfile.wandering_trader_spawn_delay())

    def estimated_wandering_trader_spawn_delay(self):
        return(self._bclevelfile.estimated_wandering_trader_spawn_delay())

    def wandering_trader_spawn_chance(self):
        return(self._bclevelfile.wandering_trader_spawn_chance())

    def wandering_trader_id(self):
        return(self._bclevelfile.wandering_trader_id())

    def estimated_time_of_day(self):
        return(self._bclevelfile.estimated_time_of_day())

    def estimated_is_monsters(self):
        return(self._bclevelfile.estimated_is_monsters())

    def estimated_is_bed_usable(self):
        return(self._bclevelfile.estimated_is_bed_usable())

    def server_active(self):
        return(self._bclogfiles.server_active())

    def server_start_time(self):
        return(self._bclogfiles.server_start_time())

    def all_advancements_count(self):
        return(self._bcalladvancements.get_milestone("blazeandcave:bacap/advancement_legend"))

    def get_advancement(self,name):
        return(self._bcalladvancements.get_advancement(name))

    def bacap_advancements_list(self):
        return(self._bcalladvancements.BACAP_LIST)

    def mining_advancements_list(self):
        return(self._bcalladvancements.MINING_LIST)

    def building_advancements_list(self):
        return(self._bcalladvancements.BUILDING_LIST)

    def update_game_info(self):

        self._bclogfiles.update_log_info()
        self._bclevelfile.update_level_info(self.server_active(),self.server_start_time())
        self._bcalladvancements.update_advancements(self._bcalladvancements.PRIMARY)

        if(self._logresults):
            self._bclog.log_results(self._bclevelfile,self._bclogfiles)

    def save_all_files(self):
        call(["./save-it-all.bash"])
        sleep(0.5)

    def query_time(self):
        call(["./query-time.bash"])
        sleep(0.5)

    def print_debug(self):
        print(f"Level File:          {self.level_filename()}")
        print(f"Log File:            {self.log_filename()}")
        print(f"Advancement Dir:     {self.advancement_dir()}")
        print(f"Last Update Time:    {self.level_file_last_update()}")
        print(f"Seed:                {self.seed()}")
        print(f"Game Time:           {self.game_time()}")
        print(f"Estimated Game Time: {self.estimated_game_time()}")
        print(f"Day Time:            {self.day_time()}")
        print(f"Estimated Day Time:  {self.estimated_day_time()}")
        print(f"Clear Weather Time:  {self.clear_weather_time()}")
        print(f"Estimated Clear Wea: {self.estimated_clear_weather_time()}")
        print(f"Raining:             {self.raining()}")
        print(f"Rain Time:           {self.rain_time()}")
        print(f"Estimated Rain Time: {self.estimated_rain_time()}")
        print(f"Thundering:          {self.thundering()}")
        print(f"Thunder Time:        {self.thunder_time()}")
        print(f"Estimated Thunder T: {self.estimated_thunder_time()}")
        print(f"Wandering Trader Sp: {self.wandering_trader_spawn_delay()}")
        print(f"Estimated Wandering: {self.estimated_wandering_trader_spawn_delay()}")
        print(f"Wandering Trader Sp: {self.wandering_trader_spawn_chance()}")
        print(f"Wandering Trader Id: {self.wandering_trader_id()}")
        print(f"Estimated Time of D: {self.estimated_time_of_day()}")
        self._bcalladvancements.print_all_advancements()

def main():

    print("BCGameInstance: Unit Testing")
    bcgame = BCGameInstance()

    bcgame.update_game_info()
    bcgame.print_debug()

#    while True:
#        sleep(2)
#        print()
#        bcgame.update_game_info()
#        bcgame.print_debug()



if __name__ == '__main__':
    main()