#!/usr/bin/python3
import curses
from argparse import ArgumentParser

class BCHudConstants():

    FOCUS_QUIT=-1
    FOCUS_STARTSCREEN=0
    FOCUS_BCHUD_MENU=1

    MENUBAR_COLOR=1
    MENUBAR_SELECTED_COLOR=2

    DAWN=1           # LIGHT ORANGE (1min 40secs)
    WORKDAY=2        # LIGHT YELLOW (5mins 50secs)
    HAPPYHOUR=3      # LIGHT MAROON (2mins 30secs)
    TWILIGHT=4       # LIGHT PURPLE (27secs)
    SLEEP=5          # DARK BLUE (21secs)
    MONSTERS=6       # DARKEST BLUE/BLACK (8mins 1secs)
    NOMONSTERS=7     # BLUE (11 secs)
    NOSLEEP=8        # MAUVE (27secs)

    STATSBAR_COLOR=21
    STATSBAR_REALTIMECOLOR=22
    STATSBAR_UNTILRAINCOLOR=23
    STATSBAR_UNTILTHUNDERCOLOR=24

    ADVANCEMENT_COMPLETE =30
    ADVANCEMENT_INCOMPLETE =31
    CRITERIA_COMPLETE =32
    CRITERIA_INCOMPLETE =33

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
    RAIN_NOSLEEP=23992       # 23992 No sleeping rainy days (19:59/9:33)
    DAY_FULLDAY=24000        # 24000 Full-day 


    def cursessetup(stdscr):

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.halfdelay(10)

        # Start colors in curses
        if curses.has_colors():
            curses.start_color()

#        curses.init_pair(BCHudConstants.MENUBAR_COLOR, 0, curses.COLOR_BLACK)
        curses.init_pair(BCHudConstants.MENUBAR_SELECTED_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def initserver(argv=None):

        parser = ArgumentParser(prog='bchud')
        parser.add_argument('--minecraftdir', default="/media/local/Minecraft/server", help="minecraft server directory")
        parser.add_argument('--servername', default="fury", help="servername is the name of the server")
        parser.add_argument('--worldname', help="worldname is the name of the world (if different then server)")
        args = parser.parse_args(argv)
        if(args.worldname == None):
            args.worldname = args.servername
        return(args.minecraftdir,args.servername,args.worldname)

def main():

    print( "BCHudConstants:             Unit Testing")
    print(f"BCHudConstants.MODE_QUIT: {BCHudConstants.FOCUS_QUIT:3}")
    print(f"BCHudConstants.DAWN:      {BCHudConstants.DAWN:3}")
    print(f"BCHudConstants.WORKDAY:   {BCHudConstants.WORKDAY:3}")

if __name__ == "__main__":
    main()