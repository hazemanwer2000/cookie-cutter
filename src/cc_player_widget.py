
from cc_player import Player
from cc_assets import assets
from cc_constants import constants
from cc_hover_percentage_bar_widget import HoverPercentageBar

from util import ms_to_format
from util_qt import asset_path, Slider, PushButton

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class PlayerSlider(Slider):
    def __init__(self, playerWidget):
        super().__init__()
        self.playerWidget = playerWidget

    def seek_to_pos(self, e):
        perc = e.position().x() / self.width()
        if perc >= 0 and perc <= 1:
            self.playerWidget.seek(int(self.playerWidget.player.get_media_length() * perc))

    def mousePressEvent(self, e):
        self.seek_to_pos(e)

    def mouseMoveEvent(self, e):
        self.seek_to_pos(e)

class PlayerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.frame = QFrame()
        self.player = Player(self.frame)

        self.volume = 100                   # Note: Used to track currently set volume
        self.muted = False                  # Note: Used to track 'mute' state

        self.createControl()
        self.createFrameContainer()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frameContainer)
        self.layout.addWidget(self.control)
        self.layout.setStretch(self.layout.indexOf(self.frameContainer), 1)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.updateGUI)

    # Function: Create frame layout.
    def createFrameContainer(self):
        self.frameContainer = QWidget()
        frameContainerLayout = QGridLayout()
        self.frameContainer.setLayout(frameContainerLayout)

        # Add frame
        frameContainerLayout.addWidget(self.frame, 1, 1)
        frameContainerLayout.setColumnStretch(1, 1)
        frameContainerLayout.setRowStretch(1, 1)

        # Add Horizontal/Vertical percentage bars
        frameContainerLayout.addWidget(HoverPercentageBar(constants["hover-percentage-bar-horizontal-size"], isHorizontal=True), 0, 1)
        frameContainerLayout.addWidget(HoverPercentageBar(constants["hover-percentage-bar-vertical-size"], isHorizontal=False), 1, 0)

    # Function: Create control bar.
    def createControl(self):
        self.controlPlay = PushButton()
        self.iconPlay = QIcon(asset_path(assets["icon"]["play"]))
        self.iconPause = QIcon(asset_path(assets["icon"]["pause"]))
        self.controlPlay.setIcon(self.iconPlay)
        self.controlPlay.setIconSize(QSize(constants["icon-size"], constants["icon-size"]))
        self.controlPlay.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.controlPlay.setDisabled(True)
        self.controlPlay.clicked.connect(self.toggle)

        self.controlSeek = PlayerSlider(self)
        self.controlSeek.setOrientation(Qt.Orientation.Horizontal)
        self.controlSeek.setMinimum(0)
        self.controlSeek.setTickInterval(1)
        self.controlSeek.setSingleStep(1)
        self.controlSeek.setDisabled(True)
        self.controlSeek.valueChanged.connect(self.seek)

        self.controlTime = QLabel(ms_to_format(0, False))
        self.controlTime.setFixedSize(QSize(constants["button-size"]*3, constants["button-size"]))
        self.controlTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.controlMute = PushButton()
        self.iconMute = QIcon(asset_path(assets["icon"]["mute"]))
        self.iconUnmute = QIcon(asset_path(assets["icon"]["unmute"]))
        self.controlMute.setIcon(self.iconUnmute)
        self.controlMute.setIconSize(QSize(constants["icon-size"], constants["icon-size"]))
        self.controlMute.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.controlMute.setDisabled(True)
        self.controlMute.clicked.connect(self.toggle_mute)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.controlPlay)
        self.controlLayout.addWidget(self.controlTime)
        self.controlLayout.addWidget(self.controlSeek)
        self.controlLayout.addWidget(self.controlMute)
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.setStretch(self.controlLayout.indexOf(self.controlSeek), 1)

        self.control = QWidget()
        self.control.setLayout(self.controlLayout)

    # Function: Update GUI repeatedly.
    def updateGUI(self):
        if self.player.is_ended():
            self.player.play()
        else:
            self.controlSeek.valueChanged.disconnect(self.seek)
            self.controlSeek.setValue(self.player.position())
            self.controlSeek.valueChanged.connect(self.seek)

        self.controlTime.setText(ms_to_format(self.player.position(), False))

    # API: Seek to position in video.
    def seek(self, value):
        self.player.seek(value)

    # API: Skip in video.
    def skip(self, offset):
        new_pos = offset + self.player.position()
        if new_pos < 0 or new_pos >= self.player.get_media_length():
            new_pos = 0
        self.seek(new_pos)

    # API: Skip frame.
    def next_frame(self):
        self.player.next_frame()

    # API: Toggle video (play/pause). 
    def toggle(self):
        if self.player.is_playing():
            self.pause()
        else:
            self.play()

    # API: Load video.
    def load(self, path):
        self.player.load(path)
        self.controlPlay.setIcon(self.iconPause)
        while self.player.get_media_length() == None:         # Note: Wait for video length to update (ie: video fully loaded)
            pass
        self.controlSeek.setMaximum(self.player.get_media_length())
            
            # Note: Enable all controls.
        self.controlSeek.setEnabled(True)
        self.controlPlay.setEnabled(True)
        self.controlMute.setEnabled(True)
        self.timer.start()

    # API: Resume video.
    def play(self):
        self.player.play()
        self.controlPlay.setIcon(self.iconPause)

    # API: Pause video.
    def pause(self):
        self.player.pause()
        self.controlPlay.setIcon(self.iconPlay)

    # Function: Set player's volume (internal-use).
    def update_volume(self):
        if self.muted == True:
            self.player.set_volume(0)
            self.controlMute.setIcon(self.iconMute)
        else:
            self.player.set_volume(self.volume)
            self.controlMute.setIcon(self.iconUnmute)

    # API: Set volume (0-100).
    def set_volume(self, value):
        self.volume = value
        self.update_volume()

    # API: Adjust volume (offset, e.g: +/-).
    def adjust_volume(self, offset):
        self.volume = self.volume + offset
        if self.volume < 0:
            self.volume = 0
            self.controlMute.setIcon(self.iconMute)
        elif self.volume > 100:
            self.volume = 100
            self.controlMute.setIcon(self.iconUnmute)
        self.update_volume()

    # API: Toggle 'mute' state.
    def toggle_mute(self):
        self.muted = not self.muted
        self.update_volume()

    # API: Mute.
    def mute(self):
        self.muted = True
        self.update_volume()

    # API: Mute.
    def unmute(self):
        self.muted = False
        self.update_volume()