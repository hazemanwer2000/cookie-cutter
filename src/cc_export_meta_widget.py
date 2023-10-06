

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from cc_constants import constants
from cc_assets import assets

from cc_export_widget import *

from util_qt import createScrollArea, asset_path, PushButton
from util import run_batch

import ffmpeg

import subprocess

class ExportMetaWidget(QWidget):
    def __init__(self, captureWidget):
        super().__init__()

        self.captureWidget = captureWidget

        self.exportWidget = ExportWidget()

        self.buttonExport = PushButton("Export")
        self.buttonExport.setFixedHeight(constants["option-height"])
        self.buttonExport.clicked.connect(self.on_export)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(createScrollArea(self.exportWidget))
        self.layout.addWidget(self.buttonExport)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

    # Function: On export button clicked.
    def on_export(self):
        self.captureWidget.playerWidget.pause()

        summary = self.exportWidget.summary()
        summary['Times'] = self.captureWidget.get_times()
        summary['Path'] = self.captureWidget.playerWidget.player.get_media_path()

        run_batch(ffmpeg.options_to_cmds(summary), asset_path(assets["batch"]))