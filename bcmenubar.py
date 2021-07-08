#!/usr/bin/python3
from bcgameinstance import BCGameInstance
from bchudconstants import BCHudConstants

import curses
from curses import panel
from os import environ

class BCMenuBar():

    bchud_menu_items = [["Bacap Advancements",BCHudConstants.BCMENU_BACAP_ADVANCEMENTS],
                        ["Mining Advancments",BCHudConstants.BCMENU_MINING_ADVANCEMENTS],
                        ["Building Advancements",BCHudConstants.BCMENU_BUILDING_ADVANCEMENTS],
                        ["Farming Advancements",BCHudConstants.BCMENU_FARMING_ADVANCEMENTS],
                        ["Animal Advancements",BCHudConstants.BCMENU_ANIMAL_ADVANCEMENTS],
                        ["Monsters Advancements",BCHudConstants.BCMENU_MONSTERS_ADVANCEMENTS],
                        ["Weaponry Advancements",BCHudConstants.BCMENU_WEAPONRY_ADVANCEMENTS],
                        ["Adventure Advancements",BCHudConstants.BCMENU_ADVENTURE_ADVANCEMENTS],
                        ["Redstone Advancements",BCHudConstants.BCMENU_REDSTONE_ADVANCEMENTS],
                        ["Enchanting Advancements",BCHudConstants.BCMENU_ENCHANTING_ADVANCEMENTS],
                        ["Statistics Advancements",BCHudConstants.BCMENU_STATISTICS_ADVANCEMENTS],
                        ["Nether Advancements",BCHudConstants.BCMENU_NETHER_ADVANCEMENTS],
                        ["Potions Advancements",BCHudConstants.BCMENU_POTIONS_ADVANCEMENTS],
                        ["End Advancements",BCHudConstants.BCMENU_END_ADVANCEMENTS],
                        ["Super Challenges",BCHudConstants.BCMENU_SUPER_CHALLENGES]]

    users_menu_items =[["stephenschaeffer",BCHudConstants.BCMENU_USER1],
                       ["Sebbac80",BCHudConstants.BCMENU_USER2],
                       ["Noodle_Hair",BCHudConstants.BCMENU_USER3],
                       ["Lilly__Bug",BCHudConstants.BCMENU_USER4],
                       ["Yee_L",BCHudConstants.BCMENU_USER5],
                       ["diggles",BCHudConstants.BCMENU_USER6],
                       ["LastStay",BCHudConstants.BCMENU_USER7]]

    level_menu_items =[["Day/Night Cycle",BCHudConstants.BCMENU_DAY_NIGHT_CYCLE],
                       ["Level Info",BCHudConstants.BCMENU_LEVEL_INFO],
                       ["BCLogs",BCHudConstants.BCMENU_BCLOGS],
                       ["latest.log",BCHudConstants.BCMENU_LATEST_LOG],
                       ["Timing",BCHudConstants.BCMENU_TIMING],
                       ["Change Server/World",BCHudConstants.BCMENU_CHANGE_SERVER_WORLD]]

    MENUS_CLOSED=0
    BCHUD_MENU=FIRST_MENU_ITEM=1
    USERS_MENU=2
    LEVEL_MENU=3
    REFRESH_MENU=4
    QUIT_MENU=5

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self.stdscr = stdscr 
        self.bcgi = bcgi

        self.selected_menu = self.MENUS_CLOSED
        self._bcmenu_result = BCHudConstants.BCMENU_NOCHANGE

        self.totalheight = 0
        self.totalwidth = 0
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
                self.bchud_menu_window.addstr(idx+3,1,f" {i[0]:23} ", curses.A_REVERSE)
            else:
                self.bchud_menu_window.addstr(idx+3,1,f" {i[0]:23} ")

        self.bchud_menu_panel.move(1,1)
        self.bchud_menu_panel.show()

    def RenderUsersMenu(self):
        users_menu_width=20
        self.menu_selected_items_max = len(self.users_menu_items)
        self.users_menu_window.resize(len(self.users_menu_items)+2,users_menu_width)
        self.users_menu_window.border()
        for idx, i in enumerate(self.users_menu_items):
            if self.menu_selected_item == idx+1:
                self.users_menu_window.addstr(idx+1,1,f" {i[0]:16} ", curses.A_REVERSE)
            else:
                self.users_menu_window.addstr(idx+1,1,f" {i[0]:16} ")

        self.users_menu_panel.move(1,7)
        self.users_menu_panel.show()

    def RenderLevelMenu(self):
        level_menu_width=23
        self.menu_selected_items_max = len(self.level_menu_items)
        self.level_menu_window.resize(len(self.level_menu_items)+2,level_menu_width)
        self.level_menu_window.border()
        for idx, i in enumerate(self.level_menu_items):
            if self.menu_selected_item == idx+1:
                self.level_menu_window.addstr(idx+1,1,f" {i[0]:19} ", curses.A_REVERSE)
            else:
                self.level_menu_window.addstr(idx+1,1,f" {i[0]:19} ")

        self.level_menu_panel.move(1,14)
        self.level_menu_panel.show()


    def Render(self,height,width):
#        self.stdscr.addstr(0,0,f"BC HUD {bcgi._servername}:{self.bcgi._worldname}", curses.A_BOLD | curses.A_REVERSE)
#        self.stdscr.addstr(0,0,f"BC HUD {self.bcgi.AllAdvancementsCount()}", curses.A_BOLD | curses.A_REVERSE)
        self.height = height
        self.width = width
        self.stdscr.addstr(0,0," ", curses.A_REVERSE)
        self.stdscr.chgat(-1, curses.A_REVERSE)
        if self.selected_menu == self.BCHUD_MENU:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.RenderBCHudMenu()
        elif self.selected_menu == self.USERS_MENU:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.bchud_menu_panel.hide()
            self.RenderUsersMenu()
        elif self.selected_menu == self.LEVEL_MENU:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()
            self.RenderLevelMenu()
        elif self.selected_menu == self.REFRESH_MENU:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.A_REVERSE)
            self.level_menu_panel.hide()
            self.users_menu_panel.hide()
            self.bchud_menu_panel.hide()
        elif self.selected_menu == self.QUIT_MENU:
            self.stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self.stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self.stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-16,f" REFRESH ", curses.A_REVERSE)
            self.stdscr.addstr(0,self.width-7,f" QUIT ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
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

        if input in [27,ord('\t')]:
            self.selected_menu = self.MENUS_CLOSED
            self.menu_selected_item = self.FIRST_MENU_ITEM
            self._bcmenu_result = BCHudConstants.BCMENU_NOCHANGE

        elif input in [curses.KEY_ENTER,ord('\n')]:

            if self.selected_menu==self.BCHUD_MENU:
                if(self.menu_selected_item==self.FIRST_MENU_ITEM):
                    self._bcmenu_result = BCHudConstants.BCMENU_ALL_ADVANCEMENTS
                else:
                    self._bcmenu_result = self.bchud_menu_items[self.menu_selected_item-2][1] 

            if self.selected_menu==self.USERS_MENU:
                self._bcmenu_result = self.users_menu_items[self.menu_selected_item-1][1] 

            if self.selected_menu==self.LEVEL_MENU:
                self._bcmenu_result = self.level_menu_items[self.menu_selected_item-1][1] 

            if self.selected_menu==self.QUIT_MENU:
                self._bcmenu_result = BCHudConstants.BCMENU_EXIT

            if self.selected_menu==self.REFRESH_MENU:
                self._bcmenu_result = BCHudConstants.BCMENU_REFRESH

            self.selected_menu = self.MENUS_CLOSED
            self.menu_selected_item = self.FIRST_MENU_ITEM
            
        elif input in [curses.KEY_DOWN,ord('j')] and self.menu_selected_item<self.menu_selected_items_max:
            self.menu_selected_item = self.menu_selected_item+1
        elif input in [curses.KEY_UP,ord('k')] and self.menu_selected_item>1:
            self.menu_selected_item = self.menu_selected_item-1
        elif input in [curses.KEY_RIGHT,ord('l')] and self.selected_menu<self.QUIT_MENU:
            self.selected_menu = self.selected_menu+1
            self.menu_selected_item = self.FIRST_MENU_ITEM
        elif input in [curses.KEY_LEFT,ord('h')] and self.selected_menu>self.BCHUD_MENU:
            self.selected_menu = self.selected_menu-1
            self.menu_selected_item = self.FIRST_MENU_ITEM

    def Result(self):
        return(self._bcmenu_result)

    def Open(self):
        self.selected_menu = self.BCHUD_MENU

    def IsOpen(self):
        return(self.selected_menu != self.MENUS_CLOSED)

    def Exit(self):
        return(self._bcmenu_result == BCHudConstants.BCMENU_EXIT)

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    BCHudConstants.cursessetup(stdscr)
    bcmenubar = BCMenuBar(stdscr,bcgi)

    try:
        (height,width) = stdscr.getmaxyx()
        keyboardinput = 0
        while keyboardinput != ord("q") and not bcmenubar.Exit(): 
            (height,width) = stdscr.getmaxyx()

            if bcmenubar.IsOpen():
                bcmenubar.EventHandler(keyboardinput)
            elif keyboardinput == ord('\t'):
                bcmenubar.Open()

            stdscr.addstr(2,0,f"Last Menu Result: {bcmenubar.Result():4} ",curses.A_NORMAL)

            bcmenubar.Render(height,width)
            curses.doupdate()
            if not bcmenubar.Exit():
                keyboardinput = stdscr.getch()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

if __name__ == "__main__":
    (minecraftdir,servername,worldname) = BCHudConstants.initserver()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, servername, worldname)