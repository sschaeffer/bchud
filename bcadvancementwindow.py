from bcalladvancements import BCAdvancement, BCAllAdvancements
from bcgameinstance import BCGameInstance
import curses

class BCAdvancementWindow():

    ADVANCEMENT_INCOMPLETE=30
    ADVANCEMENT_COMPLETE=31

    def __init__(self, window, bcgi):
        self.window:curses.window = window
        self.bcgi:BCGameInstance = bcgi

    def Render(self,height,width,currentitem,topitem):
        self.window.resize(height-2,width)
        self.window.clear()

        currentitemidx=0
        if currentitem > height-2:
            currentitemidx = height
        if currentitem > 0:
            currentitemidx = currentitem

        mining_advancements = self.bcgi.MiningAdvancements()
        mining_advancements_list = list(mining_advancements.items())
        for i in range(len(mining_advancements_list))[topitem:topitem+height-2]:
            j=i-topitem
            advancementname:str = mining_advancements_list[i][0].split('/')[1]
            if(mining_advancements[mining_advancements_list[i][0]]._completed == BCAdvancement.ADVANCEMENT_COMPLETED):
                if j == currentitem:
                    self.window.addstr(j,0,advancementname, curses.color_pair(self.ADVANCEMENT_COMPLETE)|curses.A_BOLD)
                else:
                    self.window.addstr(j,0,advancementname, curses.color_pair(self.ADVANCEMENT_COMPLETE))
            else:
                if j == currentitem:
                    self.window.addstr(j,0,advancementname, curses.A_BOLD)
                else:
                    self.window.addstr(j,0,advancementname)

        return len(mining_advancements_list)

