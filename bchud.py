#!/usr/bin/python3

from datetime import datetime
from bctimer import BCTimer
from times import MCTimes
import curses, time
from curses import wrapper

def main(stdscr):

    curses.halfdelay(5)
    curses.curs_set(0)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    stdscr.refresh()

    key = 0
    cursor_x = 0
    cursor_y = 0

    bct_time = BCTimer()
    bct_daytime = BCTimer()
    mct = MCTimes()

    mcttimestr = ""
    mctdaytimestr = ""
    bcttimestr = ""
    bctdaytimestr = ""
    bctdaystr = ""

    # Loop where k is the last character pressed
    while (key != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if key == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif key == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif key == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif key == curses.KEY_LEFT:
            cursor_x = cursor_x - 1
        elif key == ord('r'):
            mct.saveallfiles()
            bcttimestr = str(mct.gettime())
            bctdaytimestr = str(mct.getdaytime())
            bctdaystr = str(mct.getday())
            bct_time.restart(int(str(mct.gettime())))
            bct_daytime.restart(int(str(mct.getdaytime())))

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        timestr = time.strftime("%H:%M:%S")
        title = "Curses example"[:width-1]
        subtitle = timestr[:width-1]
        mctdaytimestr = bct_daytime.total()+" "+bctdaytimestr
        mcttimestr = bct_time.total()+" "+bcttimestr
        keystr = "Last key pressed: {}".format(key)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if key == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, timestr)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, mcttimestr)
        stdscr.addstr(start_y + 2, start_x_subtitle, mctdaytimestr)
        stdscr.addstr(start_y + 3, start_x_subtitle, bctdaystr)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        key = stdscr.getch()


wrapper(main)