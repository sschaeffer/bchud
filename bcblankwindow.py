#!/usr/bin/env python3
from bchudconstants import BCHudConstants
from bcgameinstance import BCGameInstance
from os import environ
import curses
from curses import panel

class BCBlankWindow():

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self._stdscr:curses.stdscr = stdscr
        self._bcgi:BCGameInstance = bcgi

        self._display_text = ""

        self._blank_window = curses.newwin(0,0)
        self._blank_panel = panel.new_panel(self._blank_window)
        self._blank_panel.hide()

    def render(self,height,width):

        if(height<BCHudConstants.MINIMUM_HEIGHT or width<BCHudConstants.MINIMUM_WIDTH):
            return
        self._max_lines = height-2
        self._blank_window.resize(height-2,width)
        self._blank_window.clear()

        self._blank_window.addstr((height//2)-1,(width-len(self._display_text))//2,self._display_text)

        self._blank_panel.move(1,0)
        self._blank_panel.show()

    def hide(self):
        self._blank_panel.hide()

    def event_handler(self,input):
        self._display_text = f"Input {input}"

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    bcgi.update_game_info()

    BCHudConstants.curses_setup(stdscr)
    bc_advancement_window = BCBlankWindow(stdscr,bcgi)

    try:
        pass
        keyboardinput = 0
        while keyboardinput != ord("q"): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)

            bc_advancement_window.event_handler(keyboardinput)
            bc_advancement_window.render(height,width)
 
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