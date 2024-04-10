#!/usr/bin/env python3
from bchudconstants import BCHudConstants
from bcgameinstance import BCGameInstance

from os import environ
import curses
from curses import panel
from datetime import datetime, timedelta
from time import time
from math import floor



class BCDebugWindow():

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance,update_time=1.0):
        self._stdscr:curses.stdscr = stdscr
        self._bcgi:BCGameInstance = bcgi

        self._debug_window = curses.newwin(0,0)
        self._debug_panel = panel.new_panel(self._debug_window)
        self._debug_panel.hide()

        self._last_update_time = 0.0
        self._update_time = update_time
        self._needs_update = True

        self._level_file_difference=0.0
        self._level_file_last_update=0.0

    def render(self,height,width):

        if(height<BCHudConstants.MINIMUM_HEIGHT or width<BCHudConstants.MINIMUM_WIDTH):
            return
        if self._needs_update == False:
            return
        if time() < self._last_update_time + self._update_time:
            return

        self._debug_window.resize(height-2,width)
        self._debug_window.clear()

        level_file_last_update = self._bcgi.level_file_last_update()
        if level_file_last_update != 0:
            if self._level_file_last_update == 0:
                self._level_file_last_update = level_file_last_update
            if self._level_file_last_update != level_file_last_update:
                self._level_file_difference = self._level_file_last_update+300-level_file_last_update
                self._level_file_last_update = level_file_last_update
            level_last_update_string = f"{datetime.fromtimestamp(level_file_last_update).strftime('%H:%M:%S')} level.dat "
            level_file_next_update = round(self._bcgi.level_file_last_update()+300-time())
            if level_file_next_update < 0:
                level_file_next_update_string = f"(Update LATE:{level_file_next_update})"
            else:
                if self._level_file_difference>=0:
                    level_file_next_update_string = f"(Update {timedelta(seconds=level_file_next_update)}+{self._level_file_difference:0.4f})"
                else:
                    level_file_next_update_string = f"(Update {timedelta(seconds=level_file_next_update)}{self._level_file_difference:0.4f})"
        else:
            level_last_update_string = "NO level.dat"
            level_file_next_update_string = ""
        self._debug_window.addstr(0, 0, level_last_update_string+level_file_next_update_string)

        estimated_game_time = round(self._bcgi.estimated_game_time()/20)
        estimated_game_time_string = f" {estimated_game_time//86400}:{(estimated_game_time%86400)//3600:02}:{(estimated_game_time%3600)//60:02}:{(estimated_game_time%60):02}"
        game_time = f"Game time{estimated_game_time_string} {round(self._bcgi.estimated_game_time())} ({self._bcgi.game_time()})"
        self._debug_window.addstr(1, 0, game_time)

        estimated_day_time = (BCHudConstants.DAY_FULLDAY-(self._bcgi.estimated_day_time()%BCHudConstants.DAY_FULLDAY))/20
        day_time_string = '{:02}:{:02}'.format(floor(abs(estimated_day_time)/60),floor(abs(estimated_day_time)%60))
        day_time = f"Day time  {day_time_string} {self._bcgi.estimated_day_time()%24000} {self._bcgi.estimated_day_time()} ({self._bcgi.day_time()})"
        self._debug_window.addstr(2, 0, day_time)

        rain_time = self._bcgi.estimated_rain_time()
        if rain_time <= 0:
            rain_time_string = f"Rain time({self._bcgi.estimated_is_raining()}:{self._bcgi.raining()}):    0:00:00 ({self._bcgi.rain_time()})"
        else:
            rain_time_string = f"Rain time({self._bcgi.estimated_is_raining()}:{self._bcgi.raining()}):    {timedelta(seconds=round(rain_time/20))} ({self._bcgi.rain_time()})"
        self._debug_window.addstr(4, 0, rain_time_string)

        thunder_time = self._bcgi.estimated_thunder_time()
        if thunder_time <= 0:
            thunder_time_string = f"Thunder time({self._bcgi.estimated_is_thundering()}:{self._bcgi.thundering()}): 0:00:00 ({self._bcgi.thunder_time()})"
        else:
            thunder_time_string = f"Thunder time({self._bcgi.estimated_is_thundering()}:{self._bcgi.thundering()}): {timedelta(seconds=round(thunder_time/20))} ({self._bcgi.thunder_time()})"
        self._debug_window.addstr(5, 0, thunder_time_string)

        clear_weather = self._bcgi.estimated_clear_weather_time()
        if clear_weather < 0:
            clear_weather = 0
        clear_weather_string = f"Clear weather time: {timedelta(seconds=round(clear_weather))} ({self._bcgi.clear_weather_time()})"
        self._debug_window.addstr(6, 0, clear_weather_string)

        wandering_trader_delay = self._bcgi.estimated_wandering_trader_spawn_delay()
        if wandering_trader_delay < 0:
            wandering_trader_delay = 0
        wandering_trader_string = f"WanderTrader Spawn Delay: {timedelta(seconds=round(wandering_trader_delay/20))} ({self._bcgi.wandering_trader_spawn_delay()}:{self._bcgi.wandering_trader_spawn_chance()})"
        self._debug_window.addstr(9, 0, wandering_trader_string)

        wandering_trader_id_string = f"Wander Trader ID: {self._bcgi.wandering_trader_id()}"
        self._debug_window.addstr(8, 0, wandering_trader_id_string)

        keysize=28
        self._debug_window.addstr(BCHudConstants.COLOR_DAWN-BCHudConstants.COLOR_DAWN, width-keysize, " 8:27 Dawn/Waking/Wandering ", curses.color_pair(BCHudConstants.COLOR_DAWN))
        self._debug_window.addstr(BCHudConstants.COLOR_WORKDAY-BCHudConstants.COLOR_DAWN, width-keysize, " 2:57 Workday               ", curses.color_pair(BCHudConstants.COLOR_WORKDAY))
        self._debug_window.addstr(BCHudConstants.COLOR_HAPPYHOUR-BCHudConstants.COLOR_DAWN, width-keysize, " 0:27 Happy-hour/Socializing", curses.color_pair(BCHudConstants.COLOR_HAPPYHOUR))
        self._debug_window.addstr(BCHudConstants.COLOR_TWILIGHT-BCHudConstants.COLOR_DAWN, width-keysize, " 0:00 Twilight/Sleeping Vill", curses.color_pair(BCHudConstants.COLOR_TWILIGHT))
        self._debug_window.addstr(BCHudConstants.COLOR_SLEEP-BCHudConstants.COLOR_DAWN, width-keysize, " 9:01 Beds are Usable       ", curses.color_pair(BCHudConstants.COLOR_SLEEP))
        self._debug_window.addstr(BCHudConstants.COLOR_MONSTERS-BCHudConstants.COLOR_DAWN, width-keysize, " 0:59 Night-time            ", curses.color_pair(BCHudConstants.COLOR_MONSTERS))   
        self._debug_window.addstr(BCHudConstants.COLOR_NO_MONSTERS-BCHudConstants.COLOR_DAWN, width-keysize, " 0:27 No New Monsters       ", curses.color_pair(BCHudConstants.COLOR_NO_MONSTERS))
        self._debug_window.addstr(BCHudConstants.COLOR_NO_SLEEP-BCHudConstants.COLOR_DAWN, width-keysize, " 0:00 Pre-dawn/Beds Unusable", curses.color_pair(BCHudConstants.COLOR_NO_SLEEP))

        if self._bcgi.estimated_time_of_day() >= BCHudConstants.COLOR_SLEEP:
            day_time = (BCHudConstants.DAY_FULLDAY-(self._bcgi.estimated_day_time()%BCHudConstants.DAY_FULLDAY))/20
        else:
            day_time = (BCHudConstants.DAY_SLEEP-(self._bcgi.estimated_day_time()%BCHudConstants.DAY_FULLDAY))/20
        day_time_string = f"{floor(abs(day_time)/60):>2}:{floor(abs(day_time)%60):02} "
        self._debug_window.addstr(self._bcgi.estimated_time_of_day()-BCHudConstants.COLOR_DAWN, width-(keysize+6),day_time_string,curses.color_pair(self._bcgi.estimated_time_of_day()))

        self._debug_panel.move(1,0)
        self._debug_panel.show()
        self._last_update_time = time()

    def close(self):
        self._debug_panel.hide()

    def event_handler(self,input):
        self._display_text = f"Input {input}"

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    bc_debug_window = BCDebugWindow(stdscr,bcgi)
    BCHudConstants.curses_setup(stdscr)

    try:
        pass
        keyboardinput = 0
        while keyboardinput != ord("q"): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)
            bcgi.update_game_info()

            bc_debug_window.event_handler(keyboardinput)
            bc_debug_window.render(height,width)
 
            panel.update_panels()
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