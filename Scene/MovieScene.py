import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *
from moviepy.editor import *
from Library import data_dir
from Library.pyvidplayer import Video
from Library.UI import UI


class MovieScene(Scene):

    window = None
    screen = None

    def __init__(self, window, path):
        self.path = path
        self.window = window
        self.screen = window.screen
        self.isPlaying = False
        self.vid = Video(data_dir()+path+'/playlist.m3u8')
        self.vid.set_size((WINDOW_WIDTH, WINDOW_HEIGHT))
        print(self.vid.get_file_data())

        self.play_image = UI.slice_icon_video_player()
        self.play_image_rect = UI.centered_rect(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, self.play_image.get_width(), self.play_image.get_height())
        self.vid.draw(self.screen, (0, 0), force_draw=False)

    def loop(self):

        if self.isPlaying:
            self.vid.draw(self.screen, (0, 0), force_draw=False)
        else:
            self.screen.blit(self.play_image, self.play_image_rect)


    def click_notify(self, position):
        if self.play_image_rect.collidepoint(position):
            self.isPlaying = not self.isPlaying

    def before_finish(self):
        pass