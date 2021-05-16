#!/usr/bin/env python3

from bcgameinstance import BCGameInstance
from math import floor
from datetime import datetime, timedelta
from time import time, sleep, strftime, strptime
import curses

class BCStatusBar():


    STATSBAR_COLOR=21 
    STATSBAR_REALTIMECOLOR=22    
    STATSBAR_UNTILRAINCOLOR=23   
    STATSBAR_UNTILTHUNDERCOLOR=24   

    def __init__(self,stdscr,statusbarwin):
        self.stdscr = stdscr
        self.statusbarwin = statusbarwin
        self.esttimeofday = 1

    def Render(self,bcgi):

        (height,width) = self.stdscr.getmaxyx()
        currenttimestr = strftime(" %H:%M:%S")
        hmsgametimestr = " {} ".format(timedelta(seconds=round(bcgi.EstimatedGameTime()/20)))
        daystr = str(floor(bcgi.EstimatedDayTime()/24000)+1)

        self.stdscr.chgat(height-1, 0, -1, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, width-(len(currenttimestr)+len(hmsgametimestr)+1), hmsgametimestr, curses.color_pair(self.STATSBAR_REALTIMECOLOR))
        self.stdscr.addstr(height-1, width-(len(currenttimestr)+1), currenttimestr, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.chgat(-1,curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, 0, f" {daystr} ",curses.color_pair(self.STATSBAR_REALTIMECOLOR))
        untilrainstr = f"{bcgi.EstimatedRainTime()/1200:.0f}"
        untilthunderstr = f"{bcgi.EstimatedThunderTime()/1200:.0f}"
        if bcgi.EstimatedIsRaining():
            self.stdscr.addstr(height-1, len(daystr)+2, f" {untilrainstr} ",curses.color_pair(self.STATSBAR_UNTILRAINCOLOR))
        else:
            self.stdscr.addstr(height-1, len(daystr)+2, f" {untilrainstr} ",curses.color_pair(self.STATSBAR_COLOR))
        if bcgi.EstimatedIsThundering():
            self.stdscr.addstr(height-1, len(daystr)+len(untilrainstr)+4, f" {untilthunderstr} ",curses.color_pair(self.STATSBAR_UNTILTHUNDERCOLOR))
        else:
            self.stdscr.addstr(height-1, len(daystr)+len(untilrainstr)+4, f" {untilthunderstr} ",curses.color_pair(self.STATSBAR_COLOR))

        statusbar_esttimeofday = bcgi.EstimatedTimeOfDay()
        if statusbar_esttimeofday >= bcgi.SLEEP:
            displaytime = (bcgi.DAY_FULLDAY-(bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY))/20
        else:
            displaytime = (bcgi.DAY_SLEEP-(bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY))/20
        #displaytimestr = '  {:0}:{:02} \U0001F4A4 '.format(floor(abs(displaytime)/60),floor(abs(displaytime)%60),esttimeofday,bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY)
        #displaytimestr = '\U0001F4A4\U0001F479{: 2}:{:02} \U0001F329 \U0001F327 '.format(floor(abs(displaytime)/60),floor(abs(displaytime)%60))
        displaytimestr = '{: 2}:{:02} '.format(floor(abs(displaytime)/60),floor(abs(displaytime)%60))
        
        rainthunderstr = "     "
#        rainthunderstr = "   \U0001F327  "
#        rainthunderstr = "\U0001F329  \U0001F327 "
        if bcgi.EstimatedIsThundering():
            rainthunderstr = "\U0001F329  \U0001F327 "
        elif bcgi.EstimatedIsRaining():
            rainthunderstr = "   \U0001F327  "

        monsterstr = "     "
#        monsterstr = "\U0001F319"
#        monsterstr = "\U0001F319 \U0001F479"
        if bcgi.EstimatedIsMonsters():
            monsterstr = "\U0001F319 \U0001F479"
        elif bcgi.EstimatedIsBedUsable():
           monsterstr = "\U0001F319    "

        self.stdscr.addstr(height-1, (width//2)-(len(displaytimestr)//2),displaytimestr,curses.color_pair(statusbar_esttimeofday))
        self.stdscr.addstr(height-1, ((width//2)-(len(displaytimestr)//2))-6,rainthunderstr, curses.color_pair(self.STATSBAR_COLOR))
        self.stdscr.addstr(height-1, ((width//2)+(len(displaytimestr)//2))+1,monsterstr, curses.color_pair(self.STATSBAR_COLOR))

    def RenderWindow(self,bcgi: BCGameInstance):
        (height,width) = self.statusbarwin.getmaxyx()

        if bcgi.LevelFileLastUpdate() != 0:
            leveltimestr = f"{datetime.fromtimestamp(bcgi.LevelFileLastUpdate()).strftime('%H:%M')} level.dat "
            testlastupdatetime = round(bcgi.LevelFileLastUpdate()+300-time())
            if testlastupdatetime < 0: 
                nextupdatestr = f"(next update is LATE)          "
            else:
                nextupdatestr = f"(next update in {timedelta(seconds=round(bcgi.LevelFileLastUpdate()+300-time()))})"
        else:
            leveltimestr = "NO level.dat"
            nextupdatestr = ""
        self.statusbarwin.addstr(0, 0, leveltimestr+nextupdatestr)

        gametimestr = f"Gametime {round(bcgi.EstimatedGameTime())} ({bcgi.GameTime()})"
        daytimestr = f"Daytime {bcgi.EstimatedDayTime()} % 24000 = {bcgi.EstimatedDayTime()%24000} ({bcgi.DayTime()})"
        self.statusbarwin.addstr(1, 0, gametimestr)
        self.statusbarwin.addstr(2, 0, daytimestr)


        rainweather = bcgi.EstimatedRainTime()
        if rainweather <= 0:
            rainweatherstr = f"Rain time({bcgi.EstimatedIsRaining()}:{bcgi.Raining()}): 0:00:00 ({bcgi.RainTime()})"
            untilrainstr = "  0"
        else:
            rainweatherstr = f"Rain time({bcgi.EstimatedIsRaining()}:{bcgi.Raining()}): {timedelta(seconds=round(rainweather/20))} ({bcgi.RainTime()})"
            untilrainstr = f"{rainweather/1200}"
        self.statusbarwin.addstr(4, 0, rainweatherstr)

        thunderweather = bcgi.EstimatedThunderTime()
        if thunderweather <= 0:
            thunderweatherstr = f"Thunder time({bcgi.EstimatedIsThundering()}:{bcgi.Thundering()}): 0:00:00 ({bcgi.ThunderTime()})"
        else:
            thunderweatherstr = f"Thunder time({bcgi.EstimatedIsThundering()}:{bcgi.Thundering()}): {timedelta(seconds=round(thunderweather/20))} ({bcgi.ThunderTime()})"

        self.statusbarwin.addstr(5, 0, thunderweatherstr)
    
        clearweather = bcgi.EstimatedClearWeatherTime()
        if clearweather < 0:
            clearweather = 0
        clearweatherstr = f"Clear weather time: {timedelta(seconds=round(clearweather))} ({bcgi.ClearWeatherTime()})"
        self.statusbarwin.addstr(6, 0, clearweatherstr)



        wanderingtraderidstr = f"Wander Trader ID: {bcgi.WanderingTraderID()}"
        self.statusbarwin.addstr(8, 0, wanderingtraderidstr)

        wanderingtraderdelay = bcgi.EstimatedWanderingTraderSpawnDelay()
        if wanderingtraderdelay < 0:
            wanderingtraderdelay = 0
        wanderingtraderstr = f"WanderTrader Spawn Delay: {timedelta(seconds=round(wanderingtraderdelay/20))} ({bcgi.WanderingTraderSpawnDelay()}:{bcgi.WanderingTraderSpawnChance()})"
        self.statusbarwin.addstr(9, 0, wanderingtraderstr)




        keysize=28
        self.statusbarwin.addstr(bcgi.DAWN-1, width-keysize, " 8:27 Dawn/Waking/Wandering ", curses.color_pair(bcgi.DAWN))
        self.statusbarwin.addstr(bcgi.WORKDAY-1, width-keysize, " 2:57 Workday               ", curses.color_pair(bcgi.WORKDAY))
        self.statusbarwin.addstr(bcgi.HAPPYHOUR-1, width-keysize, " 0:27 Happy-hour/Socializing", curses.color_pair(bcgi.HAPPYHOUR))
        self.statusbarwin.addstr(bcgi.TWILIGHT-1, width-keysize, " 0:00 Twilight/Sleeping Vill", curses.color_pair(bcgi.TWILIGHT))
        self.statusbarwin.addstr(bcgi.SLEEP-1, width-keysize, " 9:01 Beds are Usable       ", curses.color_pair(bcgi.SLEEP))
        self.statusbarwin.addstr(bcgi.MONSTERS-1, width-keysize, " 0:59 Night-time            ", curses.color_pair(bcgi.MONSTERS))
        self.statusbarwin.addstr(bcgi.NOMONSTERS-1, width-keysize, " 0:27 No New Monsters       ", curses.color_pair(bcgi.NOMONSTERS))
        self.statusbarwin.addstr(bcgi.NOSLEEP-1, width-keysize, " 0:00 Pre-dawn/Beds Unusable", curses.color_pair(bcgi.NOSLEEP))

#        self.statusbarwin.addstr(5, width-43, " 9:12- 9:01 Monsters Spawning (Rainy day)", curses.color_pair(bcgi.RAINMONSTERS))
#        self.statusbarwin.addstr(8, width-43, " 0:48- 0:27 No New Monsters (Rainy day)  ", curses.color_pair(bcgi.NORAINMONSTERS))

#        self.statusbarwin.addstr(0, width-43, "    0 -  2000 Dawn Wandering   10:27 - 8:47", curses.color_pair(bcgi.DAWN))
#        self.statusbarwin.addstr(1, width-43, " 2000 -  9000 Workday           8:47 - 2:57", curses.color_pair(bcgi.WORKDAY))
#        self.statusbarwin.addstr(2, width-43, " 9000 - 12000 Happyhour Social  2:57 - 0:27", curses.color_pair(bcgi.HAPPYHOUR))
#        self.statusbarwin.addstr(3, width-43, "12000 - 12542 Twilight          0:27 - 0:00", curses.color_pair(bcgi.TWILIGHT))
#        self.statusbarwin.addstr(4, width-43, "12542 - 12969 Able to Sleep     9:33 - 9:12", curses.color_pair(bcgi.SLEEP))
#        self.statusbarwin.addstr(6, width-43, "12969 - 13188 Rainy Monsters    9:12 - 9:01", curses.color_pair(bcgi.RAINMONSTERS))
#        self.statusbarwin.addstr(7, width-43, "13188 - 22812 Monsters Spawn    9:01 - 0:59", curses.color_pair(bcgi.MONSTERS))
#        self.statusbarwin.addstr(8, width-43, "22812 - 23031 No New Monsters   0:59 - 0:48", curses.color_pair(bcgi.NOMONSTERS))
#        self.statusbarwin.addstr(9, width-43, "23031 - 23460 No Rainy Monsters 0:48 - 0:27", curses.color_pair(bcgi.NORAINMONSTERS))
#        self.statusbarwin.addstr(10, width-43, "23460 - 24000 If Clear No Beds  0:27 - 0:00", curses.color_pair(bcgi.NOSLEEP))

        if self.esttimeofday != bcgi.EstimatedTimeOfDay():
            self.statusbarwin.addstr(self.esttimeofday-1, width-(keysize+6), "      ")
            self.esttimeofday = bcgi.EstimatedTimeOfDay()

        if self.esttimeofday >= bcgi.SLEEP:
            displaytime = (bcgi.DAY_FULLDAY-(bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY))/20
        else:
            displaytime = (bcgi.DAY_SLEEP-(bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY))/20
        displaytimestr = f"{floor(abs(displaytime)/60):>2}:{floor(abs(displaytime)%60):02} "
        self.statusbarwin.addstr(self.esttimeofday-1, width-(keysize+6), displaytimestr,curses.color_pair(self.esttimeofday))
       













#        negbeforenight = "-" if beforenight < 0 else ""
#        beforenightstr = '{}{:0}:{:02} '.format(negbeforenight,floor(abs(beforenight)/60),round(abs(beforenight)%60))
#
#        beforemonster = (13188-(bcgi.EstimatedDayTime()%24000))/20
#        negbeforemonster = "-" if beforemonster < 0 else ""
#        beforemonsterstr = '({}{:0}:{:02})'.format(negbeforemonster,floor(abs(beforemonster)/60),round(abs(beforemonster)%60))
#
#        centerstatusbarstr = beforenightstr + beforemonsterstr
#        self.stdscr.addstr(height-1, (width//2)-(len(centerstatusbarstr)//2),centerstatusbarstr)
#        self.stdscr.attroff(curses.color_pair(1))