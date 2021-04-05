#!/usr/bin/python3

from bclevelfile import BCLevelFile
from bclogfile import BCLogFile, BCLogFileUpdate
from datetime import datetime, timedelta
from math import floor
from time import time, sleep, strftime, strptime
import curses
import curses.panel
from subprocess import call


class BCStatWindow():

    def __init__(self, window):
        self.window = window
        self.statcount = 8
        self.stats = ["{}".format(i) for i in range(self.statcount)]

    def RenderStatWindow(self, bclf):
        self.window.box()
        for i in range(self.statcount):
            self.window.addstr(i+1,1,self.stats[i])
            bclf_update = bclf.GetLogUpdate(bclf.NumLogUpdates()-(i+1))
            if bclf_update != None:
                updatestr="{} {:5.0f} ".format(bclf_update._updatetime.strftime("(%m/%d)%H:%M:%S"),bclf_update._gametime)
                updatestr=updatestr+"{} {}".format(bclf_update.estgametime(),datetime.fromtimestamp(bclf_update.eststarttime()).strftime("(%m/%d)%H:%M:%S"))
                self.window.addstr(i+1,33,updatestr)

    def RecordTime(self,bct):
        for i in range(self.statcount-1):
            self.stats[(self.statcount-1)-i] = self.stats[(self.statcount-1)-(i+1)]
        self.stats[0] = "[{}] The time is {}".format(strftime("%H:%M:%S"),round(bct.EstimatedGameTime()))
        call(["/home/integ/Code/stage/query-time.bash"])
        sleep(0.5)

def saveallfiles():
    call(["/home/integ/Code/stage/save-it-all.bash"])
    sleep(0.5)

def rendermenubar(stdscr,bct):
    stdscr.addstr("BC HUD", curses.A_BOLD | curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

def renderstatusbar(stdscr,bct):
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    
    currenttimestr = strftime("%H:%M")
    hmsgametimestr = str(timedelta(seconds=round(bct.EstimatedGameTime()/20)))
    daytimestr = str(floor(bct.EstimatedDayTime()%24000))
    daystr = str(floor(bct.EstimatedDayTime()/24000))
    rightstatusbarstr = '({}){} | {} | {} '.format(daystr, daytimestr, hmsgametimestr, currenttimestr)

    stdscr.addstr(height-1, 0, " " * (width -1))
    stdscr.addstr(height-1, width-(len(rightstatusbarstr)+1),rightstatusbarstr)

    beforenight = (12542-(bct.EstimatedDayTime()%24000))/20
    negbeforenight = "-" if beforenight < 0 else ""
    beforenightstr = '{}{:0}:{:02} '.format(negbeforenight,floor(abs(beforenight)/60),round(abs(beforenight)%60))

    beforemonster = (13188-(bct.EstimatedDayTime()%24000))/20
    negbeforemonster = "-" if beforemonster < 0 else ""
    beforemonsterstr = '({}{:0}:{:02})'.format(negbeforemonster,floor(abs(beforemonster)/60),round(abs(beforemonster)%60))

    centerstatusbarstr = beforenightstr + beforemonsterstr
    stdscr.addstr(height-1, (width//2)-(len(centerstatusbarstr)//2),centerstatusbarstr)
    stdscr.attroff(curses.color_pair(1))


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

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.noutrefresh()
    height, width = stdscr.getmaxyx()
    timerwin = curses.newwin(height-2,width-2,1,1)
    statwin = curses.newwin(height-2,width-2,1,1)
    bcstatwindow = BCStatWindow(statwin)

    timerpanel = curses.panel.new_panel(timerwin)
    statpanel = curses.panel.new_panel(statwin)

    key = 0
    activewindow=2
    
    bct = BCLevelFile()
    bct.ReadLevelFile()
    bclf = BCLogFile()
    bclf.ReadLogFile()

    # Loop where k is the last character pressed
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
        renderstatusbar(stdscr,bct)
        stdscr.noutrefresh()

        if (activewindow==1):
            rendertimerwindow(timerwin,bct) 
            timerwin.noutrefresh()
            timerpanel.show()
            statpanel.hide()
        elif (activewindow==2):
            bcstatwindow.RenderStatWindow(bclf) 
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