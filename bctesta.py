#!/usr/bin/python3

from bcgameinstance import BCGameInstance
from bcadvancementwindow import BCAdvancementWindow
from bctimerwindow import BCTimerWindow
from bcstatusbar import BCStatusBar

import curses
import curses.panel

import argparse


def initserver(argv=None):

    parser = argparse.ArgumentParser(prog='bchud')
    parser.add_argument('--minecraftdir', default="/media/local/Minecraft/server", help="minecraft server directory")
    parser.add_argument('--servername', default="fury", help="servername is the name of the server")
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
        curses.use_default_colors()

    curses.init_pair(BCStatusBar.STATSBAR_COLOR, curses.COLOR_WHITE, 240)
    curses.init_pair(BCStatusBar.STATSBAR_REALTIMECOLOR, curses.COLOR_BLACK, 34)
    curses.init_pair(BCStatusBar.STATSBAR_UNTILRAINCOLOR, curses.COLOR_BLACK, 26)
    curses.init_pair(BCStatusBar.STATSBAR_UNTILTHUNDERCOLOR, curses.COLOR_BLACK, 237)

    curses.init_pair(BCGameInstance.DAWN, curses.COLOR_BLACK, 216)         # 1 BRIGHT YELLOW (1min 40secs)
    curses.init_pair(BCGameInstance.WORKDAY, curses.COLOR_BLACK, 192)      # 2 YELLOW (5mins 50secs)
    curses.init_pair(BCGameInstance.HAPPYHOUR, curses.COLOR_BLACK, 181)    # 3 LIGHT BLUE/PURPLE (2mins 30secs)
    curses.init_pair(BCGameInstance.TWILIGHT, curses.COLOR_BLACK, 147)     # 4 PURPLE (27secs)
    curses.init_pair(BCGameInstance.SLEEP, curses.COLOR_WHITE, 63)         # 5 DARK BLUE PURPLE (21secs)
    curses.init_pair(BCGameInstance.MONSTERS, curses.COLOR_WHITE, 17)      # 7 DARKEST BLUE/BLACK (8mins 1secs)
    curses.init_pair(BCGameInstance.NOMONSTERS, curses.COLOR_WHITE, 20)    # 8 LIGHT BLUE (11 secs)
    curses.init_pair(BCGameInstance.NOSLEEP, curses.COLOR_WHITE, 96)       # PINK (27secs)

    curses.init_pair(BCAdvancementWindow.ADVANCEMENT_COMPLETE, 46, -1)
    curses.init_pair(BCAdvancementWindow.ADVANCEMENT_INCOMPLETE, 46, -1)




def main(stdscr, minecraftdir, servername, worldname):

    cursessetup()
    stdscr.clear()
    try:
        while True:
            input = stdscr.getch()
            stdscr.addstr(0,0,f"{input}")

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()






#
#    timerwindow = curses.newwin(height-2,width,1,0)
#    statusbarwin = curses.newwin(height-2,width,1,0)
#
#    bctimerwindow = BCTimerWindow(timerwindow)
#    bcstatusbar = BCStatusBar(stdscr,statusbarwin)
#
#    statpanel = curses.panel.new_panel(timerwindow)
#    statusbarpanel = curses.panel.new_panel(statusbarwin)
#
#   key = 0
#   activewindow=1
#

    # Loop where k is the last character presse
   # while (key != ord('q')):
#
#        if key == ord('s'):
#            bcgi.SaveAllFiles()
#        elif key == ord('t'):
#            bctimerwindow.RecordTime(bcgi)
#        elif key == ord('0'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#            activewindow = 0
#        elif key == ord('1'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#            activewindow = 1
#        elif key == ord('2'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#            activewindow = 2 
#        elif key == curses.KEY_RESIZE or key == ord('w'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#

#        rendermenubar(stdscr,bcgi) 
#        bcstatusbar.Render(bcgi)
#        stdscr.noutrefresh()
#
#        if (activewindow==1):
#            bcstatusbar.RenderWindow(bcgi) 
#            statusbarwin.noutrefresh()
#            statpanel.hide()
#            statusbarpanel.show()
#        elif (activewindow==2):
#            bctimerwindow.Render(bcgi) 
#            timerwindow.noutrefresh()
#            statpanel.show()
#            statusbarpanel.hide()
#        else:
#            statpanel.hide()
#            statusbarpanel.hide()
#
#        curses.panel.update_panels()
#        curses.doupdate()

        # Wait for next input




if __name__ == "__main__":
    (minecraftdir,servername,worldname) = initserver()
    curses.wrapper(main, minecraftdir, servername, worldname)