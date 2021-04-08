#!/usr/bin/env python3

from bclevelfile import BCLevelFile
from math import floor
from datetime import datetime, timedelta
from time import time, sleep, strftime, strptime
import curses

class BCStatusBar():


    STATSBAR_COLOR=21            #DARKGREY
    STATSBAR_REALTIMECOLOR=22    #GREEN

    def __init__(self,stdscr,statusbarwin):
        self.stdscr = stdscr
        self.statusbarwin = statusbarwin
        self.esttimeofday = 1

    def Render(self,bct):

        (height,width) = self.stdscr.getmaxyx()
        currenttimestr = strftime(" %H:%M:%S")
        hmsgametimestr = " {} ".format(timedelta(seconds=round(bct.EstimatedGameTime()/20)))
        daystr = str(floor(bct.EstimatedDayTime()/24000)+1)

        self.stdscr.chgat(height-1, 0, -1, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, width-(len(currenttimestr)+len(hmsgametimestr)+1), hmsgametimestr, curses.color_pair(self.STATSBAR_REALTIMECOLOR))
        self.stdscr.addstr(height-1, width-(len(currenttimestr)+1), currenttimestr, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.chgat(-1,curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, 0, f" Day {daystr} ",curses.color_pair(self.STATSBAR_REALTIMECOLOR))

        statusbar_esttimeofday = bct.EstimatedTimeOfDay()
        if statusbar_esttimeofday >= bct.SLEEP:
            displaytime = (bct.DAY_FULLDAY-(bct.EstimatedDayTime()%bct.DAY_FULLDAY))/20
        else:
            displaytime = (bct.DAY_SLEEP-(bct.EstimatedDayTime()%bct.DAY_FULLDAY))/20
        #displaytimestr = '  {:0}:{:02} \U0001F4A4 '.format(floor(abs(displaytime)/60),floor(abs(displaytime)%60),esttimeofday,bct.EstimatedDayTime()%bct.DAY_FULLDAY)
        displaytimestr = '  {: 2}:{:02}  '.format(floor(abs(displaytime)/60),floor(abs(displaytime)%60))
        self.stdscr.addstr(height-1, (width//2)-(len(displaytimestr)),displaytimestr,curses.color_pair(statusbar_esttimeofday))

    def RenderWindow(self,bct):
        (height,width) = self.statusbarwin.getmaxyx()

        leveltime = f"level.dat {datetime.fromtimestamp(bct.lastupdatetime).strftime('%H:%M:%S')}"



        keysize=34
        self.statusbarwin.addstr(bct.DAWN-1, width-keysize, "10:27- 8:27 Dawn/Waking/Wandering ", curses.color_pair(bct.DAWN))
        self.statusbarwin.addstr(bct.WORKDAY-1, width-keysize, " 8:27- 2:57 Workday               ", curses.color_pair(bct.WORKDAY))
        self.statusbarwin.addstr(bct.HAPPYHOUR-1, width-keysize, " 2:57- 0:27 Happy-hour/Socializing", curses.color_pair(bct.HAPPYHOUR))
        self.statusbarwin.addstr(bct.TWILIGHT-1, width-keysize, " 0:27- 0:00 Twilight/Sleeping Vill", curses.color_pair(bct.TWILIGHT))
        self.statusbarwin.addstr(bct.SLEEP-1, width-keysize, " 9:33- 9:01 Beds are Usable       ", curses.color_pair(bct.SLEEP))
        self.statusbarwin.addstr(bct.MONSTERS-1, width-keysize, " 9:01- 0:59 Night-time            ", curses.color_pair(bct.MONSTERS))
        self.statusbarwin.addstr(bct.NOMONSTERS-1, width-keysize, " 0:59- 0:27 No New Monsters       ", curses.color_pair(bct.NOMONSTERS))
        self.statusbarwin.addstr(bct.NOSLEEP-1, width-keysize, " 0:27- 0:00 Pre-dawn/Beds Unusable", curses.color_pair(bct.NOSLEEP))

#        self.statusbarwin.addstr(5, width-43, " 9:12- 9:01 Monsters Spawning (Rainy day)", curses.color_pair(bct.RAINMONSTERS))
#        self.statusbarwin.addstr(8, width-43, " 0:48- 0:27 No New Monsters (Rainy day)  ", curses.color_pair(bct.NORAINMONSTERS))

#        self.statusbarwin.addstr(0, width-43, "    0 -  2000 Dawn Wandering   10:27 - 8:47", curses.color_pair(bct.DAWN))
#        self.statusbarwin.addstr(1, width-43, " 2000 -  9000 Workday           8:47 - 2:57", curses.color_pair(bct.WORKDAY))
#        self.statusbarwin.addstr(2, width-43, " 9000 - 12000 Happyhour Social  2:57 - 0:27", curses.color_pair(bct.HAPPYHOUR))
#        self.statusbarwin.addstr(3, width-43, "12000 - 12542 Twilight          0:27 - 0:00", curses.color_pair(bct.TWILIGHT))
#        self.statusbarwin.addstr(4, width-43, "12542 - 12969 Able to Sleep     9:33 - 9:12", curses.color_pair(bct.SLEEP))
#        self.statusbarwin.addstr(6, width-43, "12969 - 13188 Rainy Monsters    9:12 - 9:01", curses.color_pair(bct.RAINMONSTERS))
#        self.statusbarwin.addstr(7, width-43, "13188 - 22812 Monsters Spawn    9:01 - 0:59", curses.color_pair(bct.MONSTERS))
#        self.statusbarwin.addstr(8, width-43, "22812 - 23031 No New Monsters   0:59 - 0:48", curses.color_pair(bct.NOMONSTERS))
#        self.statusbarwin.addstr(9, width-43, "23031 - 23460 No Rainy Monsters 0:48 - 0:27", curses.color_pair(bct.NORAINMONSTERS))
#        self.statusbarwin.addstr(10, width-43, "23460 - 24000 If Clear No Beds  0:27 - 0:00", curses.color_pair(bct.NOSLEEP))

        if self.esttimeofday != bct.EstimatedTimeOfDay():
            self.statusbarwin.addstr(self.esttimeofday-1, width-(keysize+6), "      ")
            self.esttimeofday = bct.EstimatedTimeOfDay()

        if self.esttimeofday >= bct.SLEEP:
            displaytime = (bct.DAY_FULLDAY-(bct.EstimatedDayTime()%bct.DAY_FULLDAY))/20
        else:
            displaytime = (bct.DAY_SLEEP-(bct.EstimatedDayTime()%bct.DAY_FULLDAY))/20
        displaytimestr = f"{floor(abs(displaytime)/60):>2}:{floor(abs(displaytime)%60):02} "
        self.statusbarwin.addstr(self.esttimeofday-1, width-(keysize+6), displaytimestr,curses.color_pair(self.esttimeofday))
       













#        negbeforenight = "-" if beforenight < 0 else ""
#        beforenightstr = '{}{:0}:{:02} '.format(negbeforenight,floor(abs(beforenight)/60),round(abs(beforenight)%60))
#
#        beforemonster = (13188-(bct.EstimatedDayTime()%24000))/20
#        negbeforemonster = "-" if beforemonster < 0 else ""
#        beforemonsterstr = '({}{:0}:{:02})'.format(negbeforemonster,floor(abs(beforemonster)/60),round(abs(beforemonster)%60))
#
#        centerstatusbarstr = beforenightstr + beforemonsterstr
#        self.stdscr.addstr(height-1, (width//2)-(len(centerstatusbarstr)//2),centerstatusbarstr)
#        self.stdscr.attroff(curses.color_pair(1))