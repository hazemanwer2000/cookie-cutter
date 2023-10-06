
import sys, os

import cmdln

from cc_player_widget import PlayerWidget
from cc_capture_widget import CaptureWidget
from cc_export_meta_widget import ExportMetaWidget
from cc_assets import assets
from cc_constants import constants
from util import video_exists, txt_from_file
from util_qt import asset_path
import ffmpeg

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(constants['app']['minimum-width'], constants['app']['minimum-height'])
        self.setWindowTitle("Cookie Cutter'")
        self.setWindowIcon(QIcon(asset_path(assets['icon']['window'])))

        self.playerWidget = PlayerWidget()
        self.playerWidget.load(cmdln.args['i'][0])
        self.playerWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self.captureWidget = CaptureWidget(self.playerWidget)
        self.captureWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.exportMetaWidget = ExportMetaWidget(self.captureWidget)
        self.exportMetaWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.layout = QGridLayout()

        self.layout.addWidget(self.playerWidget, 0, 0)
        self.layout.addWidget(self.captureWidget, 1, 0)
        self.layout.addWidget(self.exportMetaWidget, 0, 1, 2, 1)
        self.layout.setColumnStretch(0, 1)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)

        self.setCentralWidget(self.centralWidget)

        self.setFocus()

    def closeEvent(self, event):
        ffmpeg.clean_tmp_dir()
        with open(os.path.join(ffmpeg.tmp_dir, 'tmp.txt'), 'w') as f:
            f.write('Damn, git!')
        raise KeyboardInterrupt()    # Note: To kill all threads.
    
    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            self.playerWidget.adjust_volume(constants['app']['volume-step']['wheel'])
        else:
            self.playerWidget.adjust_volume(-1*constants['app']['volume-step']['wheel'])

    def keyPressEvent(self, e):
        ekey = e.key()
        ekeys = constants["app"]["key"]
        if ekey in ekeys.values():
            index = [i for i in ekeys.keys() if ekeys[i] == ekey][0]
            fcnName = 'key_' + index.replace('-', '_')
            getattr(self, fcnName)()

    def key_mute(self):
        self.playerWidget.toggle_mute()

    def key_play(self):
        self.playerWidget.toggle()
    
    def key_skip_high_forward(self):
        self.playerWidget.skip(constants['app']['skip-ms']['high'])

    def key_skip_high_backward(self):
        self.playerWidget.skip(-1*constants['app']['skip-ms']['high'])

    def key_skip_medium_forward(self):
        self.playerWidget.skip(constants['app']['skip-ms']['medium'])

    def key_skip_medium_backward(self):
        self.playerWidget.skip(-1*constants['app']['skip-ms']['medium'])

    def key_skip_low_forward(self):
        self.playerWidget.skip(constants['app']['skip-ms']['low'])

    def key_skip_low_backward(self):
        self.playerWidget.skip(-1*constants['app']['skip-ms']['low'])

    def key_skip_tiny_forward(self):
        self.playerWidget.skip(constants['app']['skip-ms']['tiny'])

    def key_skip_tiny_backward(self):
        self.playerWidget.skip(-1*constants['app']['skip-ms']['tiny'])

    def key_skip_frame(self):
        self.playerWidget.next_frame()

    def key_volume_lower(self):
        self.playerWidget.adjust_volume(-1*constants['app']['volume-step']['key'])

    def key_volume_higher(self):
        self.playerWidget.adjust_volume(constants['app']['volume-step']['key'])

    def enterEvent(self, e):
        self.setFocus()
    
    def leaveEvent(self, e):
        self.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(txt_from_file(asset_path(assets["stylesheet"])))

    if cmdln.args.get('i') != None and len(cmdln.args['i']) == 1:
        if video_exists(cmdln.args['i'][0]):
            window = MainWindow()
            window.show()
        else:
            cmdln.error("File does not exist, or is not a playable.")
    else:
        cmdln.error("Must pass a video file as argument (Option: -i).")

    sys.exit(app.exec())