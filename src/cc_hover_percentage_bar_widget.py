
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from cc_constants import constants

# Class: 
class HoverPercentageBar(QLabel):
    def __init__(self, thickness, isHorizontal=True):
        super().__init__(constants['hover-percentage-bar-initial-text'], alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Setup mouse-hover event(s)
        self.setMouseTracking(True)
        if (isHorizontal):
            self.mouseMoveEventCallout = self.mouseMoveEventHorizontal
            self.setFixedHeight(thickness)
        else:
            self.mouseMoveEventCallout = self.mouseMoveEventVertical
            self.setFixedWidth(thickness)

    def mouseMoveEventHorizontal(self, e):
        perc = int((float(e.position().x()) / float(self.size().width())) * 100.0)
        self.setText(str(perc) + constants['hover-percentage-bar-added-symbol'])

    def mouseMoveEventVertical(self, e):
        perc = int((float(e.position().y()) / float(self.size().height())) * 100.0)
        self.setText(str(perc) + constants['hover-percentage-bar-added-symbol'])

    def mouseMoveEvent(self, e):
        self.mouseMoveEventCallout(e)

