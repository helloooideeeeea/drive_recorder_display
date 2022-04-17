import pygame
from Scene import Scene
import cv2
from pygame.locals import *
from Constraints import *

class CameraScene(Scene):

    CAMERA_ID_1 = 0
    CAMERA_ID_2 = 1

    sprite_group = None
    screen = None

    def __init__(self, screen):

        self.screen = screen

        self.sprite_group = pygame.sprite.RenderUpdates()

        btn = self.FinishButton()
        self.sprite_group.add(btn)

        self.frame0 = cv2.VideoCapture(self.CAMERA_ID_1)
        self.frame1 = cv2.VideoCapture(self.CAMERA_ID_2)

    def loop(self):

        self.screen.fill((255, 255, 255))  # 背景色

        ret0, img0 = self.frame0.read()
        ret1, img1 = self.frame1.read()

        #
        img0 = cv2.resize(img0, (CAPTURE_IMAGE_WIDTH, CAPTURE_IMAGE_HEIGHT))
        img1 = cv2.resize(img1, (CAPTURE_IMAGE_WIDTH, CAPTURE_IMAGE_HEIGHT))

        #
        pygame_image1 = self.convert_opencv_img_to_pygame(opencv_image=img0)
        pygame_image2 = self.convert_opencv_img_to_pygame(opencv_image=img1)

        self.screen.blit(pygame_image1, (0, 0))
        self.screen.blit(pygame_image2, (CAPTURE_IMAGE_WIDTH, 0))

        for sprite in self.sprite_group:
            sprite.draw(self.screen)

    def click_notify(self, pos):
        for s in self.sprite_group:
            if s.rect.collidepoint(pos):
                s.clicked()
                break

    def before_finish(self):
        self.frame0.release()
        self.frame1.release()
        cv2.destroyAllWindows()

    @staticmethod
    def convert_opencv_img_to_pygame(opencv_image):
        opencv_image = opencv_image[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')
        return pygame_image

    class FinishButton(pygame.sprite.Sprite):
        content = None
        content_rect = None
        background = None
        background_rect = None

        WIDTH = 100
        HEIGHT = 30

        def __init__(self, *groups):
            super().__init__(*groups)
            font = pygame.font.SysFont(None, 16)
            font_color = (0, 0, 0)
            str = "Finish"
            self.content = font.render(str, True, font_color)
            # TODO 座標変換をわかりやすくする
            self.content_rect = Rect(WINDOW_WIDTH / 2 - self.WIDTH / 2 + font.size(str)[0], CAPTURE_IMAGE_HEIGHT + 10 + font.size(str)[1]/2, self.WIDTH,
                                        self.HEIGHT)

            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background.fill(pygame.Color('dodgerblue1'))
            self.rect = Rect(WINDOW_WIDTH / 2 - self.WIDTH / 2, CAPTURE_IMAGE_HEIGHT + 10, self.WIDTH,
                                        self.HEIGHT)

        def draw(self, screen):
            screen.blit(self.background, self.rect)
            screen.blit(self.content, self.content_rect)

        def clicked(self):
            print("clicked")
