import sys
import pygame
from pygame.locals import *
import cv2

CAMERA_ID_1 = 0
CAMERA_ID_2 = 1
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480


class FinishButton(pygame.sprite.Sprite):

    content = None
    background = None

    def __init__(self, *groups):
        super().__init__(*groups)
        font = pygame.font.SysFont("notosanscjkjp", 16)
        font_color = (0, 0, 0)
        self.content = font.render("Finish", True, font_color)
        self.rect = Rect(0, 0, 100, 80)
        self.background = pygame.Surface((50, 30))
        self.background.fill(pygame.Color('dodgerblue1'))

    def draw(self, screen):
        screen.blit(self.background, self.rect)
        screen.blit(self.content, self.rect)

    def clicked(self):
        print("clicked")

class WindowLoop:
    CAPTURE_IMAGE_WIDTH = 400
    CAPTURE_IMAGE_HEIGHT = 267

    sprite_group = None
    running = True

    def __init__(self):
        pygame.init()  # 初期化
        pygame.display.set_caption("Drive Recorder")  # ウィンドウタイトル
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # ウィンドウサイズ
        self.sprite_group = pygame.sprite.RenderUpdates()

        btn = FinishButton()

        self.sprite_group.add(btn)

        self.frame0 = cv2.VideoCapture(CAMERA_ID_1)
        self.frame1 = cv2.VideoCapture(CAMERA_ID_2)

    def convert_opencv_img_to_pygame(self, opencv_image):
        opencv_image = opencv_image[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')
        return pygame_image

    def loop(self):

        clock = pygame.time.Clock()
        while self.running:

            clock.tick(30)  # 1秒間に30フレーム
            self.screen.fill((255, 255, 255))  # 背景色

            ret0, img0 = self.frame0.read()
            ret1, img1 = self.frame1.read()

            img0 = cv2.resize(img0, (self.CAPTURE_IMAGE_WIDTH, self.CAPTURE_IMAGE_HEIGHT))
            img1 = cv2.resize(img1, (self.CAPTURE_IMAGE_WIDTH, self.CAPTURE_IMAGE_HEIGHT))

            pygame_image1 = self.convert_opencv_img_to_pygame(opencv_image=img0)
            pygame_image2 = self.convert_opencv_img_to_pygame(opencv_image=img1)

            self.screen.blit(pygame_image1, (0, 0))
            self.screen.blit(pygame_image2, (self.CAPTURE_IMAGE_WIDTH, 0))

            for a in self.sprite_group:
                a.draw(self.screen)


            pygame.display.update()  # 画面更新

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    self.click_notify(pos)

                elif event.type == QUIT:  # 終了処理
                    self.frame0.release()
                    self.frame1.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    sys.exit()

    def click_notify(self, pos):

        for s in self.sprite_group:
            if s.rect.collidepoint(pos):
                s.clicked()
                break


def main():
    wl = WindowLoop()
    wl.loop()


if __name__ == "__main__":
    main()
