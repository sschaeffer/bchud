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
    timedifference = 'The est new gametime is {} and our est old is {}'.format(round(bct.EstimatedGameTime()), 0)
    erroroffset="Null"
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
    timerwin.addstr(i,1,erroroffset)
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

    curses.init_pair(BCStatusBar.STATSBAR_DAYTIMECOLOR, curses.COLOR_WHITE, 17)
    curses.init_pair(BCStatusBar.STATSBAR_AFTERDINNERCOLOR, curses.COLOR_BLACK, 192)
    curses.init_pair(BCStatusBar.STATSBAR_TWILIGHTCOLOR, curses.COLOR_WHITE, 141)
    curses.init_pair(BCStatusBar.STATSBAR_NIGHTCOLOR, curses.COLOR_WHITE, 21)
    curses.init_pair(STATSBAR_DAWNCOLOR, curses.COLOR_WHITE, 21)

    stdscr.clear()
    stdscr.noutrefresh()
    height, width = stdscr.getmaxyx()
    timerwin = curses.newwin(height-2,width-2,1,1)
    statwin = curses.newwin(height-2,width-2,1,1)
    bcstatwindow = BCStatWindow(statwin)
    bcstatusbar = BCStatusBar(stdscr)

    timerpanel = curses.panel.new_panel(timerwin)
    statpanel = curses.panel.new_panel(statwin)

    key = 0
    activewindow=2
    
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
        elif (activewindow==2):
            bcstatwindow.Render(bclf) 
            statwin.noutrefresh()
            statpanel.show()
            timerpanel.hide()
        else:
            timerpanel.hide()
            statpanel.hide()

        curses.panel.update_panels()
        curses.doupdate()

        # Wait for next input
        key = stdscr.getch()


curses.wrapper(main)