import curses
import curses.textpad
import os

import sys

"""Library of the CLI Audio Player"""
class Library:


    def __init__(self):
        self.queue = []

    """returns a list of songs in the library"""
    def songsList(self):
        songs = []
        for file in os.listdir(os.getcwd()):
            if file.endswith(".wav"):
                songs.append(file)
        return songs

    """Searches for a given song in the library"""
    def searchSong(self, songName):
        songs = self.songsList()

        for song in songs:
            if(songName == song):
                return True
        return False

    """Adds chosen song to the queue"""
    def addToQueue(self, songName):
        self.queue.append(songName)

    """returns the next song in the queue"""
    def getNextSong(self):
        if len(self.queue) == 0:
            return None

        song = self.queue[0]
        del self.queue[0]
        return song
