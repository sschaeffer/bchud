#!/usr/bin/python3

from bclevelfile import BCLevelFile
from bclogfile import BCLogFile
from bcstatwindow import BCStatWindow
from bcstatusbar import BCStatusBar
from datetime import datetime, timedelta
from math import floor
from time import time, sleep, strftime, strptime
import curses
import curses.panel
from subprocess import call


def saveallfiles():
    call(["/home/integ/Code/stage/save-it-all.bash"])
    sleep(0.5)


def rendermenubar(stdscr,bct):
    stdscr.addstr(0,0,"BC HUD", curses.A_BOLD | curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)




def rendertimerwindow(timerwin,bct):
    # Declaration of strings
    timerwin.box()

    title = "Minecraft Timers (level.dat) "+"\U0001F923"
    leveldattime = 'level.dat last modified {} '.format(datetime.fromtimestamp(bct.lastupdatetime).strftime("%H:%M:%S"))
    filetimes = '(no change {})'.format(datetime.fromtimestamp(bct.lastcheckedtime - bct.lastupdatetime).strftime("%Mmins %Ssecs"))
    timedifference = 'The est new gametime is {} and daytime is {}'.format(round(bct.EstimatedGameTime()),bct.EstimatedDayTime()%24000)
    clearweather = 'Clear weather time: {} ({})'.format(round(bct.EstimatedClearWeatherTime()),bct.clearweathertime)
    rain = 'Rain ({}) time: {} ({})'.format(bct.raining, round(bct.EstimatedRainTime()), bct.raintime)
    thunder = 'Thunder ({}) time: {} ({})'.format(bct.thundering, round(bct.EstimatedThunderTime()),bct.thundertime)
    wandertrader = 'Wandering Trader: {} {} ({}/{})'.format(bct.wanderingtraderid,round(bct.EstimatedWanderingTraderSpawnDelay()),bct.wanderingtraderspawndelay,bct.wanderingtraderchance)

    i=1
    timerwin.addstr(i,1,title)
    i+=1
    timerwin.addstr(i,1,leveldattime+filetimes)
    i+=1
    timerwin.addstr(i,1,timedifference)
    i+=1
    timerwin.addstr(i,1,clearweather)
    i+=1
    timerwin.addstr(i,1,rain)
    i+=1
    timerwin.addstr(i,1,thunder)
    i+=1
    timerwin.addstr(i,1,wandertrader)

def main(stdscr):

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.halfdelay(10)

    # Start colors in curses

    if curses.has_colors():
        curses.start_color()

    curses.init_pair(BCStatusBar.STATSBAR_COLOR, curses.COLOR_WHITE, 240)
    curses.init_pair(BCStatusBar.STATSBAR_REALTIMECOLOR, curses.COLOR_BLACK, 34)

    curses.init_pair(BCLevelFile.DAWN, curses.COLOR_BLACK, 220)           # 1 BRIGHT YELLOW (1min 40secs)
    curses.init_pair(BCLevelFile.WORKDAY, curses.COLOR_BLACK, 192)           # 2 YELLOW (5mins 50secs)
    curses.init_pair(BCLevelFile.HAPPYHOUR, curses.COLOR_WHITE, 141)       # 3 LIGHT BLUE/PURPLE (2mins 30secs)
    curses.init_pair(BCLevelFile.TWILIGHT, curses.COLOR_WHITE, 57)       # 4 PURPLE (27secs)
    curses.init_pair(BCLevelFile.SLEEP, curses.COLOR_WHITE, 17)          # 5 DARK BLUE PURPLE (21secs)
    curses.init_pair(BCLevelFile.RAINMONSTERS, curses.COLOR_WHITE, 201)   # 6 DARK BLUE (11secs)
    curses.init_pair(BCLevelFile.MONSTERS, curses.COLOR_WHITE, 21)      # 7 DARKEST BLUE/BLACK (8mins 1secs)
    curses.init_pair(BCLevelFile.NOMONSTERS, curses.COLOR_WHITE, 96)    # 8 LIGHT BLUE (11 secs)
    curses.init_pair(BCLevelFile.NORAINMONSTERS, curses.COLOR_WHITE, 201) # LIGHTER BLUE/PINK (22secs)
    curses.init_pair(BCLevelFile.NOSLEEP, curses.COLOR_WHITE, 173)        # PINK (27secs)


    stdscr.clear()
    stdscr.noutrefresh()
    height, width = stdscr.getmaxyx()
    timerwin = curses.newwin(height-2,width,1,0)
    statwin = curses.newwin(height-2,width,1,0)
    statusbarwin = curses.newwin(height-2,width,1,0)

    bcstatwindow = BCStatWindow(statwin)
    bcstatusbar = BCStatusBar(stdscr,statusbarwin)

    timerpanel = curses.panel.new_panel(timerwin)
    statpanel = curses.panel.new_panel(statwin)
    statusbarpanel = curses.panel.new_panel(statusbarwin)

    key = 0
    activewindow=3
    
    bct = BCLevelFile(logresults=True)
    bct.ReadLevelFile()
    bclf = BCLogFile()
    bclf.ReadLogFile()

    # Loop where k is the last character presse
    while (key != ord('q')):

        if key == ord('r'):
            bct.ReadLevelFile()
            bclf.ReadLogFile()
        elif key == ord('s'):
            saveallfiles()
        elif key == ord('t'):
            bcstatwindow.RecordTime(bct)
        elif key == ord('0'):
            activewindow = 0
        elif key == ord('1'):
            activewindow = 1
        elif key == ord('2'):
            activewindow = 2 
        elif key == ord('3'):
            activewindow = 3 
        bct.ReadLevelFile()
        bclf.ReadLogFile()

        rendermenubar(stdscr,bct) 
        bcstatusbar.Render(bct)
        stdscr.noutrefresh()

        if (activewindow==1):
            rendertimerwindow(timerwin,bct) 
            timerwin.noutrefresh()
            timerpanel.show()
            statpanel.hide()
            statusbarpanel.hide()
        elif (activewindow==2):
            bcstatwindow.Render(bclf) 
            statwin.noutrefresh()
            statpanel.show()
            timerpanel.hide()
            statusbarpanel.hide()
        elif (activewindow==3):
            bcstatusbar.RenderWindow(bct) 
            statusbarwin.noutrefresh()
            statpanel.hide()
            timerpanel.hide()
            statusbarpanel.show()
        else:
            timerpanel.hide()
            statpanel.hide()
            statusbarpanel.hide()

        curses.panel.update_panels()
        curses.doupdate()

        # Wait for next input
        key = stdscr.getch()


curses.wrapper(main)