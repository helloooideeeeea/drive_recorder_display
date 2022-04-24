import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *
import cv2


class CameraScene(Scene):
    window = None
    screen = None
    sprite_group = None

    @staticmethod
    def decode_fourcc(v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

    @staticmethod
    def camera_setting(frame):

        # フォーマット・解像度・FPSの設定
        frame.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'P', 'E', 'G'))
        frame.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        frame.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame.set(cv2.CAP_PROP_FPS, 30)

        # フォーマット・解像度・FPSの取得
        fourcc = CameraScene.decode_fourcc(frame.get(cv2.CAP_PROP_FOURCC))
        width = frame.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = frame.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = frame.get(cv2.CAP_PROP_FPS)
        print("fourcc:{} fps:{}　width:{}　height:{}".format(fourcc, fps, width, height))

    def __init__(self, window):

        self.window = window
        self.screen = window.screen
        self.sprite_group = pygame.sprite.RenderUpdates()

        btn = self.FinishButton(self)
        self.sprite_group.add(btn)

        self.frame0 = cv2.VideoCapture(CAMERA_ID_1)
        self.frame1 = cv2.VideoCapture(CAMERA_ID_2)

        self.camera_setting(frame=self.frame0)
        self.camera_setting(frame=self.frame1)

    # Windowクラスが実行するループ
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
        self.window.switch_scene(SETTING_SCENE_NAME)
        self.defer()

    def defer(self):
        self.frame0.release()
        self.frame1.release()
        cv2.destroyAllWindows()

    @staticmethod
    def convert_opencv_img_to_pygame(opencv_image):
        opencv_image = opencv_image[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')
        return pygame_image

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
            str = "Finish"
            self.content = font.render(str, True, font_color)

            font_size = font.size(str)
            content_center = self.string_center(
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
