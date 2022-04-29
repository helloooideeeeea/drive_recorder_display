import sys
import pygame
from pygame.locals import *
from Constraints import *
from Scene.CameraScene import CameraScene
from Scene.SettingScene import SettingScene
from Scene.StartupScene import StartupScene
from loguru import logger
from Library import log_dir,ymd


class WindowLoop:

    running = True
    current_scene = None

    def __init__(self):
        pygame.init()  # 初期化
        pygame.display.set_caption("Drive Recorder")  # ウィンドウタイトル
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # ウィンドウサイズ

        self.current_scene = CameraScene(window=self)

    def loop(self):

        clock = pygame.time.Clock()
        while self.running:

            clock.tick(20)  # 1秒間に20フレーム

            self.current_scene.loop()

            pygame.display.update()  # 画面更新

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.current_scene.click_notify(position=pos)

                elif event.type == QUIT:  # 終了処理
                    self.current_scene.before_finish()
                    pygame.quit()
                    sys.exit()

    def switch_scene(self, name):
        if name == CAMERA_SCENE_NAME:
            self.current_scene = CameraScene(window=self)
        elif name == SETTING_SCENE_NAME:
            self.current_scene = SettingScene(window=self)


def main():
    logger.add(f'{log_dir()}app_{ymd()}.log')
    wl = WindowLoop()
    wl.loop()


if __name__ == "__main__":
    main()
