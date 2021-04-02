#!/usr/bin/python3

from datetime import datetime,timedelta
from bctimer import BCTimer
from math import floor
import time
import curses


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

def rendertimerwindow(timerwin,bct):
    # Declaration of strings
    title = "Minecraft Timers (level.dat)"
    timerwin.box()
    timerwin.addstr(1,1,title)

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

    key = 0
    readfiletimer=0
    readfilemax=15
    bct = BCTimer()

    # Loop where k is the last character pressed
    while (key != ord('q')):

        if key == ord('r'):
            bct.readnbtfile()
            readfiletimer=0
        elif key == ord('s'):
            bct.savenbtfile()
            bct.readnbtfile()
            readfiletimer=0
        if readfiletimer >= readfilemax:
            bct.readnbtfile()
            readfiletimer=0
        readfiletimer+=1

        # Initialization
        height, width = stdscr.getmaxyx()
        rendermenubar(stdscr,bct) 
        renderstatusbar(stdscr,bct) 
        rendertimerwindow(timerwin,bct) 

        stdscr.noutrefresh()
        timerwin.noutrefresh()
        curses.doupdate()

        #stdscr.attron(curses.A_BOLD)
        #stdscr.attroff(curses.A_BOLD)


        # Wait for next input
        key = stdscr.getch()


curses.wrapper(main)