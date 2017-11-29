# -*- coding:utf-8 -*-
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5 import QtCore, QtWidgets
import sys, os, random

files = os.walk('..\\resources\\sound')

play_list = []

for path, d, file_list in files:
    for filename in file_list:
        play_list.append(os.path.join(path, filename))

app = QtWidgets.QApplication(sys.argv)

player = QMediaPlayer()
playList = QMediaPlaylist()


def over():
    player.pause()
    index = player.playlist().currentIndex()
    recv = input("Exit(Y/N)?: ")
    if recv == 'N':
        player.playlist().setCurrentIndex(random.uniform(1, index))
    else:
        sys.exit()
    player.play()


playList.setPlaybackMode(QMediaPlaylist.Loop)
for music in play_list:
    playList.addMedia((QMediaContent(QtCore.QUrl.fromLocalFile(music))))
player.setPlaylist(playList)
# player.playlist().currentIndexChanged.connect(over)
player.play()
sys.exit(app.exec_())
