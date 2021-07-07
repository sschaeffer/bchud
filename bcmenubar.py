#!/usr/bin/python3
from bcgameinstance import BCGameInstance
from bchudconstants import BCHudConstants

import curses
from curses import panel
from os import environ

class BCMenuBar():

    bchud_menu_items = ["Bacap Advancements",
                        "Mining Advancments",
                        "Building Advancements",
                        "Farming Advancements",
                        "Animal Advancements",
                        "Monsters Advancements",
                        "Weaponry Advancements",
                        "Adventure Advancements",
                        "Redstone Advancements",
                        "Enchanting Advancements",
                        "Statistics Advancements",
                        "Nether Advancements",
                        "Potions Advancements",
                        "End Advancements",
                        "Super Challenges" ]

    users_menu_items =["stephenschaeffer",
                        "Sebbac80",
                        "Noodle_Hair",
                        "Lilly__Bug",
                        "Yee_L",
                        "diggles",
                        "LastStay"]

    level_menu_items =["Day/Night Cycle",
                        "Level Info",
                        "BCLogs",
                        "latest.log",
                        "Timing",
                        "Change Server/World"]

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self.stdscr = stdscr 
        self.bcgi = bcgi

        self.totalheight = 0
        self.totalwidth = 0
        self.selected_menu = 0
        self.menu_selected_item = 0
        self.menu_selected_items_max = 0

        self.bchud_menu_window = curses.newwin(0,0)
        self.bchud_menu_panel = panel.new_panel(self.bchud_menu_window)
        self.bchud_menu_panel.hide()

        self.users_menu_window = curses.newwin(0,0)
        self.users_menu_panel = panel.new_panel(self.users_menu_window)
        self.users_menu_panel.hide()

        self.level_menu_window = curses.newwin(0,0)
        self.level_menu_panel = panel.new_panel(self.level_menu_window)
        self.level_menu_panel.hide()

    def RenderBCHudMenu(self):
        bchud_menu_width=27
        self.menu_selected_items_max = len(self.bchud_menu_items)+1
        self.bchud_menu_window.resize(len(self.bchud_menu_items)+4,bchud_menu_width)
        self.bchud_menu_window.border()
        if self.menu_selected_item == 1:
            self.bchud_menu_window.addstr(1,1,f" {'All Advancements':23} ", curses.A_REVERSE)
        else:
            self.bchud_menu_window.addstr(1,1,f" {'All Advancements':23} ")
        self.bchud_menu_window.addstr(2,0,"\u251C")
        for i in range (1,bchud_menu_width-1):
            self.bchud_menu_window.addstr(2,i,"\u2500")
        self.bchud_menu_window.addstr(2,bchud_menu_width-1,"\u2524")
        for idx, i in enumerate(self.bchud_menu_items):
            if self.menu_selected_item == idx+2:
                self.bchud_menu_window.addstr(idx+3,1,f" {i:23} ", curses.A_REVERSE)
            else:
                self.bchud_menu_window.addstr(idx+3,1,f" {i:23} ")

        self.bchud_menu_panel.move(1,1)
        self.bchud_menu_panel.show()

    def RenderUsersMenu(self):
        users_menu_width=20
        self.menu_selected_items_max = len(self.users_menu_items)
        self.users_menu_window.resize(len(self.users_menu_items)+2,users_menu_width)
        self.users_menu_window.border()
        for idx, i in enumerate(self.users_menu_items):
            if self.menu_selected_item == idx+1:
                self.users_menu_window.addstr(idx+1,1,f" {i:16} ", curses.A_REVERSE)
            else:
                self.users_menu_window.addstr(idx+1,1,f" {i:16} ")

        self.users_menu_panel.move(1,7)
        self.users_menu_panel.show()

    def RenderLevelMenu(self):
        level_menu_width=23
        self.menu_selected_items_max = len(self.level_menu_items)
        self.level_menu_window.resize(len(self.level_menu_items)+2,level_menu_width)
        self.level_menu_window.border()
        for idx, i in enumerate(self.level_menu_items):
            if self.menu_selected_item == idx+1:
                self.level_menu_window.addstr(idx+1,1,f" {i:19} ", curses.A_REVERSE)
            else:
                self.level_menu_window.addstr(idx+1,1,f" {i:19} ")

        self.level_menu_panel.move(1,14)
        self.level_menu_panel.show()

    def Render(self,height,width):
#        self.stdscr.addstr(0,0,f"BC HUD {bcgi._servername}:{self.bcgi._worldname}", curses.A_BOLD | curses.A_REVERSE)
#        self.stdscr.addstr(0,0,f"BC HUD {self.bcgi.AllAdvancementsCount()}", curses.A_BOLD | curses.A_REVERSE)
        self.height = height
        self.width = width
        self.stdscr.chgat(-1, curses.A_REVERSE)
        if self.selected_menu == 1:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.color_pair(BCHudConstants.MENUBAR_SELECTED_COLOR)|curses.A_BOLD)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.RenderBCHudMenu()
        elif self.selected_menu == 2:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.color_pair(BCHudConstants.MENUBAR_SELECTED_COLOR)|curses.A_BOLD)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.bchud_menu_panel.hide()
            self.RenderUsersMenu()
        elif self.selected_menu == 3:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.color_pair(BCHudConstants.MENUBAR_SELECTED_COLOR)|curses.A_BOLD)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()
            self.RenderLevelMenu()
        elif self.selected_menu == 3:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()
        elif self.selected_menu == 4:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.color_pair(BCHudConstants.MENUBAR_SELECTED_COLOR)|curses.A_BOLD)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()
        elif self.selected_menu == 5:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.color_pair(BCHudConstants.MENUBAR_SELECTED_COLOR)|curses.A_BOLD)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()
        else:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()

        panel.update_panels()
        self.stdscr.noutrefresh()

    def EventHandler(self,input):
        if input == 0:
            self.selected_menu = 1
            self.menu_selected_item = 1
            self.menu_selected_items_max = len(self.bchud_menu_items)+1
        elif input in [27,ord('\t')]:
            self.selected_menu = 0
            self.menu_selected_item = 1
            return 0
        elif input in [curses.KEY_ENTER,ord('\n')]:
            result = 0 
            if self.selected_menu==5:
                result = -1
            self.selected_menu = 0
            self.menu_selected_item = 1
            return result
        elif input in [curses.KEY_DOWN,ord('j')] and self.menu_selected_item<self.menu_selected_items_max:
            self.menu_selected_item = self.menu_selected_item+1
        elif input in [curses.KEY_UP,ord('k')] and self.menu_selected_item>1:
            self.menu_selected_item = self.menu_selected_item-1
        elif input in [curses.KEY_RIGHT,ord('l')] and self.selected_menu<5:
            self.selected_menu = self.selected_menu+1
            self.menu_selected_item = 1
        elif input in [curses.KEY_LEFT,ord('h')] and self.selected_menu>1:
            self.selected_menu = self.selected_menu-1
            self.menu_selected_item = 1
        return 1

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    BCHudConstants.cursessetup(stdscr)
    bcmenubar = BCMenuBar(stdscr,bcgi)

    try:
        menuopen = 0
        input = 0
        while input != ord("q") and menuopen != -1: 
            (height,width) = stdscr.getmaxyx()
            if menuopen != 1 and input == ord('\t'):
                menuopen = 1 
                menuopen = bcmenubar.EventHandler(0) 
            elif menuopen == 1:
                menuopen = bcmenubar.EventHandler(input) 

            bcmenubar.Render(height,width)
            curses.doupdate()
            if menuopen != -1:
                input = stdscr.getch()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

if __name__ == "__main__":
    (minecraftdir,servername,worldname) = BCHudConstants.initserver()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, servername, worldname)