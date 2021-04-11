#!/usr/bin/env python3

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

mypad_contents=[]

def echo(stdscr):
  # Create curses screen
  stdscr.refresh()
#  stdscr.keypad(True)
#  curses.use_default_colors()
#  curses.noecho()

  # Get screen width/height
  height,width = stdscr.getmaxyx()

  # Create a curses pad (pad size is height + 10)
  mypad = curses.newpad(height+100, width+100);
#  mypad.scrollok(True)
  mypad_pos = 0
  mypad_refresh = lambda: mypad.noutrefresh(mypad_pos+2, 0, 0, 0, height-1, width-1)
  mypad_refresh()
  # Fill the window with text (note that 5 lines are lost forever)
  try:
    for i in range(0, 33):
        mypad.addstr("{0} This is a sample string...\n".format(i))
        if i > height: mypad_pos = min(i - height, height+100 - height)
        mypad_refresh()
        #time.sleep(0.05)

    # Wait for user to scroll or quit
    running = True
    while running:
        curses.doupdate()
        ch = stdscr.getch()
        if ch == curses.KEY_DOWN and mypad_pos < mypad.getyx()[0] - height - 1:
            mypad_pos += 1
            mypad_refresh()
        elif ch == curses.KEY_UP and mypad_pos > -2:
            mypad_pos -= 1
            mypad_refresh()
        elif ch == ord('Q') or ch == ord('q'):
            running = False
        elif ch == curses.KEY_RESIZE:
            height,width = stdscr.getmaxyx()
            while mypad_pos > mypad.getyx()[0] - height - 1:
              mypad_pos -= 1
            mypad_refresh()
  except KeyboardInterrupt: pass

#curses.wrapper(alpha)
#beta()
#charlie()
#delta()
curses.wrapper(echo)