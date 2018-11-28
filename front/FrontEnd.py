import curses
import curses.textpad
import CLI_Audio_Exception
from library.Library import Library
import os
import sys
import time

"""Front End of the CLI Audio Player"""
class FrontEnd:

    def __init__(self, player):
        self.library = Library()
        self.player = player
        curses.wrapper(self.menu)


    """Displays the main menu"""
    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        self.stdscr.addstr(0,0, "CLI Audio Player",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(8,10, "n - Next song in queue")
        self.stdscr.addstr(10,10, "ESC - Quit")
        height,width = self.stdscr.getmaxyx()
        if(height < 20 or width < 60):
            raise CLI_Audio_Exception.CLI_Audio_Screen_Size_Exception
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('l'):
                self.displayLibrary()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.clear()
                curses.wrapper(self.menu)
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('n'):
                next = self.library.getNextSong()
                if next != None:
                    self.player.stop()
                    self.player.play(next.decode(encoding="utf-8"))
                    self.updateSong()
                    self.stdscr.clear()
                    self.stdscr.touchwin()
                    self.stdscr.refresh()
                    curses.wrapper(self.menu)
                else:
                    self.player.resetCurrentSong()
                    curses.wrapper(self.menu)

    """Updates the song in the Now Playing field"""
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    """Changes the song to be played"""
    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 35)
        changeWindow.border()
        changeWindow.addstr(0,0, "Enter name of the song(including .wav)", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        songName = changeWindow.getstr(1,1, 30)
        if self.library.searchSong(songName) is True:
                playSong = songName
        else:
            raise CLI_Audio_Exception.CLI_Audio_File_Exception
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(playSong.decode(encoding="utf-8"))

    """Displays library (wav files)"""
    def displayLibrary(self):
        changeWindow = curses.newwin(24, 80, 0, 0)
        changeWindow.border()
        changeWindow.addstr(0,0, "Audio Library", curses.A_REVERSE)
        changeWindow.addstr(1,5, "Songs:")
        changeWindow.addstr(1,60, "b - Back")
        changeWindow.addstr(2,60, "a - add to queue")
        i = 0
        x = 3
        songs = self.library.songsList()
        for song in songs:
            i += 1
            x += 1
            changeWindow.addstr(x, 5, str(i)+". "+song)
        while True:
            c = changeWindow.getch()
            if c == ord('b'):
                curses.wrapper(self.menu)
            elif c == ord('a'):
                self.addQueue()

        self.stdscr.refresh()
        c = changeWindow.getch()
        path = changeWindow.getstr(20,5, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

    """Adds the chosen song to a queue"""
    def addQueue(self):
        queueBox = curses.newwin(5, 40, 5, 35)
        queueBox.border()
        queueBox.addstr(0,0, "Enter name of the song(including .wav)", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        songName = queueBox.getstr(1,1, 30)
        if self.library.searchSong(songName) is True:
            self.library.addToQueue(songName)

        curses.noecho()
        del queueBox
        self.stdscr.touchwin()
        self.stdscr.refresh()
        curses.wrapper(self.menu)


    def quit(self):
        self.player.stop()
        exit()
