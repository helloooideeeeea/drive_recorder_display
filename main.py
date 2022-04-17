import sys
import pygame
from pygame.locals import *
from Constraints import *
from Scene.CameraScene import CameraScene


class WindowLoop:
    running = True
    current_scene = None

    def __init__(self):
        pygame.init()  # 初期化
        pygame.display.set_caption("Drive Recorder")  # ウィンドウタイトル
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # ウィンドウサイズ

        self.current_scene = CameraScene(screen=self.screen)

    def loop(self):

        clock = pygame.time.Clock()
        while self.running:

            clock.tick(30)  # 1秒間に30フレーム

            self.current_scene.loop()

            pygame.display.update()  # 画面更新

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.current_scene.click_notify(pos=pos)

                elif event.type == QUIT:  # 終了処理
                    self.current_scene.before_finish()
                    pygame.quit()
                    sys.exit()


def main():
    wl = WindowLoop()
    wl.loop()


if __name__ == "__main__":
    main()
