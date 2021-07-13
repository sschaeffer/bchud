#!/usr/bin/env python3
from bchudconstants import BCHudConstants
from bcgameinstance import BCGameInstance

from os import environ
import curses
from curses import panel
from datetime import datetime, timedelta
from time import time



class BCDebugWindow():

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self._stdscr:curses.stdscr = stdscr
        self._bcgi:BCGameInstance = bcgi


        self._debug_window = curses.newwin(0,0)
        self._debug_panel = panel.new_panel(self._debug_window)
        self._debug_panel.hide()

    def render(self,height,width):

        if(height<BCHudConstants.MINIMUM_HEIGHT or width<BCHudConstants.MINIMUM_WIDTH):
            return
        self._max_lines = height-2
        self._debug_window.resize(height-2,width)
        self._debug_window.clear()

        if self._bcgi.level_file_last_update() != 0:
            level_last_update = f"{datetime.fromtimestamp(self._bcgi.level_file_last_update()).strftime('%H:%M')} level.dat "
            test_for_next_update = round(self._bcgi.level_file_last_update()+300-time())
            if test_for_next_update < 0: 
                next_update = f"(next update is LATE)          "
            else:
                next_update = f"(next update in {timedelta(seconds=round(self._bcgi.level_file_last_update()+300-time()))})"
        else:
            level_last_update = "NO level.dat"
            next_update = ""
        self._debug_window.addstr(0, 0, level_last_update+next_update)
#
#        gametimestr = f"Gametime {round(bcgi.EstimatedGameTime())} ({bcgi.GameTime()})"
#        daytimestr = f"Daytime {bcgi.EstimatedDayTime()} % 24000 = {bcgi.EstimatedDayTime()%24000} ({bcgi.DayTime()})"
#        self.statusbarwin.addstr(1, 0, gametimestr)
#        self.statusbarwin.addstr(2, 0, daytimestr)
#
#
#        rainweather = bcgi.EstimatedRainTime()
#        if rainweather <= 0:
#            rainweatherstr = f"Rain time({bcgi.EstimatedIsRaining()}:{bcgi.Raining()}): 0:00:00 ({bcgi.RainTime()})"
#            untilrainstr = "  0"
#        else:
#            rainweatherstr = f"Rain time({bcgi.EstimatedIsRaining()}:{bcgi.Raining()}): {timedelta(seconds=round(rainweather/20))} ({bcgi.RainTime()})"
#            untilrainstr = f"{rainweather/1200}"
#        self.statusbarwin.addstr(4, 0, rainweatherstr)
#
#        thunderweather = bcgi.EstimatedThunderTime()
#        if thunderweather <= 0:
#            thunderweatherstr = f"Thunder time({bcgi.EstimatedIsThundering()}:{bcgi.Thundering()}): 0:00:00 ({bcgi.ThunderTime()})"
#        else:
#            thunderweatherstr = f"Thunder time({bcgi.EstimatedIsThundering()}:{bcgi.Thundering()}): {timedelta(seconds=round(thunderweather/20))} ({bcgi.ThunderTime()})"
#
#        self.statusbarwin.addstr(5, 0, thunderweatherstr)
#    
#        clearweather = bcgi.EstimatedClearWeatherTime()
#        if clearweather < 0:
#            clearweather = 0
#        clearweatherstr = f"Clear weather time: {timedelta(seconds=round(clearweather))} ({bcgi.ClearWeatherTime()})"
#        self.statusbarwin.addstr(6, 0, clearweatherstr)
#
#
#
#        wanderingtraderidstr = f"Wander Trader ID: {bcgi.WanderingTraderID()}"
#        self.statusbarwin.addstr(8, 0, wanderingtraderidstr)
#
#        wanderingtraderdelay = bcgi.EstimatedWanderingTraderSpawnDelay()
#        if wanderingtraderdelay < 0:
#            wanderingtraderdelay = 0
#        wanderingtraderstr = f"WanderTrader Spawn Delay: {timedelta(seconds=round(wanderingtraderdelay/20))} ({bcgi.WanderingTraderSpawnDelay()}:{bcgi.WanderingTraderSpawnChance()})"
#        self.statusbarwin.addstr(9, 0, wanderingtraderstr)
#
#
#
#
#        keysize=28
#        self.statusbarwin.addstr(bcgi.DAWN-1, width-keysize, " 8:27 Dawn/Waking/Wandering ", curses.color_pair(bcgi.DAWN))
#        self.statusbarwin.addstr(bcgi.WORKDAY-1, width-keysize, " 2:57 Workday               ", curses.color_pair(bcgi.WORKDAY))
#        self.statusbarwin.addstr(bcgi.HAPPYHOUR-1, width-keysize, " 0:27 Happy-hour/Socializing", curses.color_pair(bcgi.HAPPYHOUR))
#        self.statusbarwin.addstr(bcgi.TWILIGHT-1, width-keysize, " 0:00 Twilight/Sleeping Vill", curses.color_pair(bcgi.TWILIGHT))
#        self.statusbarwin.addstr(bcgi.SLEEP-1, width-keysize, " 9:01 Beds are Usable       ", curses.color_pair(bcgi.SLEEP))
#        self.statusbarwin.addstr(bcgi.MONSTERS-1, width-keysize, " 0:59 Night-time            ", curses.color_pair(bcgi.MONSTERS))
#        self.statusbarwin.addstr(bcgi.NOMONSTERS-1, width-keysize, " 0:27 No New Monsters       ", curses.color_pair(bcgi.NOMONSTERS))
#        self.statusbarwin.addstr(bcgi.NOSLEEP-1, width-keysize, " 0:00 Pre-dawn/Beds Unusable", curses.color_pair(bcgi.NOSLEEP))
#
##        self.statusbarwin.addstr(5, width-43, " 9:12- 9:01 Monsters Spawning (Rainy day)", curses.color_pair(bcgi.RAINMONSTERS))
##        self.statusbarwin.addstr(8, width-43, " 0:48- 0:27 No New Monsters (Rainy day)  ", curses.color_pair(bcgi.NORAINMONSTERS))

##        self.statusbarwin.addstr(0, width-43, "    0 -  2000 Dawn Wandering   10:27 - 8:47", curses.color_pair(bcgi.DAWN))
##        self.statusbarwin.addstr(1, width-43, " 2000 -  9000 Workday           8:47 - 2:57", curses.color_pair(bcgi.WORKDAY))
##        self.statusbarwin.addstr(2, width-43, " 9000 - 12000 Happyhour Social  2:57 - 0:27", curses.color_pair(bcgi.HAPPYHOUR))
##        self.statusbarwin.addstr(3, width-43, "12000 - 12542 Twilight          0:27 - 0:00", curses.color_pair(bcgi.TWILIGHT))
##        self.statusbarwin.addstr(4, width-43, "12542 - 12969 Able to Sleep     9:33 - 9:12", curses.color_pair(bcgi.SLEEP))
##        self.statusbarwin.addstr(6, width-43, "12969 - 13188 Rainy Monsters    9:12 - 9:01", curses.color_pair(bcgi.RAINMONSTERS))
##        self.statusbarwin.addstr(7, width-43, "13188 - 22812 Monsters Spawn    9:01 - 0:59", curses.color_pair(bcgi.MONSTERS))
##        self.statusbarwin.addstr(8, width-43, "22812 - 23031 No New Monsters   0:59 - 0:48", curses.color_pair(bcgi.NOMONSTERS))
##        self.statusbarwin.addstr(9, width-43, "23031 - 23460 No Rainy Monsters 0:48 - 0:27", curses.color_pair(bcgi.NORAINMONSTERS))
##        self.statusbarwin.addstr(10, width-43, "23460 - 24000 If Clear No Beds  0:27 - 0:00", curses.color_pair(bcgi.NOSLEEP))

#        if self.esttimeofday != bcgi.EstimatedTimeOfDay():
#            self.statusbarwin.addstr(self.esttimeofday-1, width-(keysize+6), "      ")
#            self.esttimeofday = bcgi.EstimatedTimeOfDay()
#
#        if self.esttimeofday >= bcgi.SLEEP:
#            displaytime = (bcgi.DAY_FULLDAY-(bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY))/20
#        else:
#            displaytime = (bcgi.DAY_SLEEP-(bcgi.EstimatedDayTime()%bcgi.DAY_FULLDAY))/20
#        displaytimestr = f"{floor(abs(displaytime)/60):>2}:{floor(abs(displaytime)%60):02} "
#        self.statusbarwin.addstr(self.esttimeofday-1, width-(keysize+6), displaytimestr,curses.color_pair(self.esttimeofday))
#       
#
##        negbeforenight = "-" if beforenight < 0 else ""
##        beforenightstr = '{}{:0}:{:02} '.format(negbeforenight,floor(abs(beforenight)/60),round(abs(beforenight)%60))
##
##        beforemonster = (13188-(bcgi.EstimatedDayTime()%24000))/20
##        negbeforemonster = "-" if beforemonster < 0 else ""
##        beforemonsterstr = '({}{:0}:{:02})'.format(negbeforemonster,floor(abs(beforemonster)/60),round(abs(beforemonster)%60))
##
##        centerstatusbarstr = beforenightstr + beforemonsterstr
##        self.stdscr.addstr(height-1, (width//2)-(len(centerstatusbarstr)//2),centerstatusbarstr)
##        self.stdscr.attroff(curses.color_pair(1))





        self._debug_panel.move(1,0)
        self._debug_panel.show()

    def hide(self):
        self._debug_panel.hide()

    def event_handler(self,input):
        self._display_text = f"Input {input}"

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    bcgi.update_game_info()

    BCHudConstants.curses_setup(stdscr)
    bc_debug_window = BCDebugWindow(stdscr,bcgi)

    try:
        pass
        keyboardinput = 0
        while keyboardinput != ord("q"): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)

            bc_debug_window.event_handler(keyboardinput)
            bc_debug_window.render(height,width)
 
            panel.update_panels()
            stdscr.noutrefresh()
            curses.doupdate()
            keyboardinput = stdscr.getch()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == "__main__":
    (minecraftdir,servername,worldname) = BCHudConstants.init_server()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, servername, worldname)