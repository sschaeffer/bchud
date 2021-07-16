#!/usr/bin/python3
from bchudconstants import BCHudConstants
from bcgameinstance import BCGameInstance
from bcmenubar import BCMenuBar
from bcstatusbar import BCStatusBar
from bcdebugwindow import BCDebugWindow
from bcadvancementwindow import BCAdvancementWindow

from os import environ
import curses
from curses import panel

def main(stdscr:curses.window, minecraftdir, worldname, servername):

    bcgi = BCGameInstance(minecraftdir, worldname, servername)
    bcmenubar = BCMenuBar(stdscr,bcgi)
    bcstatusbar = BCStatusBar(stdscr,bcgi)
    bcdebugwindow = BCDebugWindow(stdscr,bcgi)
    bcadvancementwindow = BCAdvancementWindow(stdscr,bcgi)

    open_window = 0
    bcmenubar.override_result(BCHudConstants.BCMENU_LEVEL_INFO)

    BCHudConstants.curses_setup(stdscr)

    bcgi.set_auto_backup(True)
    bcgi.set_auto_backup_delay(1200.0)

    try:
        keyboardinput = 0 
        while keyboardinput != ord("q") and not bcmenubar.exit(): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)
            bcgi.update_game_info()

            if bcmenubar.is_open():
                bcmenubar.event_handler(keyboardinput)
            elif keyboardinput == ord('\t'):
                bcmenubar.open()
            elif bcadvancementwindow.is_open():
                bcadvancementwindow.event_handler(keyboardinput)

            if bcmenubar.result() != open_window:
                if open_window == BCHudConstants.BCMENU_LEVEL_INFO:
                    bcdebugwindow.close()
                elif open_window >= BCHudConstants.BCMENU_BACAP_ADVANCEMENTS and open_window <= BCHudConstants.BCMENU_SUPER_CHALLENGES:
                    bcadvancementwindow.close()
                open_window = bcmenubar.result()
                if open_window >= BCHudConstants.BCMENU_BACAP_ADVANCEMENTS and open_window <= BCHudConstants.BCMENU_SUPER_CHALLENGES:
                    bcadvancementwindow.selected_advancement_list(open_window)

            if open_window == BCHudConstants.BCMENU_LEVEL_INFO:
                bcdebugwindow.render(height,width)
            elif open_window >= BCHudConstants.BCMENU_BACAP_ADVANCEMENTS and open_window <= BCHudConstants.BCMENU_SUPER_CHALLENGES:
                bcadvancementwindow.render(height,width)

            bcstatusbar.render(height,width)
            bcmenubar.render(height,width)

#            stdscr.noutrefresh()
            panel.update_panels()
            curses.doupdate()
            if not bcmenubar.exit():
                keyboardinput = stdscr.getch()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == "__main__":
    (minecraftdir, worldname, servername) = BCHudConstants.init_server()
    environ.setdefault('ESCDELAY', '25')
#    curses.wrapper(main, minecraftdir, worldname, servername)
    curses.wrapper(main, minecraftdir, worldname, servername)