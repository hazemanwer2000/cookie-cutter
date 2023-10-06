
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from cc_constants import constants

from util_qt import ComboBox, LineEdit

# Class: 'dic' should contain (name, callback, dependency)
class OptionWidget(QWidget):
    def __init__(self, dic):
        super().__init__()

        self.layout = QHBoxLayout()

        self.name = dic["name"]

        if dic.get("dependency") != None:
            self.dependency = dic["dependency"]

        self.label = QLabel(dic["name"])
        self.label.setFixedWidth(constants["option-label-size"])
        self.label.setFixedHeight(constants["option-height"])
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label)
        self.layout.setAlignment(self.label, Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def callbackRelay(self):
        self.callback()

# Class: 'dic' should contain (+, args)
class OptionSelectWidget(OptionWidget):
    def __init__(self, dic):
        super().__init__(dic)

        self.comboBox = ComboBox()
        self.comboBox.addItems(dic["args"])
        self.comboBox.setFixedWidth(constants["option-size"])
        self.comboBox.setFixedHeight(constants["option-height"])
        self.comboBox.currentIndexChanged.connect(self.callbackRelay)

        self.layout.addWidget(self.comboBox)
        self.layout.setAlignment(self.comboBox, Qt.AlignmentFlag.AlignLeft)

    def get_arg(self):
        return self.comboBox.currentText()

    def summary(self):
        return [self.name, self.get_arg()] 

# Class: 'dic' should contain (+)
class OptionYesNoWidget(OptionSelectWidget):
    def __init__(self, dic):
        dic["args"] = ["No", "Yes"]
        super().__init__(dic)

# Class: 'dic' should contain (+, [placeholder])
class OptionInputWidget(OptionWidget):
    def __init__(self, dic):
        super().__init__(dic)

        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(constants["option-size"])
        self.lineEdit.setFixedHeight(constants["option-height"])
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lineEdit.textChanged.connect(self.callbackRelay)
        
        if dic.get("placeholder") != None:
            self.lineEdit.setPlaceholderText(dic["placeholder"])

        self.layout.addWidget(self.lineEdit)
        self.layout.setAlignment(self.lineEdit, Qt.AlignmentFlag.AlignLeft)

    def get_arg(self):
        return self.lineEdit.text()

    def summary(self):
        return [self.name, self.get_arg()]