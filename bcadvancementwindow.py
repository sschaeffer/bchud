#!/usr/bin/env python3
from re import T
from bchudconstants import BCHudConstants
from bcalladvancements import BCAdvancement
from bcgameinstance import BCGameInstance
from os import environ
import curses
from curses import panel

class BCAdvancementWindow():

    ADVANCEMENT_WINDOW_DOWN=1
    ADVANCEMENT_WINDOW_UP=-1

    ADVANCEMENT_WINDOW_ORIGINAL_ORDER=0
    ADVANCEMENT_WINDOW_REVERSE_ORIGINAL_ORDER=1
    ADVANCEMENT_WINDOW_SORTED_ORDER=2
    ADVANCEMENT_WINDOW_REVERSE_SORTED_ORDER=3
    ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER=4
    ADVANCEMENT_WINDOW_COMPLETED_LAST_ORDER=5

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self._stdscr:curses.stdscr = stdscr
        self._bcgi:BCGameInstance = bcgi
        self._advancement_category = BCHudConstants.BCMENU_BACAP_ADVANCEMENTS

        self._max_lines = 0
        self._current_advancement = 0
        self._top_advancement=0
        self._bottom_advancement=0

        self._top_criteria=0

        self._advancements_list=[]
        self._advancement_sort=self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER

        self._advancement_window = curses.newwin(0,0)
        self._advancement_panel = panel.new_panel(self._advancement_window)
        self._advancement_panel.hide()
        self._window_open = False

    def advancement_title(self,advancement_name):
        return self._bcgi.get_advancement(advancement_name)._title

    def advancement_completed(self,advancement_name):
        return self._bcgi.get_advancement(advancement_name)._completed

    def selected_advancement_list(self,advancement_category):

        self._advancement_category = advancement_category
        self._advancements_list.clear()

        self._current_advancement = 0
        self._top_advancement=0
        self._advancement_sort = self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER

        if(self._advancement_category == BCHudConstants.BCMENU_BACAP_ADVANCEMENTS):
            self._advancements_list = self._bcgi.bacap_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_MINING_ADVANCEMENTS):
            self._advancements_list = self._bcgi.mining_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_BUILDING_ADVANCEMENTS):
            self._advancements_list = self._bcgi.building_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_FARMING_ADVANCEMENTS):
            self._advancements_list = self._bcgi.farming_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_ANIMAL_ADVANCEMENTS):
            self._advancements_list = self._bcgi.animal_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_MONSTERS_ADVANCEMENTS):
            self._advancements_list = self._bcgi.monsters_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_WEAPONRY_ADVANCEMENTS):
            self._advancements_list = self._bcgi.weaponry_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_ADVENTURE_ADVANCEMENTS):
            self._advancements_list = self._bcgi.adventure_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_REDSTONE_ADVANCEMENTS):
            self._advancements_list = self._bcgi.redstone_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_ENCHANTING_ADVANCEMENTS):
            self._advancements_list = self._bcgi.enchanting_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_STATISTICS_ADVANCEMENTS):
            self._advancements_list = self._bcgi.statistics_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_NETHER_ADVANCEMENTS):
            self._advancements_list = self._bcgi.nether_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_POTIONS_ADVANCEMENTS):
            self._advancements_list = self._bcgi.potions_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_END_ADVANCEMENTS):
            self._advancements_list = self._bcgi.end_advancements_list().copy()
        elif(self._advancement_category == BCHudConstants.BCMENU_SUPER_CHALLENGES):
            self._advancements_list = self._bcgi.super_challenges_list().copy()

    def change_sort_order(self):
        if(self._advancement_sort == self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER):
            self.selected_advancement_list(self._advancement_category)
        elif(self._advancement_sort == self.ADVANCEMENT_WINDOW_REVERSE_ORIGINAL_ORDER):
            self._advancements_list = list(reversed(self._advancements_list))
        elif(self._advancement_sort == self.ADVANCEMENT_WINDOW_SORTED_ORDER):
            self._advancements_list.sort(key = self.advancement_title)
        elif(self._advancement_sort == self.ADVANCEMENT_WINDOW_REVERSE_SORTED_ORDER):
            self._advancements_list.sort(key = self.advancement_title, reverse=True)
        elif(self._advancement_sort == self.ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER):
            self._advancements_list.sort(key = self.advancement_completed, reverse=True)
        elif(self._advancement_sort == self.ADVANCEMENT_WINDOW_COMPLETED_LAST_ORDER):
            self._advancements_list. sort(key = self.advancement_completed)

    def render(self,height,width):

        if(height<BCHudConstants.MINIMUM_HEIGHT or width<BCHudConstants.MINIMUM_WIDTH):
            return

        self._window_open = True

        self._max_lines = height-2
        self._advancement_window.resize(height-2,width)
        self._advancement_window.clear()

        self._bottom_advancement = len(self._advancements_list)
        if self._bottom_advancement < 1:
            return

        for i in range(len(self._advancements_list))[self._top_advancement:self._top_advancement+self._max_lines]:
            j=i-self._top_advancement
            advancement_title:str = self.advancement_title(self._advancements_list[i])
            if j == self._current_advancement:
                if(self.advancement_completed(self._advancements_list[i]) == BCAdvancement.ADVANCEMENT_COMPLETED):
                    self._advancement_window.addstr(j,0,advancement_title,
                            curses.color_pair(BCHudConstants.COLOR_ADVANCEMENT_COMPLETE)|curses.A_REVERSE)
                else:
                    self._advancement_window.addstr(j,0,advancement_title, curses.A_REVERSE)
            else:
                if(self.advancement_completed(self._advancements_list[i]) == BCAdvancement.ADVANCEMENT_COMPLETED):
                    self._advancement_window.addstr(j,0,advancement_title,
                            curses.color_pair(BCHudConstants.COLOR_ADVANCEMENT_COMPLETE))
                else:
                    self._advancement_window.addstr(j,0,advancement_title)

        advancement:BCAdvancement = self._bcgi.get_advancement(self._advancements_list[self._top_advancement+self._current_advancement])
        criteria_length = len(advancement._criteria) 
        for i in range(criteria_length)[self._top_criteria:self._top_criteria+self._max_lines]:
            j=i-self._top_criteria
            if advancement._criteria[i] in advancement._finished:
                self._advancement_window.addstr(j,30,advancement._criteria[i],
                        curses.color_pair(BCHudConstants.COLOR_ADVANCEMENT_COMPLETE))
            else:
                self._advancement_window.addstr(j,30,advancement._criteria[i])

        self._advancement_panel.move(1,0)
        self._advancement_panel.show()
        panel.update_panels()
        self._stdscr.noutrefresh()


    def event_handler(self,input):

        if input in [curses.KEY_ENTER,ord('\n')]:
            pass
        if input in [curses.KEY_DOWN,ord('j')]:
            self.scroll_advancements(self.ADVANCEMENT_WINDOW_DOWN) 
        elif input in [curses.KEY_UP,ord('k')]:
            self.scroll_advancements(self.ADVANCEMENT_WINDOW_UP) 
        elif input == ord('c'):
            if self._advancement_sort == self.ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER:
                self._advancement_sort = self.ADVANCEMENT_WINDOW_COMPLETED_LAST_ORDER
            else:
                self._advancement_sort = self.ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER
            self.change_sort_order()
        elif input == ord('o'):
            if self._advancement_sort == self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER:
                self._advancement_sort = self.ADVANCEMENT_WINDOW_REVERSE_ORIGINAL_ORDER 
            else:
                self._advancement_sort = self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER 
            self.change_sort_order()
        elif input == ord('a'):
            if self._advancement_sort == self.ADVANCEMENT_WINDOW_SORTED_ORDER:
                self._advancement_sort = self.ADVANCEMENT_WINDOW_REVERSE_SORTED_ORDER
            else:
                self._advancement_sort = self.ADVANCEMENT_WINDOW_SORTED_ORDER
            self.change_sort_order()

    def scroll_advancements(self, direction):
        next_line = self._current_advancement + direction
        if (direction == self.ADVANCEMENT_WINDOW_UP) and (self._top_advancement > 0 and self._current_advancement == 0):
            self._top_advancement += direction
        elif ((direction == self.ADVANCEMENT_WINDOW_DOWN) and (next_line == self._max_lines) and
                (self._top_advancement + self._max_lines < self._bottom_advancement)):
            self._top_advancement += direction
        elif (direction == self.ADVANCEMENT_WINDOW_UP) and (self._top_advancement > 0 or self._current_advancement > 0):
            self._current_advancement = next_line
        elif ((direction == self.ADVANCEMENT_WINDOW_DOWN) and (next_line < self._max_lines) and 
                (self._top_advancement + next_line < self._bottom_advancement)):
            self._current_advancement = next_line

    def close(self):
        self._window_open = False
        self._advancement_panel.hide()

    def is_open(self):
        return(self._window_open)

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    bcgi.update_game_info()

    BCHudConstants.curses_setup(stdscr)
    bc_advancement_window = BCAdvancementWindow(stdscr,bcgi)
    bc_advancement_window.selected_advancement_list(BCHudConstants.BCMENU_BACAP_ADVANCEMENTS)

    try:
        pass
        keyboardinput = 0
        while keyboardinput != ord("q"): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)

            bc_advancement_window.event_handler(keyboardinput)
            bc_advancement_window.render(height,width)
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