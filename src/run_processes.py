
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import subprocess

class RunProcessesSignals(QObject):
    done = pyqtSignal(int, list)

class RunProcesses(QRunnable, QObject):
    signals = RunProcessesSignals()

    def __init__(self, cmds, shellState=True):
        super().__init__()

        self.cmds = cmds
        self.shellState = shellState
    
    @pyqtSlot()                      
    def run(self):
        lst = []
        for cmd in self.cmds:
            res = subprocess.run(cmd, capture_output=True, text=True, shell=self.shellState)
            lst.append(res.stdout)
            if res.returncode != 0:
                print(res.stderr)
                break

        self.signals.done.emit(res.returncode, lst)