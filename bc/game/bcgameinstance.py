#!/usr/bin/env python3
import sys
sys.path.append("/home/integ/Code/bchud")

from bc.common.constants import Constants
#from enum import auto
#from io import UnsupportedOperation
import subprocess

from bc.game.bclevelfile import BCLevelFile
from bc.game.bcalladvancements import BCAllAdvancements
from bc.game.gamequery import GameQuery
#from bc.game.bclogfiles import BCLogFiles
#from bc.game.bclog import BCLog

from time import sleep, time
from subprocess import run 

class BCGameInstance():

    def __init__(self, minecraftdir, worldname, singleplayer):
        """
        Parameters
        ----------
        minecraftdir : str
            The path to the minecraft directory
        servername : str
            The name of the current minecraft server
        worldname : str
            The name of the current minecraft world
        log_results : boolean, optional
            Write out a log into BClogs or not
        update_time : float, optional
            How many seconds to wait before updating
        """
        self._minecraftdir=minecraftdir
        self._worldname=worldname
        self._singleplayer=singleplayer

        self._log_results=False

        self._auto_update=True
        self._auto_update_delay=1.0
        self._last_auto_update=0.0

        self._auto_backup=False
        self._auto_backup_delay=60.0
        self._last_auto_backup=0.0

        self._bclevelfile = BCLevelFile(minecraftdir, worldname)
        self._bcalladvancements = BCAllAdvancements(minecraftdir, worldname)
#        self._bclogfiles = BCLogFiles(minecraftdir, servername)
#        self._bclog = BCLog(minecraftdir,servername)





    def update_game_info(self):
        """Update Game Info - this function will check to see how much time has past and will update the following classes
            - BCLevelFile - the main level.dat for the minecraft server
            - BCAllAdvancements - the datapack advancements directory (bac_advancements) and then each users json file
            - BCLogFiles - all the log files in the log directory
        """
        if self._auto_update:
            if time() > self._last_auto_update + self._auto_update_delay:
                self._bclevelfile.update_level_info()
                self._bcalladvancements.update_advancements(self._bcalladvancements.PRIMARY)

#                self._bclogfiles.update_log_info()
#                if(self._log_results):
#                    self._bclog.log_results(self._bclevelfile,self._bclogfiles)
                self._last_auto_update = time()

        if self._auto_backup:
            if time() > self._last_auto_backup + self._auto_backup_delay:
                self.backup_server()
                self._last_auto_backup = time()

    def set_auto_update(self, auto_update):
        self._auto_update = auto_update
        self._last_auto_update = time()

    def set_auto_update_delay(self, auto_update_delay):
        """Set Update Time
        Change the update time from the default to whatever is reasonable
            4.0 = 4 seconds
            0.5 = 1/2 second
        """
        self._auto_update_delay = auto_update_delay

    def set_auto_backup(self, auto_backup):
        self._auto_backup = auto_backup
        self._last_auto_backup = time()
    
    def set_auto_backup_delay(self, auto_backup_delay):
        self._auto_backup_delay = auto_backup_delay


    """
    The rest of all these functions are getter routines for the Game Instance - None of these routines should cost any cycles
    """

#    def log_filename(self):
#        return(self._bclogfiles.log_filename())
#
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

    def all_advancements_count(self):
        return(self._bcalladvancements.get_milestone("blazeandcave:bacap/advancement_legend"))

    def get_advancement(self,name):
        return(self._bcalladvancements.get_advancement(name))

    """
    These functions return the list of advancements per section
    """

    def bacap_advancements_list(self):
        return(self._bcalladvancements.BACAP_LIST)

    def mining_advancements_list(self):
        return(self._bcalladvancements.MINING_LIST)

    def building_advancements_list(self):
        return(self._bcalladvancements.BUILDING_LIST)

    def farming_advancements_list(self):
        return(self._bcalladvancements.FARMING_LIST)

    def animal_advancements_list(self):
        return(self._bcalladvancements.ANIMAL_LIST)

    def monsters_advancements_list(self):
        return(self._bcalladvancements.MONSTERS_LIST)

    def weaponry_advancements_list(self):
        return(self._bcalladvancements.WEAPONRY_LIST)

    def adventure_advancements_list(self):
        return(self._bcalladvancements.ADVENTURE_LIST)

    def redstone_advancements_list(self):
        return(self._bcalladvancements.REDSTONE_LIST)

    def enchanting_advancements_list(self):
        return(self._bcalladvancements.ENCHANTING_LIST)

    def statistics_advancements_list(self):
        return(self._bcalladvancements.STATISTICS_LIST)

    def nether_advancements_list(self):
        return(self._bcalladvancements.NETHER_LIST)

    def potions_advancements_list(self):
        return(self._bcalladvancements.POTION_LIST)

    def end_advancements_list(self):
        return(self._bcalladvancements.END_LIST)

    def super_challenges_list(self):
        return(self._bcalladvancements.CHALLENGES_LIST)

    """
    These functions are quick bash scripts for interacting with the servers (through screen) 
    """

    def save_all(self):
        command_line = f"./scripts/save-all.bash {self._worldname}"
        run([command_line])
        sleep(0.5)

    def query_time(self):
        command_line = f"./scripts/query-time.bash {self._worldname}"
        run([command_line])
        sleep(0.5)

    def backup_server(self):
        command_line = ["./scripts/backup-server.bash",f"{self._minecraftdir}",f"{self._worldname}"]
        run(command_line,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
        sleep(0.5)


    def print_debug(self):
        print(f"Level File:          {self.level_filename()}")
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
        print()
#        self._bcalladvancements.print_all_advancements()

def main(minecraft, worldname, singleplayer):

    print("BCGameInstance: Unit Testing")
    bcgame = BCGameInstance(minecraft, worldname, singleplayer)
    bcgame.

    bcgame.update_game_info()
    bcgame.print_debug()

if __name__ == '__main__':
    (minecraftdir, worldname, singleplayer) = Constants.init_server("/home/integ/Code/bchud/config.json")
    main(minecraftdir, worldname, singleplayer)