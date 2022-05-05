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

    def __init__(self, window, data):
        self.path = data['path']
        self.file_select_page = data['page']
        self.window = window
        self.screen = window.screen
        self.back_surface, self.back_rect = UI.create_back()

        self.isPlaying = False
        self.vid = Video(data_dir()+self.path+'/playlist.m3u8')
        self.vid.set_size((WINDOW_WIDTH, WINDOW_HEIGHT))
        #print(self.vid.get_file_data())

        self.play_image = UI.slice_icon_video_player()
        self.play_image_rect = UI.centered_rect(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, self.play_image.get_width(), self.play_image.get_height())

        self.screen.fill((255, 255, 255))  # 背景色

    def loop(self):
        if self.isPlaying:
            self.vid.draw(self.screen, (0, 0), force_draw=False)
        else:
            self.screen.blit(self.play_image, self.play_image_rect)
        self.screen.blit(self.back_surface, self.back_rect)

    def click_notify(self, position):
        if self.play_image_rect.collidepoint(position):
            self.isPlaying = not self.isPlaying
            return
        if self.back_rect.collidepoint(position):
            self.window.switch_scene(FILE_SELECT_SCENE_NAME, data={'page': self.file_select_page})
            return

    def before_finish(self):
        pass