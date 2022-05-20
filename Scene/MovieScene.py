import pygame
from pygame.locals import *
from Scene import Scene
from Constraints import *
import cv2
from Library.CameraSettings import CameraSettings
from Library import data_dir
from Library.UI import UI


class MovieScene(Scene):

    window = None
    screen = None
    fps = None

    def __init__(self, window, data):
        self.path = data['path']
        self.file_select_page = data['page']
        self.window = window
        self.screen = window.screen
        self.back_surface, self.back_rect = UI.create_back()

        self.isPlaying = False
        self.cap = cv2.VideoCapture(data_dir()+self.path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.play_image = UI.slice_icon_video_player()
        self.play_image_rect = UI.centered_rect(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, self.play_image.get_width(), self.play_image.get_height())

        self.screen.fill((255, 255, 255))  # 背景色

    def loop(self):
        if self.isPlaying:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
                frame = CameraSettings.convert_opencv_img_to_pygame(opencv_image=frame)
                self.screen.blit(frame, (0, 0))
                pygame.time.wait(1/self.fps)
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