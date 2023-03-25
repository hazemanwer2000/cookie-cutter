
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from cc_constants import constants

from cc_option_widget import *

class ExportWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.customSetup()

        self.layout = QVBoxLayout()

        self.insertAll()

        self.setLayout(self.layout)
        self.layout.setContentsMargins(5, 5, 5, 5)

    # Function: Insert header.
    def insertHeader(self, name):
        label = QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedWidth(constants["option-label-size"] + constants["option-size"])
        label.setFixedHeight(constants["option-height"])
        self.layout.addWidget(label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # Function: Insert option.
    def insertOption(self, option):
        self.layout.addWidget(option)

    # Function: Insert all (headers + options).
    def insertAll(self):
        for menu in self.options:
            self.insertHeader(menu["name"])
            widgets = menu["widgets"]
            for key in widgets.keys():
                self.insertOption(widgets[key])
        self.updateGUI()

    # Function: Customize your setup.
    def customSetup(self):
        self.options = [
            {
                "name" : "Format",
                "widgets" : {
                    "Type" : OptionSelectWidget({
                        "name" : "Type",
                        "args" : ["Video", "GIF"]
                    }),
                    "Re-encode" : OptionYesNoWidget({
                        "name" : "Re-encode",
                        "dependency" : [
                            ["Type", ["Video"]]
                        ]
                    }),
                    "Extension" : OptionInputWidget({
                        "name" : "Extension",
                        "placeholder" : "(e.g: mp4)",
                        "dependency" : [
                            ["Type", ["Video"]],
                            ["Re-encode", ["Yes"]]
                        ]
                    }),
                    "CRF" : OptionInputWidget({
                        "name" : "CRF",
                        "placeholder" : "(e.g: 17)",
                        "dependency" : [
                            ["Type", ["Video"]],
                            ["Re-encode", ["Yes"]]
                        ]
                    }),
                    "Mute" : OptionYesNoWidget({
                        "name" : "Mute",
                        "dependency" : [
                            ["Type", ["Video"]]
                        ]
                    }),
                    "FPS" : OptionInputWidget({
                        "name" : "FPS",
                        "placeholder" : "(e.g: 30)",
                        "dependency" : [
                            ["Type", ["GIF"]]
                        ]
                    }),
                    "Playback" : OptionInputWidget({
                        "name" : "Playback",
                        "placeholder" : "(e.g: 0.5)",
                        "dependency" : [
                            ["Type", ["GIF"]]
                        ]
                    }),
                    "Width" : OptionInputWidget({
                        "name" : "Width",
                        "placeholder" : "(e.g: 800)",
                        "dependency" : [
                            ["Type", ["GIF"]],
                            ["Height", [""]]
                        ]
                    }),
                    "Height" : OptionInputWidget({
                        "name" : "Height",
                        "placeholder" : "(e.g: 450)",
                        "dependency" : [
                            ["Type", ["GIF"]],
                            ["Width", [""]]
                        ]
                    })
                },
            },{
                "name" : "Filters",
                "widgets" : {
                    "Fade" : OptionInputWidget({
                        "name" : "Fade",
                        "placeholder" : "(e.g: 1)"
                    }),
                    "Crop (W)" : OptionInputWidget({
                        "name" : "Crop (W)",
                        "placeholder" : "(i.e: %)"
                    }),
                    "Crop (H)" : OptionInputWidget({
                        "name" : "Crop (H)",
                        "placeholder" : "(i.e: %)"
                    }),
                    "Crop (X)" : OptionInputWidget({
                        "name" : "Crop (X)",
                        "placeholder" : "(i.e: %)"
                    }),
                    "Crop (Y)" : OptionInputWidget({
                        "name" : "Crop (Y)",
                        "placeholder" : "(i.e: %)"
                    })
                }
            }
        ]

        self.all_options = {}                       # Note: List of all options
        for menu in self.options:
            self.all_options.update(menu["widgets"])

        for key in self.all_options:             # Note: Add 'callback' to all options
            self.all_options[key].callback = self.updateGUI

    # API: Update GUI.
    def updateGUI(self):
        for key in self.all_options:
            option = self.all_options[key]
            if hasattr(option, 'dependency'):
                depCheck = True
                for dep in option.dependency:    # Note: For each dependency.
                    depKey = dep[0]
                    depList = dep[1]
                    if self.all_options[depKey].get_arg() not in depList:
                        depCheck = False
                        break
                if depCheck:
                    option.show()
                else:
                    option.hide()
            else:
                option.show()
        
        self.summary()

    # API: Get options summary.
    def summary(self):
        dic = {}
        for option in self.all_options.values():
            if option.isVisible():
                lst = option.summary()
                dic[lst[0]] = lst[1]
        return dic