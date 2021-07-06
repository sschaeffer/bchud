#!/usr/bin/python3
from bcgameinstance import BCGameInstance
from bchudconstants import BCHudConstants

import curses
from curses import panel
from os import environ

class BCMenuBar():

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self.stdscr = stdscr 
        self.bcgi = bcgi
        self.height = 0
        self.width = 0
        self.bchud_menu_window = curses.newwin(0,0)
        self.bchud_menu_panel = panel.new_panel(self.bchud_menu_window)
        self.bchud_menu_panel.hide()

    def RenderBCHudMenu(self):
        self.bchud_menu_window.resize(self.height-2,26)
        self.bchud_menu_window.border()
        self.bchud_menu_window.addstr(1,1,"All Advancements")
        self.bchud_menu_window.addstr(2,0,"\u251C\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524")
        self.bchud_menu_window.addstr(3,1,"Bacap Advancements")
        self.bchud_menu_window.addstr(4,1,"Mining Advancements")
        self.bchud_menu_window.addstr(5,1,"Building Advancements")
        self.bchud_menu_window.addstr(6,1,"Farming Advancements")
        self.bchud_menu_window.addstr(7,1,"Animal Advancements")
        self.bchud_menu_window.addstr(8,1,"Monsters Advancements")
        self.bchud_menu_window.addstr(9,1,"Weaponry Advancements")
        self.bchud_menu_window.addstr(10,1,"Adventure Advancements")
        self.bchud_menu_window.addstr(11,1,"Redstone Advancements")
        self.bchud_menu_window.addstr(12,1,"Enchanting Advancements")
        self.bchud_menu_window.addstr(13,1,"Statistics Advancements")
        self.bchud_menu_window.addstr(14,1,"Nether Advancements")
        self.bchud_menu_window.addstr(15,1,"Potions Advancements")
        self.bchud_menu_window.addstr(16,1,"End Advancements")
        self.bchud_menu_window.addstr(17,1,"Super Challenges")
#        self.bchud_menu_window.addstr(18,0,"\u251C\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524")
#        self.bchud_menu_window.addstr(19,0,"Quit")
        self.bchud_menu_panel.move(1,1)
        self.bchud_menu_panel.show()

    def Render(self,height,width,focus):
#        self.stdscr.addstr(0,0,f"BC HUD {bcgi._servername}:{self.bcgi._worldname}", curses.A_BOLD | curses.A_REVERSE)
#        self.stdscr.addstr(0,0,f"BC HUD {self.bcgi.AllAdvancementsCount()}", curses.A_BOLD | curses.A_REVERSE)
        self.height = height
        self.width = width
        self.stdscr.chgat(-1, curses.A_REVERSE)
        if focus == BCHudConstants.FOCUS_BCHUD_MENU:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.color_pair(BCHudConstants.MENUBAR_SELECTED_COLOR)|curses.A_BOLD)
            self.RenderBCHudMenu()
        else:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.bchud_menu_panel.hide()
        panel.update_panels()
        self.stdscr.noutrefresh()

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    BCHudConstants.cursessetup(stdscr)
    bcmenubar = BCMenuBar(stdscr,bcgi)

    try:
        focus = BCHudConstants.FOCUS_STARTSCREEN
        input = 0
        while True:
            (height,width) = stdscr.getmaxyx()
            if input in [curses.KEY_ENTER,ord('\n')]:
                focus = BCHudConstants.FOCUS_BCHUD_MENU
            elif input == 27:
                focus = BCHudConstants.FOCUS_STARTSCREEN
            bcmenubar.Render(height,width,focus)
            curses.doupdate()
            input = stdscr.getch()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

if __name__ == "__main__":
    (minecraftdir,servername,worldname) = BCHudConstants.initserver()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, servername, worldname)