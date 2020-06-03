# PyQt5 Video player
#!/usr/bin/env python

'''
Based upon code provided by https://pythonprogramminglanguage.com/pyqt5-video-widget/
Quick and dirty script, that definitely needs reworking, but it works for now.
Highly unstable at the moment, expect unwanted crashes!
'''

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys, random
import requests
import json
import urllib.request

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)

        self.readConfig()

        self.setWindowTitle("Endless Reddit Player") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.data = requests.get(f'https://www.reddit.com/r/{self.subreddit}/{self.sortby}.json?limit=100', headers = {'User-agent': 'endless video bot uwu'}).json()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.skipButton = QPushButton()
        self.skipButton.setEnabled(True)
        self.skipButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.skipButton.clicked.connect(self.selectNewVideo)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.skipButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def readConfig(self):
        with open('config.json', 'r') as file:
            config = json.load(file)
            self.subreddit = config['subreddit']
            self.sortby = config['sortby']
            self.offlineMode = config['offlineMode']

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.playButton.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPause))
            else:
                self.playButton.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPlay))

    def mediaStatusChanged(self, status):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            self.mediaPlayer.pause()
            self.selectNewVideo()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
        
    def selectNewVideo(self):
        if len(self.data['data']['children']) == 0:
            if(self.data["data"]["after"]):
                self.data = requests.get(f'https://www.reddit.com/r/{self.subreddit}/{self.sortby}.json?limit=100&after={self.data["data"]["after"]}', headers = {'User-agent': 'endless video bot uwu'}).json()
            else:
                self.data = requests.get(f'https://www.reddit.com/r/{self.subreddit}/{self.sortby}.json?limit=100', headers = {'User-agent': 'endless video bot uwu'}).json()
        number = random.randrange(len(self.data['data']['children']))
        if self.data['data']['children'][number]['data']['is_video']:
            self.url = self.data['data']['children'][number]['data']['media']['reddit_video']['fallback_url']
            print("selected next: " + self.url + ", " + str(len(self.data['data']['children'])) + " left before rescan.")
            self.mediaPlayer.setMedia(QMediaContent(QUrl(self.url)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()
            del self.data['data']['children'][number]
        else: 
            del self.data['data']['children'][number]
            self.selectNewVideo()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    player.selectNewVideo()
    sys.exit(app.exec_())