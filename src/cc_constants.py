
from PyQt6.QtCore import *

constants = {
    "icon-size" : 18,
    "button-size" : 30,
    "time-undefined" : "NaN",
    "option-label-size" : 100,
    "option-size" : 125,
    "option-height" : 25,
    "hover-percentage-bar-horizontal-size" : 25,
    "hover-percentage-bar-vertical-size" : 40,
    "hover-percentage-bar-initial-text" : "0%",
    "hover-percentage-bar-added-symbol" : "%",

    "ffmpeg" : {
        "def-crf" : "17",
        "def-ext" : "mp4",
        "def-fade" : "0",
        "def-playback" : "1",
        "def-width" : "800",
        "tune-fade-offset" : 0,
        "tune-keyframe-start" : 0
    },

    "app" : {
        "minimum-width" : 750,
        "minimum-height" : 400,

        "key" : {
            "mute" : Qt.Key.Key_M,
            "play" : Qt.Key.Key_Space,
            
            "skip-high-forward" : Qt.Key.Key_Period,
            "skip-high-backward" : Qt.Key.Key_Comma,
            
            "skip-medium-forward" : Qt.Key.Key_Right,
            "skip-medium-backward" : Qt.Key.Key_Left,
            
            "skip-low-forward" : Qt.Key.Key_Apostrophe,
            "skip-low-backward" : Qt.Key.Key_Semicolon,

            "skip-tiny-forward" : Qt.Key.Key_BracketRight,
            "skip-tiny-backward" : Qt.Key.Key_BracketLeft,
            
            "skip-frame" : Qt.Key.Key_Slash,

            "volume-lower" : Qt.Key.Key_Down,
            "volume-higher" : Qt.Key.Key_Up
        },

        "skip-ms" : {
            "high" : 10000,
            "medium" : 3000,
            "low" : 1000,
            "tiny" : 150
        },

        "volume-step" : {
            "key" : 10,
            "wheel" : 10
        }
    },

    "cmd" : {
        "copy" : "copy"
    }
}