import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *
from Library.CameraSettings import CameraSettings
import cv2, time, os
from Library.Recorder import Recorder
from loguru import logger
from dotenv import load_dotenv
load_dotenv()  # .env読込


class CameraScene(Scene):

    BUTTON_LEFT_MARGIN = 10
    BUTTON_TOP_MARGIN = 10
    outside_btn = None
    inside_btn = None

    recoder = None

    is_locked = False

    def __init__(self, window):

        self.recoder = Recorder()
        self.recoder.start_AV_recording()

        self.window = window
        self.screen = window.screen
        self.sprite_group = pygame.sprite.RenderUpdates()

        self.inside_camera_src = os.getenv('INSIDE_CAMERA')
        self.outside_camera_src = os.getenv('OUTSIDE_CAMERA')

        self.current_camera_src = self.outside_camera_src

        history_btn = self.CameraSceneButton(">> History", Rect(self.BUTTON_LEFT_MARGIN, WINDOW_HEIGHT - 40, 110, 50),
                                             self.history_button_clicked)
        self.sprite_group.add(history_btn)

        self.setup_camera()

    def setup_camera(self):

        rect = Rect(self.BUTTON_LEFT_MARGIN, self.BUTTON_TOP_MARGIN, 140, 50)
        if self.current_camera_src == self.inside_camera_src:
            self.outside_btn = self.CameraSceneButton(">> Outside Camera", rect, self.switch_outside_camera)
            self.sprite_group.add(self.outside_btn)
            self.sprite_group.remove(self.inside_btn)
        elif self.current_camera_src == self.outside_camera_src:
            self.inside_btn = self.CameraSceneButton(">> Inside Camera", rect, self.switch_inside_camera)
            self.sprite_group.add(self.inside_btn)
            self.sprite_group.remove(self.outside_btn)

    # Windowクラスが実行するループ
    def loop(self):
        self.screen.fill((255, 255, 255))  # 背景色
        frame = None
        if self.current_camera_src == self.inside_camera_src:
            frame = self.recoder.inside_video_thread.frame
        elif self.current_camera_src == self.outside_camera_src:
            frame = self.recoder.outside_video_thread.frame
        if frame is not None:
            frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            frame = CameraSettings.convert_opencv_img_to_pygame(opencv_image=frame)
            self.screen.blit(frame, (0, 0))

        for sprite in self.sprite_group:
            sprite.draw(self.screen)

    # Windowクラスからタップ位置のお知らせがくる
    def click_notify(self, position):
        if not self.is_locked:
            for s in self.sprite_group:
                if s.rect.collidepoint(position):
                    self.is_locked = True
                    s.clicked()
                    self.is_locked = False
                    break

    # Windowクラスからアプリケーション終了のお知らせがくる
    def before_finish(self):
        self.defer()

    # Historyボタンがクリックされたら、シーンの切り替え命令を出す
    def history_button_clicked(self):
        self.window.switch_scene(FILE_SELECT_SCENE_NAME)

    def switch_inside_camera(self):
        self.current_camera_src = self.inside_camera_src
        self.setup_camera()

    def switch_outside_camera(self):
        self.current_camera_src = self.outside_camera_src
        self.setup_camera()

    def defer(self):
        logger.info("recording Finish")
        self.recoder.stop_AV_recording()


    # Cameraシーンボタンの実装
    class CameraSceneButton(pygame.sprite.Sprite):

        def __init__(self, str, rect, callback, *groups):
            super().__init__(*groups)

            self.rect = rect
            self.callback = callback

            font = pygame.font.SysFont(None, 30)
            font_color = (0, 145, 255)
            self.content = font.render(str, True, font_color)

        def draw(self, screen):
            screen.blit(self.content, self.rect)

        def clicked(self):
            self.callback()
