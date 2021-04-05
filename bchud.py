#!/usr/bin/python3

from bctimer import BCTimer
from bclogfile import BCLogFile
from datetime import datetime,timedelta
from math import floor
import time
import curses
import curses.panel


def rendermenubar(stdscr,bct):
    stdscr.addstr("BC HUD", curses.A_BOLD | curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

def renderstatusbar(stdscr,bct):
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    
    currenttimestr = time.strftime("%H:%M")
    hmsgametimestr = str(timedelta(seconds=round(bct.estgametime()/20)))
    daytimestr = str(floor(bct.estdaytime()%24000))
    daystr = str(floor(bct.estdaytime()/24000))
    rightstatusbarstr = '({}){} | {} | {} '.format(daystr, daytimestr, hmsgametimestr, currenttimestr)

    stdscr.addstr(height-1, 0, " " * (width -1))
    stdscr.addstr(height-1, width-(len(rightstatusbarstr)+1),rightstatusbarstr)

    beforenight = (12542-(bct.estdaytime()%24000))/20
    negbeforenight = "-" if beforenight < 0 else ""
    beforenightstr = '{}{:0}:{:02} '.format(negbeforenight,floor(abs(beforenight)/60),round(abs(beforenight)%60))

    beforemonster = (13188-(bct.estdaytime()%24000))/20
    negbeforemonster = "-" if beforemonster < 0 else ""
    beforemonsterstr = '({}{:0}:{:02})'.format(negbeforemonster,floor(abs(beforemonster)/60),round(abs(beforemonster)%60))

    centerstatusbarstr = beforenightstr + beforemonsterstr
    stdscr.addstr(height-1, (width//2)-(len(centerstatusbarstr)//2),centerstatusbarstr)
    stdscr.attroff(curses.color_pair(1))

def renderstatwindow(statwin, bct, bclf):
    statwin.box()
    for i in range(8):
        statwin.addstr(i+1,1,bct.timerhistory[i])
        bclf_update = bclf.GetLogUpdate(bclf.NumLogUpdates()-i)
        if bclf_update != None:
            updatestr="{} {:5.0f} {} {}".format(bclf_update._updatetime,bclf_update._gametime,bclf_update.estgametime(),bclf_update.eststarttime())
            statwin.addstr(i,33,updatestr)
        i+=1

def rendertimerwindow(timerwin,bct):
    # Declaration of strings
    timerwin.box()

    title = "Minecraft Timers (level.dat) "+"\U0001F923"
    leveldattime = 'level.dat last modified {} '.format(datetime.fromtimestamp(bct.mtime).strftime("%H:%M:%S"))
    filetimes = '(no change {})'.format(datetime.fromtimestamp(bct.checktime - bct.mtime).strftime("%Mmins %Ssecs"))
    timedifference = 'The est new gametime is {} and our est old is {}'.format(round(bct.estgametime()), round(bct.estoldgametime()))
    erroroffset = 'The error offset during the last update was {:.04f} seconds'.format(round(bct.estgametime() - bct.estoldgametime()))
    clearweather = 'Clear weather time: {} ({})'.format(round(bct.estclearweathertime()),bct.clearweathertime)
    rain = 'Rain ({}) time: {} ({})'.format(bct.raining, round(bct.estraintime()), bct.raintime)
    thunder = 'Thunder ({}) time: {} ({})'.format(bct.thundering, round(bct.estthundertime()),bct.thundertime)
    wandertrader = 'Wandering Trader: {} {} ({}/{})'.format(bct.wanderingTrader,round(bct.estwandertradertime()),bct.wanderingTraderTime,bct.wanderingTraderChance)

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

    timerpanel = curses.panel.new_panel(timerwin)
    statpanel = curses.panel.new_panel(statwin)

    key = 0
    activewindow=2
    readtimer=readtimercount=15
    bct = BCTimer()
    bct.readlevelfile()
    bclf = BCLogFile()
    bclf.ReadLogFile()

    # Loop where k is the last character pressed
    while (key != ord('q')):

        if key == ord('r'):
            bclf.ReadLogFile()
            bct.readlevelfile()
            readtimercount=readtimer
        elif key == ord('s'):
            bct.saveallfiles()
        elif key == ord('t'):
            bct.recordtime()
            bclf.ReadLogFile()
        elif key == ord('0'):
            activewindow = 0
        elif key == ord('1'):
            activewindow = 1
        elif key == ord('2'):
            activewindow = 2 
        if readtimercount <= 0:
            bclf.ReadLogFile()
            bct.readlevelfile()
            readtimercount=readtimer
        readtimercount-=1

        rendermenubar(stdscr,bct) 
        renderstatusbar(stdscr,bct) 
        stdscr.noutrefresh()

        if (activewindow==1):
            rendertimerwindow(timerwin,bct) 
            timerwin.noutrefresh()
            timerpanel.show()
            statpanel.hide()
        elif (activewindow==2):
            renderstatwindow(statwin,bct,bclf) 
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