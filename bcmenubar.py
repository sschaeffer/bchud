#!/usr/bin/python3
from bcgameinstance import BCGameInstance
from bchudconstants import BCHudConstants

import curses
from curses import panel
from os import environ

class BCMenuBar():

    BCHUD_MENU_ITEMS = [["Bacap Advancements",BCHudConstants.BCMENU_BACAP_ADVANCEMENTS],
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

    USERS_MENU_ITEMS =[["stephenschaeffer",BCHudConstants.BCMENU_USER1],
                       ["Sebbac80",BCHudConstants.BCMENU_USER2],
                       ["Noodle_Hair",BCHudConstants.BCMENU_USER3],
                       ["Lilly__Bug",BCHudConstants.BCMENU_USER4],
                       ["Yee_L",BCHudConstants.BCMENU_USER5],
                       ["diggles",BCHudConstants.BCMENU_USER6],
                       ["LastStay",BCHudConstants.BCMENU_USER7]]

    LEVEL_MENU_ITEMS =[["Auto-Update",BCHudConstants.BCMENU_AUTO_UPDATE],
                       ["Auto-Backup",BCHudConstants.BCMENU_AUTO_BACKUP],
                       ["Day/Night Cycle",BCHudConstants.BCMENU_DAY_NIGHT_CYCLE],
                       ["Level Info",BCHudConstants.BCMENU_LEVEL_INFO],
                       ["BCLogs",BCHudConstants.BCMENU_BCLOGS],
                       ["latest.log",BCHudConstants.BCMENU_LATEST_LOG],
                       ["Timing Window",BCHudConstants.BCMENU_TIMING_WINDOW],
                       ["Change Server/World",BCHudConstants.BCMENU_CHANGE_SERVER_WORLD],
                       ["Save Level File",BCHudConstants.BCMENU_SAVE_LEVEL_FILE],
                       ["Update",BCHudConstants.BCMENU_UPDATE],
                       ["Record Time",BCHudConstants.BCMENU_RECORD_TIME]]

    MENUS_CLOSED=0
    BCHUD_MENU=FIRST_MENU_ITEM=1
    USERS_MENU=2
    LEVEL_MENU=3
    REFRESH_MENU=4
    QUIT_MENU=5

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):
        self._stdscr = stdscr 
        self._bcgi = bcgi

        self._selected_menu = self.MENUS_CLOSED
        self._bcmenu_result = BCHudConstants.BCMENU_NOCHANGE

        self._totalheight = 0
        self._totalwidth = 0
        self._menu_selected_item = 0
        self._menu_selected_items_max = 0

        self._menu_selected_user = BCHudConstants.BCMENU_USER1
        self._menu_auto_update_selected = True
        self._menu_auto_backup_selected = True

        self._bchud_menu_window = curses.newwin(0,0)
        self._bchud_menu_panel = panel.new_panel(self._bchud_menu_window)
        self._bchud_menu_panel.hide()

        self._users_menu_window = curses.newwin(0,0)
        self._users_menu_panel = panel.new_panel(self._users_menu_window)
        self._users_menu_panel.hide()

        self._level_menu_window = curses.newwin(0,0)
        self._level_menu_panel = panel.new_panel(self._level_menu_window)
        self._level_menu_panel.hide()

    def render_bchud_menu(self):
        BCHUD_MENU_WIDTH=27
        self._menu_selected_items_max = len(self.BCHUD_MENU_ITEMS)+1
        self._bchud_menu_window.resize(len(self.BCHUD_MENU_ITEMS)+4,BCHUD_MENU_WIDTH)
        self._bchud_menu_window.border()
        if self._menu_selected_item == 1:
            self._bchud_menu_window.addstr(1,1,f" {'All Advancements'.ljust(BCHUD_MENU_WIDTH-4)} ", curses.A_REVERSE)
        else:
            self._bchud_menu_window.addstr(1,1,f" {'All Advancements'.ljust(BCHUD_MENU_WIDTH-4)} ")
        self._bchud_menu_window.addstr(2,0,"\u251C")
        for i in range (1,BCHUD_MENU_WIDTH-1):
            self._bchud_menu_window.addstr(2,i,"\u2500")
        self._bchud_menu_window.addstr(2,BCHUD_MENU_WIDTH-1,"\u2524")
        for idx, i in enumerate(self.BCHUD_MENU_ITEMS):
            if self._menu_selected_item == idx+2:
                self._bchud_menu_window.addstr(idx+3,1,f" {str(i[0]).ljust(BCHUD_MENU_WIDTH-4)} ", curses.A_REVERSE)
            else:
                self._bchud_menu_window.addstr(idx+3,1,f" {str(i[0]).ljust(BCHUD_MENU_WIDTH-4)} ")

        self._bchud_menu_panel.move(1,1)
        self._bchud_menu_panel.show()

    def render_users_menu(self):
        USERS_MENU_WIDTH=22
        self._menu_selected_items_max = len(self.USERS_MENU_ITEMS)
        self._users_menu_window.resize(len(self.USERS_MENU_ITEMS)+2,USERS_MENU_WIDTH)
        self._users_menu_window.border()
        for idx, i in enumerate(self.USERS_MENU_ITEMS):
            if self._menu_selected_item == idx+1:
                if self._menu_selected_user == i[1]:
                    self._users_menu_window.addstr(idx+1,1,f" * {str(i[0]).ljust(USERS_MENU_WIDTH-6)} ", curses.A_REVERSE)
                else:
                    self._users_menu_window.addstr(idx+1,1,f"   {str(i[0]).ljust(USERS_MENU_WIDTH-6)} ", curses.A_REVERSE)
            else:
                if self._menu_selected_user == i[1]:
                    self._users_menu_window.addstr(idx+1,1,f" * {str(i[0]).ljust(USERS_MENU_WIDTH-6)} ")
                else:
                    self._users_menu_window.addstr(idx+1,1,f"   {str(i[0]).ljust(USERS_MENU_WIDTH-6)} ")

        self._users_menu_panel.move(1,7)
        self._users_menu_panel.show()

    def render_level_menu(self):
        LEVEL_MENU_WIDTH=25
        self._menu_selected_items_max = len(self.LEVEL_MENU_ITEMS)
        self._level_menu_window.resize(len(self.LEVEL_MENU_ITEMS)+2,LEVEL_MENU_WIDTH)
        self._level_menu_window.border()
        for idx, i in enumerate(self.LEVEL_MENU_ITEMS):

            if self._menu_selected_item == idx+1:
                if i[1] == BCHudConstants.BCMENU_AUTO_UPDATE and self._menu_auto_update_selected:
                    self._level_menu_window.addstr(idx+1,1,f" * {str(i[0]).ljust(LEVEL_MENU_WIDTH-6)} ", curses.A_REVERSE)
                elif i[1] == BCHudConstants.BCMENU_AUTO_BACKUP and self._menu_auto_backup_selected:
                    self._level_menu_window.addstr(idx+1,1,f" * {str(i[0]).ljust(LEVEL_MENU_WIDTH-6)} ", curses.A_REVERSE)
                else:
                    self._level_menu_window.addstr(idx+1,1,f"   {str(i[0]).ljust(LEVEL_MENU_WIDTH-6)} ", curses.A_REVERSE)
            else:
                if i[1] == BCHudConstants.BCMENU_AUTO_UPDATE and self._menu_auto_update_selected:
                    self._level_menu_window.addstr(idx+1,1,f" * {str(i[0]).ljust(LEVEL_MENU_WIDTH-6)} ")
                elif i[1] == BCHudConstants.BCMENU_AUTO_BACKUP and self._menu_auto_backup_selected:
                    self._level_menu_window.addstr(idx+1,1,f" * {str(i[0]).ljust(LEVEL_MENU_WIDTH-6)} ")
                else:
                    self._level_menu_window.addstr(idx+1,1,f"   {str(i[0]).ljust(LEVEL_MENU_WIDTH-6)} ")

        self._level_menu_panel.move(1,14)
        self._level_menu_panel.show()


    def render(self,height,width):
#        self.stdscr.addstr(0,0,f"BC HUD {bcgi._servername}:{self.bcgi._worldname}", curses.A_BOLD | curses.A_REVERSE)
#        self.stdscr.addstr(0,0,f"BC HUD {self.bcgi.AllAdvancementsCount()}", curses.A_BOLD | curses.A_REVERSE)
        if(height<BCHudConstants.MINIMUM_HEIGHT or width<BCHudConstants.MINIMUM_WIDTH):
            return
        self._width = width
        self._stdscr.addstr(0,0," ", curses.A_REVERSE)
        self._stdscr.chgat(-1, curses.A_REVERSE)
        if self._selected_menu == self.BCHUD_MENU:
            self._stdscr.addstr(0,1,f" BCHUD ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self._stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self._stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-16,f" REFRESH ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-7,f" QUIT ", curses.A_REVERSE)
            self._level_menu_panel.hide()
            self._users_menu_panel.hide()
            self.render_bchud_menu()
        elif self._selected_menu == self.USERS_MENU:
            self._stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self._stdscr.addstr(0,8,f" USERS ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self._stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-16,f" REFRESH ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-7,f" QUIT ", curses.A_REVERSE)
            self._level_menu_panel.hide()
            self._bchud_menu_panel.hide()
            self.render_users_menu()
        elif self._selected_menu == self.LEVEL_MENU:
            self._stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self._stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self._stdscr.addstr(0,15,f" LEVEL ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self._stdscr.addstr(0,self._width-16,f" REFRESH ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-7,f" QUIT ", curses.A_REVERSE)
            self._users_menu_panel.hide()
            self._bchud_menu_panel.hide()
            self.render_level_menu()
        elif self._selected_menu == self.REFRESH_MENU:
            self._stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self._stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self._stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-16,f" REFRESH ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self._stdscr.addstr(0,self._width-7,f" QUIT ", curses.A_REVERSE)
            self._level_menu_panel.hide()
            self._users_menu_panel.hide()
            self._bchud_menu_panel.hide()
        elif self._selected_menu == self.QUIT_MENU:
            self._stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self._stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self._stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-16,f" REFRESH ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-7,f" QUIT ", curses.color_pair(BCHudConstants.COLOR_BCMENU_SELECTED_MENU)|curses.A_BOLD)
            self._level_menu_panel.hide()
            self._users_menu_panel.hide()
            self._bchud_menu_panel.hide()
        else:
            self._stdscr.addstr(0,1,f" BCHUD ", curses.A_REVERSE)
            self._stdscr.addstr(0,8,f" USERS ", curses.A_REVERSE)
            self._stdscr.addstr(0,15,f" LEVEL ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-16,f" REFRESH ", curses.A_REVERSE)
            self._stdscr.addstr(0,self._width-7,f" QUIT ", curses.A_REVERSE)
            self._level_menu_panel.hide()
            self._users_menu_panel.hide()
            self._bchud_menu_panel.hide()

        panel.update_panels()
        self._stdscr.noutrefresh()

    def event_handler(self,input):

        if input in [27,ord('\t')]:
            self._selected_menu = self.MENUS_CLOSED
            self._menu_selected_item = self.FIRST_MENU_ITEM
            self._bcmenu_result = BCHudConstants.BCMENU_NOCHANGE

        elif input in [curses.KEY_ENTER,ord('\n')]:

            if self._selected_menu==self.BCHUD_MENU:
                if(self._menu_selected_item==self.FIRST_MENU_ITEM):
                    self._bcmenu_result = BCHudConstants.BCMENU_ALL_ADVANCEMENTS
                else:
                    self._bcmenu_result = self.BCHUD_MENU_ITEMS[self._menu_selected_item-2][1] 

            if self._selected_menu==self.USERS_MENU:
                self._bcmenu_result = self.USERS_MENU_ITEMS[self._menu_selected_item-1][1] 
                self._menu_selected_user = self._bcmenu_result 

            if self._selected_menu==self.LEVEL_MENU:
                self._bcmenu_result = self.LEVEL_MENU_ITEMS[self._menu_selected_item-1][1] 
                if(self._bcmenu_result == BCHudConstants.BCMENU_AUTO_UPDATE):
                    self._menu_auto_update_selected = not self._menu_auto_update_selected
                if(self._bcmenu_result == BCHudConstants.BCMENU_AUTO_BACKUP):
                    self._menu_auto_backup_selected = not self._menu_auto_backup_selected
            if self._selected_menu==self.QUIT_MENU:
                self._bcmenu_result = BCHudConstants.BCMENU_EXIT

            if self._selected_menu==self.REFRESH_MENU:
                self._bcmenu_result = BCHudConstants.BCMENU_REFRESH

            self._selected_menu = self.MENUS_CLOSED
            self._menu_selected_item = self.FIRST_MENU_ITEM
            
        elif input in [curses.KEY_DOWN,ord('j')] and self._menu_selected_item<self._menu_selected_items_max:
            self._menu_selected_item = self._menu_selected_item+1
        elif input in [curses.KEY_UP,ord('k')] and self._menu_selected_item>1:
            self._menu_selected_item = self._menu_selected_item-1
        elif input in [curses.KEY_RIGHT,ord('l')] and self._selected_menu<self.QUIT_MENU:
            self._selected_menu = self._selected_menu+1
            self._menu_selected_item = self.FIRST_MENU_ITEM
        elif input in [curses.KEY_LEFT,ord('h')] and self._selected_menu>self.BCHUD_MENU:
            self._selected_menu = self._selected_menu-1
            self._menu_selected_item = self.FIRST_MENU_ITEM

    def result(self):
        return(self._bcmenu_result)

    def open(self):
        self._selected_menu = self.BCHUD_MENU

    def is_open(self):
        return(self._selected_menu != self.MENUS_CLOSED)

    def exit(self):
        return(self._bcmenu_result == BCHudConstants.BCMENU_EXIT)

def main(stdscr:curses.window, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    BCHudConstants.curses_setup(stdscr)
    bcmenubar = BCMenuBar(stdscr,bcgi)

    try:
        keyboardinput = 0
        while keyboardinput != ord("q") and not bcmenubar.Exit(): 
            (height,width) = BCHudConstants.check_minimum_size(stdscr)

            if bcmenubar.is_open():
                bcmenubar.event_handler(keyboardinput)
            elif keyboardinput == ord('\t'):
                bcmenubar.open()

            stdscr.addstr(2,0,f"Last Menu Result: {bcmenubar.result():4} ",curses.A_NORMAL)

            bcmenubar.render(height,width)
            curses.doupdate()
            if not bcmenubar.exit():
                keyboardinput = stdscr.getch()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

if __name__ == "__main__":
    (minecraftdir,servername,worldname) = BCHudConstants.init_server()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, servername, worldname)