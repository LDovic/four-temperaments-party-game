import simpleaudio as audio
from wavinfo import WavInfoReader
from constants import *
from button import *

class MusicPlayer():
    def __init__(self):
        self.tracks = self.create_tracks()
        self.track_index = 0
        self.no_of_tracks = self.get_number_of_tracks()
        self.now_playing = False

        """Music player buttons"""
        self.musicplayer_secondary_buttons = []

        self.track_info = Button("Stopped", (0, 0), WHITE, BUTTON_FONT_SIZE)

        self.musicplayer_secondary_buttons.append(self.track_info)

    def get_number_of_tracks(self):
        num = 0
        contents = os.listdir(SOUNDTRACK)
        for item in contents:
            if AUDIO_FILE_TYPE in item:
                num += 1
        return num

    def create_tracks(self):
        tracks = []
       
        contents = os.listdir(SOUNDTRACK)

        for item in contents:
            if AUDIO_FILE_TYPE in item:
                track = {}
                metadata = WavInfoReader(SOUNDTRACK + item)
                track['title'] = metadata.info.title
                track['artist'] = metadata.info.artist
                track['genre'] = metadata.info.genre
                track['track'] = (audio.WaveObject.from_wave_file(SOUNDTRACK + item))
                tracks.append(track)

        return tracks

    def get_genre(self):
       try:
           return self.now_playing['genre']
       except TypeError:
           return False

    def change_track(self):
       self.stop()
       self.track_index += 1       
       if self.track_index >= self.no_of_tracks:
           self.track_index = 0
       self.play()

    def stop(self):
       try:
           self.now_playing = False
           self.track_obj.stop()
       except AttributeError:
           pass

    def play(self):
       self.now_playing = self.tracks[self.track_index]
       self.track_obj = self.tracks[self.track_index]['track'].play()

    def has_stopped(self):
       if self.now_playing is not False:
           if not self.track_obj.is_playing():
               self.change_track()
