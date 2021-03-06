#!/usr/bin/python3
import curses
from argparse import ArgumentParser
from pathlib import Path
import io
import json
import os

class Constants():

    MINIMUM_HEIGHT=20
    MINIMUM_WIDTH=40

    BCMENU_EXIT=-1
    BCMENU_NOCHANGE=0
    BCMENU_REFRESH=1

    BCMENU_AUTO_UPDATE=11
    BCMENU_AUTO_BACKUP=12
    BCMENU_DAY_NIGHT_CYCLE=13
    BCMENU_LEVEL_INFO=14
    BCMENU_BCLOGS=15
    BCMENU_LATEST_LOG=16
    BCMENU_TIMING_WINDOW=17
    BCMENU_CHANGE_SERVER_WORLD=18
    BCMENU_SAVE_LEVEL_FILE=19
    BCMENU_UPDATE=20
    BCMENU_RECORD_TIME=21

    BCMENU_CURRENTUSER=50
    BCMENU_USER1=51
    BCMENU_USER2=52
    BCMENU_USER3=53
    BCMENU_USER4=54
    BCMENU_USER5=55
    BCMENU_USER6=56
    BCMENU_USER7=57

    BCMENU_ALL_ADVANCEMENTS=100
    BCMENU_BACAP_ADVANCEMENTS=101
    BCMENU_MINING_ADVANCEMENTS=102
    BCMENU_BUILDING_ADVANCEMENTS=103
    BCMENU_FARMING_ADVANCEMENTS=104
    BCMENU_ANIMAL_ADVANCEMENTS=105
    BCMENU_MONSTERS_ADVANCEMENTS=106
    BCMENU_WEAPONRY_ADVANCEMENTS=107
    BCMENU_ADVENTURE_ADVANCEMENTS=108
    BCMENU_REDSTONE_ADVANCEMENTS=109
    BCMENU_ENCHANTING_ADVANCEMENTS=110
    BCMENU_STATISTICS_ADVANCEMENTS=111
    BCMENU_NETHER_ADVANCEMENTS=112
    BCMENU_POTIONS_ADVANCEMENTS=113
    BCMENU_END_ADVANCEMENTS=114
    BCMENU_SUPER_CHALLENGES=115

    COLOR_BCMENU_MENU=1
    COLOR_BCMENU_SELECTED_MENU=2
    COLOR_ADVANCEMENT_COMPLETE=3
    COLOR_STATUS_BAR=4
    COLOR_STATUS_BAR_GAME_TIME=5
    COLOR_STATUS_BAR_UNTIL_RAIN=6
    COLOR_STATUS_BAR_UNTIL_THUNDER=7

    COLOR_DAWN=101           # 1min 40secs
    COLOR_WORKDAY=102        # 5mins 50secs
    COLOR_HAPPYHOUR=103      # 2mins 30secs
    COLOR_TWILIGHT=104       # 27secs
    COLOR_SLEEP=105          # 21secs
    COLOR_MONSTERS=106       # 8mins 1secs
    COLOR_NO_MONSTERS=107    # 11 secs
    COLOR_NO_SLEEP=108       # 27secs

    DAY_DAWN=0               #     0 DAWN Wakeup and Wander (0:00)
    DAY_WORKDAY=2000         #  2000 WORKDAY (1:40)
    DAY_HAPPYHOUR=9000       #  9000 HAPPY-HOUR (7:30)
    DAY_TWILIGHT=12000       # 12000 TWILIGHT/villagers sleep (10:00)
    RAIN_SLEEP=12010         # 12010 SLEEP on rainy days (10:00)
    DAY_SLEEP=12542          # 12542 SLEEP on normal days/mobs don't burn (10:27.1/0)
    RAIN_MONSTERS=12969      # 12969 Rainy day monsters (10:48.45/21)
    DAY_MONSTERS=13188       # 13188 Monsters (10:59.4/32)
    DAY_NO_MONSTERS=22812     # 22812 No more monsters (19:00.6/8:33)
    RAIN_NO_MONSTERS=23031    # 23031 No more rainy day monsters(19:11.55/8:44)
    DAY_NO_SLEEP=23460        # 23460 No sleeping on normal days (19:33/9:06)
    RAIN_NO_SLEEP=23992       # 23992 No sleeping rainy days (19:59/9:33)
    DAY_FULLDAY=24000        # 24000 Full-day 


    def curses_setup(stdscr):

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.halfdelay(10)

        # Start colors in curses
        if curses.has_colors():
            curses.start_color()

        curses.init_pair(Constants.COLOR_BCMENU_MENU, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(Constants.COLOR_BCMENU_SELECTED_MENU, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Constants.COLOR_ADVANCEMENT_COMPLETE, 46, 0) #GREEN text and default bkgd
        curses.init_pair(Constants.COLOR_STATUS_BAR, curses.COLOR_WHITE, 240) #BLACK text and GREY bkgd 
        curses.init_pair(Constants.COLOR_STATUS_BAR_GAME_TIME, curses.COLOR_BLACK, 34) #BLACK text and BRIGHT GREEN bkgd 
        curses.init_pair(Constants.COLOR_STATUS_BAR_UNTIL_RAIN, curses.COLOR_BLACK, 26) #BLACK text and  
        curses.init_pair(Constants.COLOR_STATUS_BAR_UNTIL_THUNDER, curses.COLOR_CYAN, 237) #BLACK text and  

        curses.init_pair(Constants.COLOR_DAWN, curses.COLOR_BLACK, 216)         # BLACK text and BRIGHT YELLOW bkgd (1min 40secs)
        curses.init_pair(Constants.COLOR_WORKDAY, curses.COLOR_BLACK, 192)      # BLACK text and YELLOW bkgd (5mins 50secs)
        curses.init_pair(Constants.COLOR_HAPPYHOUR, curses.COLOR_BLACK, 181)    # BLACK text and LIGHT BLUE/PURPLE bkgd (2mins 30secs)
        curses.init_pair(Constants.COLOR_TWILIGHT, curses.COLOR_BLACK, 147)     # BLACK text and PURPLE bkgd (27secs)
        curses.init_pair(Constants.COLOR_SLEEP, curses.COLOR_WHITE, 63)         # WHITE text and DARK BLUE PURPLE bkgd (21secs)
        curses.init_pair(Constants.COLOR_MONSTERS, curses.COLOR_WHITE, 17)      # WHITE text and DARKEST BLUE/BLACK bkgd (8mins 1secs)
        curses.init_pair(Constants.COLOR_NO_MONSTERS, curses.COLOR_WHITE, 20)   # WHITE text and LIGHT BLUE bkgd (11 secs)
        curses.init_pair(Constants.COLOR_NO_SLEEP, curses.COLOR_WHITE, 96)      # WHITE text and PINK bkgd (27secs)

    def init_server(config_file, argv=None):

        minecraftdir = f"{Path.home()}/.minecraft"
        worldname = "New World"
        singleplayer=True
        data = None

        if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
            with open(config_file, "r") as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()

        if(data):
            if "minecraftdir" in data: minecraftdir = data["minecraftdir"]
            if "worldname" in data: worldname = data["worldname"]
            if "singleplayer" in data: singleplayer = data["singleplayer"]

        parser = ArgumentParser(prog='bchud')
        parser.add_argument('--minecraftdir', help="minecraft server directory")
        parser.add_argument('--worldname', help="worldname is the name of the world")
        parser.add_argument('--singleplayer',  help="single player world", action="store_true" )
        args = parser.parse_args(argv)

        if(args.singleplayer):
            singleplayer = True
            minecraftdir = f"{Path.home()}/.minecraft"
        if(args.minecraftdir != None):
            minecraftdir = args.minecraftdir
        if(args.worldname != None):
            worldname = args.worldname

        return(minecraftdir,worldname,singleplayer)

    def write_config_file(config_file, minecraftdir,worldname,singleplayer):

        if os.path.isfile(config_file) and not os.access(config_file, os.W_OK):
            print("config.json exists but can't be written to")
        else:
            with open(config_file,"w") as jsonfile:
                output ={
                    "minecraftdir": minecraftdir,
                    "worldname": worldname,
                    "singleplayer": singleplayer
                }
                json.dump(output,jsonfile,indent=4)
                jsonfile.close()


    def check_minimum_size(stdscr:curses.window):
        (height,width) = stdscr.getmaxyx()
        if(height<Constants.MINIMUM_HEIGHT or width<Constants.MINIMUM_WIDTH):
            stdscr.clear()
            stdscr.addstr(int(height/2),int((width/2)-5),
                          f"Resize{Constants.MINIMUM_HEIGHT}x{Constants.MINIMUM_WIDTH}")
            stdscr.noutrefresh()
        return(height,width)

def main(minecraftdir, worldname, singleplayer):

    print()
    print( "BC Constants:         Unit Testing")
    print()
    print(f"Minecraft Dir: {minecraftdir}")
    print(f"World Name: {worldname}")
    print(f"Single Player: {singleplayer}")
#    Constants.write_config_file("/home/integ/Code/bchud/config.json","testminecraft","testworld", False)

if __name__ == "__main__":
    (minecraftdir, worldname, singleplayer) = Constants.init_server("/home/integ/Code/bchud/config.json")
    main(minecraftdir, worldname, singleplayer)