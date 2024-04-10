#!/usr/bin/python3
<<<<<<< HEAD

from bcgameinstance import BCGameInstance
from bcstatwindow import BCStatWindow
from bcstatusbar import BCStatusBar
from datetime import datetime, timedelta
#from math import floor
#from time import time, sleep, strftime, strptime
import curses
import curses.panel

from sys import argv
import argparse


def initserver(argv=None):

    parser = argparse.ArgumentParser(prog='bchud')
    parser.add_argument('--minecraftdir', default="/media/local/Minecraft/server", help="minecraft server directory")
    parser.add_argument('--servername', default="snapshot", help="servername is the name of the server")
    parser.add_argument('--worldname', help="worldname is the name of the world (if different then server)")
    args = parser.parse_args(argv)
    if(args.worldname == None):
        args.worldname = args.servername
    return(args.minecraftdir,args.servername,args.worldname)


def cursessetup():

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.halfdelay(10)

    # Start colors in curses

    if curses.has_colors():
        curses.start_color()

    curses.init_pair(BCStatusBar.STATSBAR_COLOR, curses.COLOR_WHITE, 240)
    curses.init_pair(BCStatusBar.STATSBAR_REALTIMECOLOR, curses.COLOR_BLACK, 34)
    curses.init_pair(BCStatusBar.STATSBAR_UNTILRAINCOLOR, curses.COLOR_BLACK, 26)
    curses.init_pair(BCStatusBar.STATSBAR_UNTILTHUNDERCOLOR, curses.COLOR_BLACK, 237)

    curses.init_pair(BCGameInstance.DAWN, curses.COLOR_BLACK, 216)           # 1 BRIGHT YELLOW (1min 40secs)
    curses.init_pair(BCGameInstance.WORKDAY, curses.COLOR_BLACK, 192)           # 2 YELLOW (5mins 50secs)
    curses.init_pair(BCGameInstance.HAPPYHOUR, curses.COLOR_BLACK, 181)       # 3 LIGHT BLUE/PURPLE (2mins 30secs)
    curses.init_pair(BCGameInstance.TWILIGHT, curses.COLOR_BLACK, 147)       # 4 PURPLE (27secs)
    curses.init_pair(BCGameInstance.SLEEP, curses.COLOR_WHITE, 63)          # 5 DARK BLUE PURPLE (21secs)
    curses.init_pair(BCGameInstance.MONSTERS, curses.COLOR_WHITE, 17)      # 7 DARKEST BLUE/BLACK (8mins 1secs)
    curses.init_pair(BCGameInstance.NOMONSTERS, curses.COLOR_WHITE, 20)    # 8 LIGHT BLUE (11 secs)
    curses.init_pair(BCGameInstance.NOSLEEP, curses.COLOR_WHITE, 96)        # PINK (27secs)


def rendermenubar(stdscr, servername, worldname):

    stdscr.addstr(0,0,f"BC HUD {servername}:{worldname}", curses.A_BOLD | curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)


def main(stdscr, minecraftdir, servername, worldname):

    cursessetup()

    stdscr.clear()
    stdscr.noutrefresh()
    height, width = stdscr.getmaxyx()

    statwin = curses.newwin(height-2,width,1,0)
    statusbarwin = curses.newwin(height-2,width,1,0)

    bcstatwindow = BCStatWindow(statwin)
    bcstatusbar = BCStatusBar(stdscr,statusbarwin)

    statpanel = curses.panel.new_panel(statwin)
    statusbarpanel = curses.panel.new_panel(statusbarwin)

    key = 0
    activewindow=1

    bcgi = BCGameInstance(minecraftdir,servername,worldname)

    # Loop where k is the last character presse
    while (key != ord('q')):

        if key == ord('s'):
            bcgi.SaveAllFiles()
        elif key == ord('t'):
            bcstatwindow.RecordTime()
        elif key == ord('0'):
            stdscr.clear()
            statusbarwin.clear()
            statwin.clear()
            activewindow = 0
        elif key == ord('1'):
            stdscr.clear()
            statusbarwin.clear()
            statwin.clear()
            activewindow = 1
        elif key == ord('2'):
            stdscr.clear()
            statusbarwin.clear()
            statwin.clear()
            activewindow = 2 
        elif key == curses.KEY_RESIZE or key == ord('w'):
            stdscr.clear()
            statusbarwin.clear()
            statwin.clear()

        bcgi.UpdateGameInfo()

        rendermenubar(stdscr,servername,worldname) 
        bcstatusbar.Render(bcgi)
        stdscr.noutrefresh()

        if (activewindow==1):
            bcstatusbar.RenderWindow(bcgi) 
            statusbarwin.noutrefresh()
            statpanel.hide()
            statusbarpanel.show()
        elif (activewindow==2):
            bcstatwindow.Render(bcgi) 
            statwin.noutrefresh()
            statpanel.show()
            statusbarpanel.hide()
        else:
            statpanel.hide()
            statusbarpanel.hide()

        curses.panel.update_panels()
        curses.doupdate()

        # Wait for next input
        key = stdscr.getch()

if __name__ == "__main__":
    (minecraftdir,servername,worldname) = initserver()
    curses.wrapper(main, minecraftdir, servername, worldname)
=======
from bchud.bchudconstants import BCHudConstants
from bchud.gameinstance.bcgameinstance import BCGameInstance
from bcmenubar import BCMenuBar
from bcstatusbar import BCStatusBar
from bcdebugwindow import BCDebugWindow
from bcadvancementwindow import BCAdvancementWindow

from os import environ
import curses
from curses import panel

def main(stdscr:curses.window, minecraftdir, worldname, servername):

    bcgi = BCGameInstance(minecraftdir, worldname, servername)
    bcmenubar = BCMenuBar(stdscr,bcgi)
    bcstatusbar = BCStatusBar(stdscr,bcgi)
    bcdebugwindow = BCDebugWindow(stdscr,bcgi)
    bcadvancementwindow = BCAdvancementWindow(stdscr,bcgi)

    open_window = 0
    bcmenubar.override_result(BCHudConstants.BCMENU_LEVEL_INFO)

    BCHudConstants.curses_setup(stdscr)

    bcgi.set_auto_backup(True)
    bcgi.set_auto_backup_delay(1200.0)

    try:
        keyboardinput = 0 
        while keyboardinput != ord("q") and not bcmenubar.exit(): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)
            bcgi.update_game_info()

            if bcmenubar.is_open():
                bcmenubar.event_handler(keyboardinput)
            elif keyboardinput == ord('\t'):
                bcmenubar.open()
            elif bcadvancementwindow.is_open():
                bcadvancementwindow.event_handler(keyboardinput)

            if bcmenubar.result() != open_window:
                if open_window == BCHudConstants.BCMENU_LEVEL_INFO:
                    bcdebugwindow.close()
                elif open_window >= BCHudConstants.BCMENU_BACAP_ADVANCEMENTS and open_window <= BCHudConstants.BCMENU_SUPER_CHALLENGES:
                    bcadvancementwindow.close()
                open_window = bcmenubar.result()
                if open_window >= BCHudConstants.BCMENU_BACAP_ADVANCEMENTS and open_window <= BCHudConstants.BCMENU_SUPER_CHALLENGES:
                    bcadvancementwindow.selected_advancement_list(open_window)

            if open_window == BCHudConstants.BCMENU_LEVEL_INFO:
                bcdebugwindow.render(height,width)
            elif open_window >= BCHudConstants.BCMENU_BACAP_ADVANCEMENTS and open_window <= BCHudConstants.BCMENU_SUPER_CHALLENGES:
                bcadvancementwindow.render(height,width)

            bcstatusbar.render(height,width)
            bcmenubar.render(height,width)

            panel.update_panels()
            curses.doupdate()
            if not bcmenubar.exit():
                keyboardinput = stdscr.getch()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == "__main__":
    (minecraftdir, worldname, servername) = BCHudConstants.init_server()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, worldname, servername)
>>>>>>> refs/remotes/origin/main
