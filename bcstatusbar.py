from bclevelfile import BCLevelFile
from math import floor
from datetime import datetime, timedelta
from time import time, sleep, strftime, strptime
import curses

class BCStatusBar():


    STATSBAR_COLOR=21            #DARKGREY
    STATSBAR_REALTIMECOLOR=22    #GREEN

    STATSBAR_DAWN=0           # BRIGHT YELLOW (1min 40secs)
    STATSBAR_WORKDAY=1        # YELLOW (5mins 50secs)
    STATSBAR_HAPPYHOUR=2      # LIGHT BLUE (2mins 30secs)
    STATSBAR_TWILIGHT=3       # PURPLE (27secs)
    STATSBAR_RAINMONSTERS=7   # DARK BLUE (21secs)
    STATSBAR_MONSTERS=7       #
    STATSBAR_NOMONSTERS=7     #
    STATSBAR_NORAINMONSTERS=7 #
    STATSBAR_NOSLEEP=7        # 30secs

    DAY_DAWNSTARTS=0         #    0-2000 Wakeup and Wander (0:00)
    DAY_WORKDAYSTARTS=2000   # 2000-9000 Workday (1:40)
    DAY_WORKDAYENDS=9000     # 9000-12000 Happy-hour (7:30)
    DAY_SLEEP=12000          # 12000 Twilight/villagers sleep (10:00) - 12010 sleep on rainy days
    DAY_ENDS=12542           # 12542 Sleep on normal days/mobs don't burn (10:27)
    DAY_RAINMONSTERS=12969   # 12969 Rainy day monsters (10:48/18secs)
    DAY_MONSTERS=13188       # 13188 monsters (11:00/30secs)
    DAY_NOMONSTERS=22812     # 22812 No more monsters (19:00/8:30)
    DAY_NORAINMONSTERS=23031 # 12969 No more rainy day monsters(19:12/8:42)
    DAY_NOSLEEP=23460        # 23460 No sleeping on normal days (19:33/9:03)
    DAY_FULLDAY=24000        # 23992 No sleeping rainy days (19:59/9:30)




    def __init__(self,stdscr):
        self.stdscr = stdscr

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

        estdaytime = bct.EstimatedDayTime()%24000

        beforenight = (12542-(bct.EstimatedDayTime()%24000))/20
        if beforenight < 0:
            beforenight = (24000-(bct.EstimatedDayTime()%24000))/20
            beforenightstr = '  {:0}:{:02}  '.format(floor(abs(beforenight)/60),round(abs(beforenight)%60))
            if beforenight >= 60:
                self.stdscr.addstr(height-1, (width//2)-(len(beforenightstr)),beforenightstr,curses.color_pair(3))
            else:
                self.stdscr.addstr(height-1, (width//2)-(len(beforenightstr)),beforenightstr,curses.color_pair(6))
        else:
            beforenightstr = '  {:0}:{:02}  '.format(floor(abs(beforenight)/60),round(abs(beforenight)%60))
            if beforenight >= 60:
                self.stdscr.addstr(height-1, (width//2)-(len(beforenightstr)),beforenightstr,curses.color_pair(4))
            else:
                self.stdscr.addstr(height-1, (width//2)-(len(beforenightstr)),beforenightstr,curses.color_pair(5))


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