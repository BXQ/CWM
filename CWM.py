#! /usr/bin/python
"""CWM tests and trains complex working memory"""
##################################################################################
# CWM is a program to test and train complex working memory
#                                                          
# Most of the program is based on details gleaned from
# "Can You Make Yourself Smarter?"
# by Dan Hurley, New York Times, 18 April, 2012
# As well as "The generality of working memory capacity:
# a latent-variable approach to verbal and visuospatial memory span and reasoning"
# by Kane, et. al., J. Exp. Psychol. Gen., 2004
#
# Copyright (C) 2012: Brandon Milholland
# brandon dot milholland at gmail dot com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##################################################################################





import time
import random
import curses


def main():
    """The main function of the program"""
    fill_window(stdscr, " ", pair=1)
    prev_results = list()
    prev_trials = 0
    
    level = 2
    while True:
        if not begin_prompt(level):
            return 0
        else:
            prev_results.append(task(level))
            prev_trials += 1
            if prev_trials < 2:
                level = 2
                continue
            if prev_results[-1] and prev_results[-2]:
                level += 1
            if not (prev_results[-1] or prev_results[-2]):
                level = max(1, level-1)

def fill_window(win, char, pair=0):
    """Fills window win with character char"""
    height, width = win.getmaxyx()
    string = char*(width-1)
    for line in range(height):
        win.addstr(line, 0 , string, curses.color_pair(pair))
    win.refresh()
        
def printc(message, window, pair=0, yoffset=0, attribute=0, xoffset=0):
    """Prints a message in the center of a window, with an optional offset"""
    rows, cols = window.getmaxyx()
    window.addstr(rows//2+yoffset, (cols-len(message))//2+xoffset, message,
                  curses.color_pair(pair) | attribute)
    window.refresh()
                         
def task(level):
    """Performs the complex working memory span task at a given level"""
    result = True
    locations = list()
    for i in range(level):
        result =  symmetry_tasks() and result
        locations.append(random.randint(0, 15))
        display_location(locations[i])
    result = recall_prompt(locations) and result
    return result

def begin_prompt(level):
    """The initial prompt for the program."""
    fill_window(stdscr, " ", pair=1)
    printc("Complex Working Memory Span Testing and Training Program",
           stdscr, pair=1, yoffset=-10)
    printc("Current level: "+str(level), stdscr, pair=1)
    key = ""
    printc("Press c to enter testing or q to quit.", stdscr, yoffset=1, pair=1)
    printc("Copyright (C) 2012: Brandon Milholland", stdscr, yoffset=10, pair=1)
    printc("Distributed under the GNU Affero General Public License", stdscr, yoffset=11, pair=1)
    while(key != ord("c") and key != ord("q")):
        key = stdscr.getch()
        if key == ord("c"):
            return True
        if key == ord("q"):
            return False
        
def symmetry_tasks():
    """Prompts the user to determine the symmetry of 3 random 8x8 matrices"""
    result = True
    for i in range(3):
        symmetrical = random.randint(0, 1)
        if symmetrical:
            display_matrix(generate_symmetrical())
        else:
            display_matrix(generate_asymmetrical())
                                
        key = ""
        printc("Is this pattern symmetrical?", stdscr, pair=1, yoffset=8)
        printc("y/n", stdscr, pair=1, yoffset=9)
        while(key !=ord("y") and key!=ord("n")):
            key = stdscr.getch()
            if key == ord("y"):
                result = result and symmetrical
                
            if key == ord("n"):
                result = result and not symmetrical
                
            if (key == ord("y") and symmetrical) or (key == ord("n") and not symmetrical) :
                printc("Right", stdscr, pair=1, yoffset=9)
            elif key == ord("y") or key == ord("n"):
                printc("Wrong", stdscr, pair=1, yoffset=9)
        time.sleep(.5)
        fill_window(stdscr, " ", pair=1)
    return result

def display_matrix(matrix):
    """Displays a matrix in the center of stdscr"""
    fill_window(stdscr, " ", pair=1)
    i = 0
    for row in matrix:
        printc(row, stdscr, pair=1, yoffset=i)
        i += 1

def generate_asymmetrical():
    """Generates a matrix highly unlikely (<0.02%) to be symmetrical"""
    matrix = list()
    for i in range(8):
        row = ""
        for j in range(8):
            if(random.randint(0, 1) == 0):
                row += "O"
            else:
                row += "*"
        matrix.append(row)
    return matrix

def generate_symmetrical():
    """Generates a matrix guaranteed to be symmetrical"""
    matrix = list()
    for i in range(8):
        row = ""
        for j in range(4):
            if(random.randint(0, 1) == 0):
                row += "O"
            else:
                row += "*"
        row += row[::-1]
        matrix.append(row)
    return matrix

def display_location(location):
    """Displays a location to be memorized"""
    fill_window(stdscr, " ", pair=1)
    printc("Remember the location of the star.", stdscr, pair=1)
    grid = 16*"O"
    grid = grid[0:location]+"*"+grid[location+1:]
    for i in range(4):
        printc(grid[i*4:(i+1)*4], stdscr, yoffset=1+i, pair=1)
    time.sleep(.65)
    fill_window(stdscr, " ", pair=1)
    time.sleep(.5)

def recall_prompt(locations):
    """Prompts the user to recall a series of locations"""
    i = 1
    result = True
    for loc in locations:
        fill_window(stdscr, " ", pair=1)
        printc("Where was location "+str(i)+"?", stdscr, pair=1)
        printc("Use the arrow keys to move the star and press space to select.",
               stdscr, yoffset=5, pair=1)
        key = ""
        cursor_pos = [0, 0]
        rows, cols = stdscr.getmaxyx()
        upper_left = [rows//2+1, (cols-4)//2]
        while key != ord(" "):
            for j in range(4):
                printc(4*"O", stdscr, pair=1, yoffset=1+j)
            stdscr.addch(upper_left[0]+cursor_pos[0], upper_left[1]+cursor_pos[1], "*", curses.color_pair(1))
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP:
                cursor_pos[0] = max(0, cursor_pos[0]-1)
            elif key == curses.KEY_DOWN:
                cursor_pos[0] = min(3, cursor_pos[0]+1)
            elif key == curses.KEY_LEFT:
                cursor_pos[1] = max(0, cursor_pos[1]-1)
            elif key == curses.KEY_RIGHT:
                cursor_pos[1] = min(3, cursor_pos[1]+1)

        if 4*cursor_pos[0]+cursor_pos[1] == loc:
            printc("Correct", stdscr, pair=1, yoffset=6)
            result = result and True
        else:
            printc("Incorrect", stdscr, pair=1, yoffset=6)
            result = result and False
        time.sleep(.5)
        i += 1
    return result
    

            


random.seed()
stdscr = curses.initscr()
curses.start_color()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
curses.curs_set(0) 



try:         
    main()

finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


