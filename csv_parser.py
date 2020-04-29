import csv
import json
import os


class ItunesSong:
    def __init__(self, name, length, artist, album, genre, plays):
        self.name = name
        self.length = length
        self.artist = artist
        self.genre = genre
        self.plays = plays
        self.album = album


def main():
    song_listt = []
    with open('./SongsLibrary.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            print(row[0])

if __name__ == "__main__":
    main()