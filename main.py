import sys, os
import pygame
from pygame.locals import *
from Constraints import *
from Scene.CameraScene import CameraScene
from Scene.StartupScene import StartupScene
from Scene.MovieScene import MovieScene
from Scene.FileSelectScene import FileSelectScene
from loguru import logger
from Library import log_dir, ymd, is_debug, jornal_log_path, filter_able_path
from Library.Redis import Redis
from Library.AWS import Aws


class WindowLoop:

    running = True
    current_scene = None
    recorder = None
    redis = None
    aws = None

    def __init__(self):
        pygame.init()  # 初期化
        pygame.display.set_caption("Drive Recorder")  # ウィンドウタイトル
        if is_debug():
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

        self.redis = Redis(window=self)
        self.redis.start_ups_subscribe()

        self.current_scene = StartupScene(window=self)

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

    def switch_scene(self, name, data = None):
        if name == CAMERA_SCENE_NAME:
            self.current_scene = CameraScene(window=self, recorder=self.recorder)
        elif name == FILE_SELECT_SCENE_NAME:
            self.current_scene = FileSelectScene(window=self, data=data)
        elif name == MOVIE_SCENE_NAME:
            self.current_scene = MovieScene(window=self, data=data)

    def set_recorder(self, recorder):
        self.recorder = recorder

    def received_remove_external_power_supply_signal(self):
        logger.info(f"received_remove_external_power_supply_signal")
        if self.recorder is not None:
            self.recorder.stop_AV_recording()
            # TODO AVI attach Audio

        aws = Aws()
        # Jornal Log 保存
        jlp = jornal_log_path()
        os.system(f"sudo journalctl -u my_app.service -S today > {jlp}")
        aws.process_s3_upload_files([jlp], Aws.LOG_DIR)
        # Application Log 保存
        log_file_paths = filter_able_path(log_dir(), [])
        aws.process_s3_upload_files(log_file_paths, Aws.LOG_DIR)
        # プロセス終了待ち合わせ
        for proc in aws.upload_process_list:
            proc.join()

        os.system('sudo shutdown -h now')


def main():
    logger.add(f'{log_dir()}app_{ymd()}.log')
    wl = WindowLoop()
    wl.loop()


if __name__ == "__main__":
    main()
