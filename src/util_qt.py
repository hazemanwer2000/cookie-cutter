
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from run_processes import RunProcesses

from util import get_script_dir
import os

# API: Create horizontal spacing widget.
def createHorizontalSpacing(spacing):
    widget = QWidget()
    widget.setFixedSize(QSize(spacing, 1))
    return widget

# API: Launch runnable.
def run(cmds, callback):
    task = RunProcesses(cmds)
    task.signals.done.connect(callback)
    QThreadPool.globalInstance().start(task)

# API: Create scroll-area.
def createScrollArea(widget):
    scrollArea = QScrollArea()
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scrollArea.setWidgetResizable(True)
    scrollArea.setWidget(widget)
    return scrollArea

# API: Get asset's real path.
def asset_path(relative):
    return os.path.join(get_script_dir(), relative)

# Class: 'QPushButton' shadow.
class PushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

# Class: 'QSlider' shadow.
class Slider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

# Class: 'QComboBox' shadow.
class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

# Class: 'QLineEdit' shadow.
class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)