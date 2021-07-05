from bcalladvancements import BCAdvancement, BCAllAdvancements
from bcgameinstance import BCGameInstance
import curses

class BCAdvancementWindow():

    ADVANCEMENT_INCOMPLETE=30
    ADVANCEMENT_COMPLETE=31

    def __init__(self, window, bcgi):
        self.window:curses.window = window
        self.bcgi:BCGameInstance = bcgi
        self._selectedItem = ""


    def Render(self,height,width,currentitem,topitem,currentcrit,topcrit):
        self.window.resize(height-2,width)
        self.window.clear()

        criterialen = 0

        mining_advancements = self.bcgi.MiningAdvancements()
        mining_advancements_list = list(mining_advancements.items())
        for i in range(len(mining_advancements_list))[topitem:topitem+height-2]:
            j=i-topitem
            advancementname:str = mining_advancements_list[i][0].split('/')[1]
            if j == currentitem:
                self._highlightedItem = mining_advancements_list[i][0]
                if(mining_advancements[mining_advancements_list[i][0]]._completed == BCAdvancement.ADVANCEMENT_COMPLETED):
                    self.window.addstr(j,0,advancementname, curses.color_pair(self.ADVANCEMENT_COMPLETE)|curses.A_REVERSE|curses.A_BOLD)
                else:
                    self.window.addstr(j,0,advancementname, curses.A_REVERSE|curses.A_BOLD)
            else:
                if(mining_advancements[mining_advancements_list[i][0]]._completed == BCAdvancement.ADVANCEMENT_COMPLETED):
                    self.window.addstr(j,0,advancementname, curses.color_pair(self.ADVANCEMENT_COMPLETE))
                else:
                    self.window.addstr(j,0,advancementname)

        if self._selectedItem != "":
            advancement:BCAdvancement = self.bcgi._bcalladvancements._advancements[self._selectedItem]
            criterialen = len(advancement._criteria) 
            for i in range(criterialen)[topcrit:topcrit+height-2]:
                j=i-topcrit
                if j == currentcrit:
                    if advancement._criteria[i] in advancement._finished:
                        self.window.addstr(j,30,advancement._criteria[i], curses.color_pair(self.ADVANCEMENT_COMPLETE)|curses.A_REVERSE|curses.A_BOLD)
                    else:
                        self.window.addstr(j,30,advancement._criteria[i], curses.A_REVERSE|curses.A_BOLD)
                else:
                    if advancement._criteria[i] in advancement._finished:
                        self.window.addstr(j,30,advancement._criteria[i], curses.color_pair(self.ADVANCEMENT_COMPLETE))
                    else:
                        self.window.addstr(j,30,advancement._criteria[i])

        return (len(mining_advancements_list),criterialen)

    def SelectAdvancement(self):
        self._selectedItem = self._highlightedItem

    def DeselectAdvancement(self):
        self._selectedItem = ""