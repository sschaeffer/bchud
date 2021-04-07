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

    def Render(self,bct):

        (height,width) = self.stdscr.getmaxyx()
        currenttimestr = strftime(" %H:%M:%S")
        hmsgametimestr = " {} ".format(timedelta(seconds=round(bct.EstimatedGameTime()/20)))
        daystr = str(floor(bct.EstimatedDayTime()/24000))

        self.stdscr.chgat(height-1, 0, -1, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, width-(len(currenttimestr)+len(hmsgametimestr)+1), hmsgametimestr, curses.color_pair(self.STATSBAR_REALTIMECOLOR))
        self.stdscr.addstr(height-1, width-(len(currenttimestr)+1), currenttimestr, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.chgat(-1,curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, 0, " Day {} ".format(daystr),curses.color_pair(self.STATSBAR_REALTIMECOLOR))

        esttimeofday = bct.EstimatedTimeOfDay()
        if esttimeofday >= bct.RAINMONSTERS:
            displaytime = (bct.DAY_FULLDAY-(bct.EstimatedDayTime()%bct.DAY_FULLDAY))/20
        else:
            displaytime = (bct.DAY_SLEEP-(bct.EstimatedDayTime()%bct.DAY_FULLDAY))/20
        displaytimestr = '  {:0}:{:02} {} {}'.format(floor(abs(displaytime)/60),floor(abs(displaytime)%60),esttimeofday,bct.EstimatedDayTime()%bct.DAY_FULLDAY)
        self.stdscr.addstr(height-1, (width//2)-(len(displaytimestr)),displaytimestr,curses.color_pair(esttimeofday))

    def RenderWindow(self,bct):
        (height,width) = self.statusbarwin.getmaxyx()
        self.statusbarwin.addstr(0, width-40, "    0 -  2000 Dawn        8:47", curses.color_pair(bct.DAWN))
        self.statusbarwin.addstr(1, width-40, " 2000 -  9000 Workday     2:57", curses.color_pair(bct.WORKDAY))
        self.statusbarwin.addstr(2, width-40, " 9000 - 12000 Happyhour    :27", curses.color_pair(bct.HAPPYHOUR))
        self.statusbarwin.addstr(3, width-40, "12000 - 12542 Twilight     :00", curses.color_pair(bct.TWILIGHT))
        self.statusbarwin.addstr(4, width-40, "12542 - 12969 Sleeptime   9:33", curses.color_pair(bct.SLEEP))
        self.statusbarwin.addstr(5, width-40, "12969 - 13188 Rainy Mnst  9:12", curses.color_pair(bct.RAINMONSTERS))
        self.statusbarwin.addstr(6, width-40, "13188 - 22812 Monsters    9:01", curses.color_pair(bct.MONSTERS))
        self.statusbarwin.addstr(7, width-40, "22812 - 23031 No Monsters  :49", curses.color_pair(bct.NOMONSTERS))
        self.statusbarwin.addstr(8, width-40, "23031 - 23460 No Rainy Mo  :27", curses.color_pair(bct.NORAINMONSTERS))
        self.statusbarwin.addstr(9, width-40, "23460 - 24000 No Sleep     :00", curses.color_pair(bct.NOSLEEP))
       













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