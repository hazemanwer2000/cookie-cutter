
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from cc_constants import constants
from util import ms_to_format

import ffmpeg
from util_qt import run, PushButton
import cmdln
import re, bisect

class CaptureTimeWidget(QWidget):
    def __init__(self, playerWidget):
        super().__init__()

        self.playerWidget = playerWidget
        self.time_ms = -1

        self.callback = None

        self.buttonCapture = PushButton("C")
        self.buttonCapture.setToolTip("Capture")
        self.buttonCapture.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonCapture.clicked.connect(self.on_capture)

        self.buttonSeek = PushButton("S")
        self.buttonSeek.setToolTip("Seek")
        self.buttonSeek.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonSeek.clicked.connect(self.on_seek)

        self.buttonUndefine = PushButton("U")
        self.buttonUndefine.setToolTip("Undefine")
        self.buttonUndefine.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonUndefine.clicked.connect(self.on_undefine)

        self.labelTime = QLabel(constants["time-undefined"])
        self.labelTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.buttonCapture)
        self.layout.addWidget(self.buttonSeek)
        self.layout.addWidget(self.buttonUndefine)
        self.layout.addWidget(self.labelTime)
        self.layout.setStretch(self.layout.indexOf(self.labelTime), 1)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    # Function: On capture.
    def on_capture(self):
        self.time_ms = self.playerWidget.player.position()
        self.labelTime.setText(ms_to_format(self.time_ms))
        self.callback()

    # Function: On seek.
    def on_seek(self):
        if self.time_ms != -1:
            self.playerWidget.pause()
            self.playerWidget.seek(self.time_ms)

    # Function: On undefine.
    def on_undefine(self):
        self.time_ms = -1
        self.labelTime.setText(constants["time-undefined"])
        self.callback()

    # API: Set time. (-1 if undefined).
    def set_time_ms(self, value):
        self.time_ms = value
        if self.time_ms == -1:
            self.labelTime.setText(constants["time-undefined"])
        else:
            self.labelTime.setText(ms_to_format(self.time_ms))


class CaptureWidget(QWidget):
    def __init__(self, playerWidget):
        super().__init__()

        self.playerWidget = playerWidget

        self.index = 0
        self.times = [[-1, -1]]

        self.buttonPreviousKeyframe = PushButton("K-")
        self.buttonPreviousKeyframe.setToolTip("Previous Keyframe")
        self.buttonPreviousKeyframe.setDisabled(True)
        self.buttonPreviousKeyframe.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonPreviousKeyframe.clicked.connect(self.on_previous_keyframe)

        self.buttonNextKeyframe = PushButton("K+")
        self.buttonNextKeyframe.setToolTip("Next Keyframe")
        self.buttonNextKeyframe.setDisabled(True)
        self.buttonNextKeyframe.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonNextKeyframe.clicked.connect(self.on_next_keyframe)

        self.labelIndex = QLabel(self.get_index_text())
        self.labelIndex.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelIndex.setFixedSize(QSize(constants["button-size"]*3, constants["button-size"]*2))

        self.buttonPrevious = PushButton("<")
        self.buttonPrevious.setToolTip("Previous")
        self.buttonPrevious.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonPrevious.clicked.connect(self.on_previous)

        self.buttonNext = PushButton(">")
        self.buttonNext.setToolTip("Next")
        self.buttonNext.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonNext.clicked.connect(self.on_next)

        self.buttonMoveLeft = PushButton("<<")
        self.buttonMoveLeft.setToolTip("Move Left")
        self.buttonMoveLeft.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonMoveLeft.clicked.connect(self.on_move_left)

        self.buttonMoveRight = PushButton(">>")
        self.buttonMoveRight.setToolTip("Move Right")
        self.buttonMoveRight.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonMoveRight.clicked.connect(self.on_move_right)

        self.buttonRemove = PushButton("X")
        self.buttonRemove.setToolTip("Remove")
        self.buttonRemove.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonRemove.clicked.connect(self.on_remove)

        self.buttonAdd = PushButton("+")
        self.buttonAdd.setToolTip("Add")
        self.buttonAdd.setFixedSize(QSize(constants["button-size"], constants["button-size"]))
        self.buttonAdd.clicked.connect(self.on_add)

        self.startCaptureTimeWidget = CaptureTimeWidget(self.playerWidget)
        self.startCaptureTimeWidget.callback = self.startCaptureTimeCallback

        self.endCaptureTimeWidget = CaptureTimeWidget(self.playerWidget)
        self.endCaptureTimeWidget.callback = self.endCaptureTimeCallback

        columnIndex = 0
        self.layout = QGridLayout()
        self.layout.addWidget(self.buttonNextKeyframe, 0, columnIndex)
        self.layout.addWidget(self.buttonPreviousKeyframe, 1, columnIndex)
        columnIndex += 1
        self.layout.addWidget(self.labelIndex, 0, columnIndex, 2, 1)
        columnIndex += 1
        self.layout.addWidget(self.buttonPrevious, 0, columnIndex)
        self.layout.addWidget(self.buttonMoveLeft, 1, columnIndex)
        columnIndex += 1
        self.layout.addWidget(self.buttonNext, 0, columnIndex)
        self.layout.addWidget(self.buttonMoveRight, 1, columnIndex)
        columnIndex += 1
        self.layout.addWidget(self.buttonAdd, 0, columnIndex)
        self.layout.addWidget(self.buttonRemove, 1, columnIndex)
        columnIndex += 1
        self.layout.addWidget(self.startCaptureTimeWidget, 0, columnIndex)
        self.layout.addWidget(self.endCaptureTimeWidget, 1, columnIndex)
        self.layout.setColumnStretch(columnIndex, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

        self.query_keyframes()

    # Function: Start capture time callback function.
    def startCaptureTimeCallback(self):
        self.times[self.index][0] = self.startCaptureTimeWidget.time_ms

    # Function: End capture time callback function.
    def endCaptureTimeCallback(self):
        self.times[self.index][1] = self.endCaptureTimeWidget.time_ms

    # Function: Get index text.
    def get_index_text(self):
        return "" + str(self.index + 1) + " out of " + str(len(self.times)) + ""

    # Function: Update index GUI.
    def update_index_GUI(self):
        self.labelIndex.setText(self.get_index_text())

    # Function: Update times GUI.
    def update_times_GUI(self):
        self.startCaptureTimeWidget.set_time_ms(self.times[self.index][0])
        self.endCaptureTimeWidget.set_time_ms(self.times[self.index][1])

    # Function: On next.
    def on_next(self):
        if self.index + 1 < len(self.times):
            self.index += 1
        self.update_index_GUI()
        self.update_times_GUI()

    # Function: On previous.
    def on_previous(self):
        if self.index > 0:
            self.index -= 1
        self.update_index_GUI()
        self.update_times_GUI()

    # Function: On add.
    def on_add(self):
        self.index += 1
        self.times.insert(self.index, [-1, -1])
        self.update_index_GUI()
        self.update_times_GUI()

    # Function: On remove.
    def on_remove(self):
        if len(self.times) > 1:
            self.times.pop(self.index)
            if self.index > 0:
                self.index -= 1
        self.update_index_GUI()
        self.update_times_GUI()

    # Function: On move right.
    def on_move_right(self):
        if self.index + 1 < len(self.times):
            self.times[self.index], self.times[self.index + 1] = self.times[self.index + 1], self.times[self.index]
            self.index += 1
            self.update_index_GUI()
            self.update_times_GUI()

    # Function: On move left.
    def on_move_left(self):
        if self.index > 0:
            self.times[self.index], self.times[self.index - 1] = self.times[self.index - 1], self.times[self.index]
            self.index -= 1
            self.update_index_GUI()
            self.update_times_GUI()

    # Function: On next keyframe.
    def on_next_keyframe(self):
        i = bisect.bisect_right(self.keyframes, self.playerWidget.player.position())
        if (i < len(self.keyframes)):
            self.playerWidget.pause()
            self.playerWidget.seek(self.keyframes[i])

    # Function: On previous keyframe.
    def on_previous_keyframe(self):
        i = bisect.bisect_left(self.keyframes, self.playerWidget.player.position()) - 1
        if i >= 0:
            self.playerWidget.pause()
            self.playerWidget.seek(self.keyframes[i])

    # Function: Keyframes queried.
    def keyframes_queried(self, status, results):
        if status == 0:
            self.keyframes = self.clean_keyframes(results[0])
            self.buttonNextKeyframe.setEnabled(True)
            self.buttonPreviousKeyframe.setEnabled(True)
        else:
            cmdln.error("Failed to query keyframes.")

    # Function: Clean keyframes.
    def clean_keyframes(self, keyframes):
        keyframes = keyframes.strip()
        keyframes = re.split(r'\n+', keyframes)
        for i in range(len(keyframes)):
            keyframes[i] = int(float(keyframes[i]) * 1000) + 1
        return keyframes

    # Function: Query keyframes.
    def query_keyframes(self):
        cmds = [ffmpeg.create_cmd("keyframes", {
            "input" :  '"' + self.playerWidget.player.get_media_path() + '"'
        })]
        run(cmds, self.keyframes_queried)

    # API: Get times.
    def get_times(self):
        return self.times