import curses
from pathlib import Path 
from math import floor


def alpha(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, curses.COLOR_WHITE, i)
    try:
        for i in range(0, 255):
            stdscr.addstr(str(i), curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

def beta():
    fname = Path("/media/deflection/Minecraft/server/snapshot/snapshot/leveal.dat")
    if( not fname.exists()):
        print("doesn't exist")
    else:
        print(fname.stat().st_mtime)

def charlie():
    beforenight = (12542-(1000%24000))/20
    negstr = "-" if beforenight < 0 else ""
    centerstatusbarstr = '{:0.0f}   {}{:0}:{:02}'.format(beforenight,negstr,floor(abs(beforenight)/60),round(abs(beforenight)%60))
    print(centerstatusbarstr)

    beforenight = (12542-(12500%24000))/20
    negstr = "-" if beforenight < 0 else ""
    centerstatusbarstr = '{:0.0f}   {}{:0}:{:02}'.format(beforenight,negstr,floor(abs(beforenight)/60),round(abs(beforenight)%60))
    print(centerstatusbarstr)

    beforenight = (12542-(12600%24000))/20
    negstr = "-" if beforenight < 0 else ""
    centerstatusbarstr = '{:0.0f}   {}{:0}:{:02}'.format(beforenight,negstr,floor(abs(beforenight)/60),round(abs(beforenight)%60))
    print(centerstatusbarstr)

    beforenight = (12542-(14500%24000))/20
    negstr = "-" if beforenight < 0 else ""
    centerstatusbarstr = '{:0.0f}   {}{:0}:{:02}'.format(beforenight,negstr,floor(abs(beforenight)/60),round(abs(beforenight)%60))
    print(centerstatusbarstr)

def delta():
    width = 10
    title = "Curses example"[:width-1]
    print("-"+title+"-")

#curses.wrapper(alpha)
#beta()
#charlie()
delta()