#!/usr/bin/python3

from bcgameinstance import BCGameInstance
from bchudconstants import BCHudConstants
from bcmenubar import BCMenuBar

from os import environ
import curses
from curses import panel
from argparse import ArgumentParser




class BCHud():

    def __init__(self, stdscr:curses.window, bcgi:BCGameInstance):

        self.stdscr = stdscr 
        self.bcgi =  bcgi

#        self.advancementwindow = curses.newwin(0,0)
#        self.advancementpanel = panel.new_panel(self.advancementwindow)
#        self.bcadvancementwindow = BCAdvancementWindow(self.advancementwindow,self.bcgi)

        self.currentmode = BCHudConstants.MODE_QUIT

    def Render(self):
        (height,width) = self.stdscr.getmaxyx()
        if(height!=self.height or width!=self.width):
            self.height = height
            self.width = width

        panel.update_panels()
        curses.doupdate()

    def EventHandler(self,input):
        self.lastinputkey = input
        if input in [ord('Q'),ord('q')]:
            pass
        elif input in [curses.KEY_UP, ord('k')]:
            pass
        elif input in [curses.KEY_DOWN, ord('j')]:
            pass
        elif input in [curses.KEY_LEFT, ord('h')]:
            pass
        elif input in [curses.KEY_RIGHT, ord('l')]:
            pass
        elif input in [curses.KEY_ENTER, ord('\n')]:
            pass
        elif input == 27:  #KEY_ESCAPE
            pass

    def Exit(self):
        if(self.currentmode == BCHudConstants.MODE_QUIT):
            return True
        else:
            return False



#def rendermenubar(stdscr, bcgi):
#
#    stdscr.addstr(0,0,f"BC HUD {servername}:{worldname}", curses.A_BOLD | curses.A_REVERSE)
#    stdscr.addstr(0,0,f"BC HUD {bcgi.AllAdvancementsCount()}", curses.A_BOLD | curses.A_REVERSE)
#    stdscr.chgat(-1, curses.A_REVERSE)


def main(stdscr, minecraftdir, servername, worldname):

    bcgi = BCGameInstance(minecraftdir,servername,worldname)
    bchud = BCHud(stdscr, bcgi)
    BCHudConstants.cursessetup(stdscr)
    stdscr.clear()
    try:
        while not bchud.Exit():

            bcgi.UpdateGameInfo()
            bchud.Render()

            input = stdscr.getch()
            bchud.EventHandler(input)

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()






#
#    timerwindow = curses.newwin(height-2,width,1,0)
#    statusbarwin = curses.newwin(height-2,width,1,0)
#
#    bctimerwindow = BCTimerWindow(timerwindow)
#    bcstatusbar = BCStatusBar(stdscr,statusbarwin)
#
#    statpanel = panel.new_panel(timerwindow)
#    statusbarpanel = panel.new_panel(statusbarwin)
#
#   key = 0
#   activewindow=1
#

    # Loop where k is the last character presse
   # while (key != ord('q')):
#
#        if key == ord('s'):
#            bcgi.SaveAllFiles()
#        elif key == ord('t'):
#            bctimerwindow.RecordTime(bcgi)
#        elif key == ord('0'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#            activewindow = 0
#        elif key == ord('1'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#            activewindow = 1
#        elif key == ord('2'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#            activewindow = 2 
#        elif key == curses.KEY_RESIZE or key == ord('w'):
#            stdscr.clear()
#            statusbarwin.clear()
#            timerwindow.clear()
#

#        rendermenubar(stdscr,bcgi) 
#        bcstatusbar.Render(bcgi)
#        stdscr.noutrefresh()
#
#        if (activewindow==1):
#            bcstatusbar.RenderWindow(bcgi) 
#            statusbarwin.noutrefresh()
#            statpanel.hide()
#            statusbarpanel.show()
#        elif (activewindow==2):
#            bctimerwindow.Render(bcgi) 
#            timerwindow.noutrefresh()
#            statpanel.show()
#            statusbarpanel.hide()
#        else:
#            statpanel.hide()
#            statusbarpanel.hide()
#
#        panel.update_panels()
#        curses.doupdate()

        # Wait for next input



if __name__ == "__main__":
    (minecraftdir,servername,worldname) = BCHudConstants.initserver()
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main, minecraftdir, servername, worldname)