import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *
from Library.CameraSettings import CameraSettings
import cv2
import os
from Library.UI import UI
from Library.SpriteSheet import SpriteSheet
from dotenv import load_dotenv
load_dotenv()  # .env読込


class CameraScene(Scene):
    window = None
    screen = None
    sprite_group = None

    def __init__(self, window):

        self.window = window
        self.screen = window.screen
        self.sprite_group = pygame.sprite.RenderUpdates()

        btn = self.FinishButton(self)
        self.sprite_group.add(btn)

        self.frame0 = cv2.VideoCapture(os.getenv('INSIDE_CAMERA'))
        self.frame1 = cv2.VideoCapture(os.getenv('OUTSIDE_CAMERA'))

        CameraSettings.set(frame=self.frame0)
        CameraSettings.set(frame=self.frame1)

    # Windowクラスが実行するループ
    def loop(self):

        self.screen.fill((255, 255, 255))  # 背景色

        ret0, img0 = self.frame0.read()
        ret1, img1 = self.frame1.read()

        if ret0:
            img0 = cv2.resize(img0, (CAPTURE_IMAGE_WIDTH, CAPTURE_IMAGE_HEIGHT))
            pygame_image1 = CameraSettings.convert_opencv_img_to_pygame(opencv_image=img0)
            self.screen.blit(pygame_image1, (0, 0))

        if ret1:
            img1 = cv2.resize(img1, (CAPTURE_IMAGE_WIDTH, CAPTURE_IMAGE_HEIGHT))
            pygame_image2 = CameraSettings.convert_opencv_img_to_pygame(opencv_image=img1)
            self.screen.blit(pygame_image2, (CAPTURE_IMAGE_WIDTH, 0))

        for sprite in self.sprite_group:
            sprite.draw(self.screen)

    # Windowクラスからタップ位置のお知らせがくる
    def click_notify(self, position):
        for s in self.sprite_group:
            if s.rect.collidepoint(position):
                s.clicked()
                break

    # Windowクラスからアプリケーション終了のお知らせがくる
    def before_finish(self):
        self.defer()

    # Finishボタンがクリックされたら、シーンの切り替え命令を出す
    def finish_button_clicked(self):
        self.window.switch_scene(FILE_SELECT_SCENE_NAME)
        self.defer()

    def defer(self):
        self.frame0.release()
        self.frame1.release()
        cv2.destroyAllWindows()

    # Finishボタンの実装
    class FinishButton(pygame.sprite.Sprite):
        content = None
        content_rect = None
        background = None

        scene = None

        WIDTH = 100
        HEIGHT = 30
        MARGIN_BOTTOM = 20

        @staticmethod
        def string_center(center_position, font_size):
            font_width = font_size[0]
            font_height = font_size[1]
            center_x = center_position[0]
            center_y = center_position[1]
            return center_x - font_width / 2, center_y - font_height / 2

        def __init__(self, scene, *groups):
            super().__init__(*groups)

            self.scene = scene

            font = pygame.font.SysFont(None, 16)
            font_color = (0, 0, 0)
            str = "History"
            self.content = font.render(str, True, font_color)

            font_size = font.size(str)
            content_center = UI.string_center(
                (WINDOW_WIDTH / 2, CAPTURE_IMAGE_HEIGHT + self.MARGIN_BOTTOM + self.HEIGHT / 2), font_size)
            self.content_rect = Rect(content_center[0], content_center[1], font_size[0], font_size[1])

            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background.fill(pygame.Color('dodgerblue1'))
            # box center
            self.rect = Rect(WINDOW_WIDTH / 2 - self.WIDTH / 2, CAPTURE_IMAGE_HEIGHT + self.MARGIN_BOTTOM, self.WIDTH,
                             self.HEIGHT)

        def draw(self, screen):
            screen.blit(self.background, self.rect)
            screen.blit(self.content, self.content_rect)

        def clicked(self):
            self.scene.finish_button_clicked()
