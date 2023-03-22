
import vlc, sys

# Variable: VLC instance.
VLC = vlc.Instance()

# Object: Manages a VLC player instance.
class Player:
    def __init__(self, frame):
        self.player = VLC.media_player_new()
        self.integrate(frame)
        self.path = None

    # Function: Integrate with 'QFrame'.
    def integrate(self, frame):
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(frame.winId())
        elif sys.platform == "win32":
            self.player.set_hwnd(frame.winId())
        else:
            raise Exception("Failed to integrate 'QFrame' with VLC player instance.")
        
    # API: Seek to time (in ms).
    def seek(self, time):
        self.player.set_time(time)

    # API: Get position (in ms).
    def position(self):
        return self.player.get_time()

    # API: Next frame.
    def next_frame(self):
        self.player.next_frame()

    # API: Load new file. 
    def load(self, path):
        self.path = path
        media = VLC.media_new(path)
        self.player.set_media(media)
        self.player.play()

    # API: Pause video.
    def pause(self):
        self.player.set_pause(True)

    # API: Play video (relaods if video has ended).
    def play(self):
        if self.player.get_state() == vlc.State.Ended:
            self.load(self.path)
        else:
            self.player.play()

    # API: Check if video is playing.
    def is_playing(self):
        return self.player.is_playing()
    
    # API: Check if video ended.
    def is_ended(self):
        return self.player.get_state() == vlc.State.Ended
    
    # API: Set audio volume (0-100)
    def set_volume(self, value):
        self.player.audio_set_volume(value)

    # API: Get loaded video path ('None' if not yet loaded).
    def get_media_path(self):
        return self.path
    
    # API: Get video length in ms ('None' if not yet loaded).
    def get_media_length(self):
        length = self.player.get_length()
        return length if length != 0 else None