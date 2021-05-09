#!/usr/bin/python3

from bclevelfile import BCLevelFile
from bclogfile import BCLogFile
from bclog import BCLog
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
    parser.add_argument('--servername', default="snapshot", help="servername is the name of the server")
    parser.add_argument('--worldname', help="worldname is the name of the world (if different then server)")
    args = parser.parse_args(argv)
    if(args.worldname == None):
        args.worldname = args.servername
    return(args.servername,args.worldname)



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

    curses.init_pair(BCLevelFile.DAWN, curses.COLOR_BLACK, 216)           # 1 BRIGHT YELLOW (1min 40secs)
    curses.init_pair(BCLevelFile.WORKDAY, curses.COLOR_BLACK, 192)           # 2 YELLOW (5mins 50secs)
    curses.init_pair(BCLevelFile.HAPPYHOUR, curses.COLOR_BLACK, 181)       # 3 LIGHT BLUE/PURPLE (2mins 30secs)
    curses.init_pair(BCLevelFile.TWILIGHT, curses.COLOR_BLACK, 147)       # 4 PURPLE (27secs)
    curses.init_pair(BCLevelFile.SLEEP, curses.COLOR_WHITE, 63)          # 5 DARK BLUE PURPLE (21secs)
    curses.init_pair(BCLevelFile.MONSTERS, curses.COLOR_WHITE, 17)      # 7 DARKEST BLUE/BLACK (8mins 1secs)
    curses.init_pair(BCLevelFile.NOMONSTERS, curses.COLOR_WHITE, 20)    # 8 LIGHT BLUE (11 secs)
    curses.init_pair(BCLevelFile.NOSLEEP, curses.COLOR_WHITE, 96)        # PINK (27secs)


def rendermenubar(stdscr, servername, worldname):

    stdscr.addstr(0,0,f"BC HUD {servername}:{worldname}", curses.A_BOLD | curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)


def main(stdscr, servername, worldname):

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

    bclog = BCLog(servername,worldname)
    bclf = BCLogFile(bclog=bclog)
    bct = BCLevelFile(bclf=bclf, bclog=bclog)

    bclf.ReadLogFile()
    bct.ReadLevelFile()

    # Loop where k is the last character presse
    while (key != ord('q')):

        if key == ord('r'):
            bclf.ReadLogFile()
            bct.ReadLevelFile()
        elif key == ord('s'):
            bclog.SaveAllFiles()
        elif key == ord('t'):
            bcstatwindow.RecordTime(bct)
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

        bclf.ReadLogFile()
        bct.ReadLevelFile()

        rendermenubar(stdscr,servername,worldname) 
        bcstatusbar.Render(bct)
        stdscr.noutrefresh()

        if (activewindow==1):
            bcstatusbar.RenderWindow(bct) 
            statusbarwin.noutrefresh()
            statpanel.hide()
            statusbarpanel.show()
        elif (activewindow==2):
            bcstatwindow.Render(bclf) 
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
    (servername,worldname) = initserver()
    curses.wrapper(main, servername, worldname)