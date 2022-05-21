import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *
from Library import data_dir, filter_able_path
from Library.UI import UI
from Library.Recorder import Recorder
from Library.AWS import Aws


class StartupScene(Scene):

    onlyOnce = True

    def __init__(self, window):

        self.window = window
        self.screen = window.screen
        self.sprite_group = pygame.sprite.RenderUpdates()

        self.label = self.LoadingLabel(self)
        self.sprite_group.add(self.label)

    def loop(self):

        self.screen.fill((255, 255, 255))
        self.label.set_text('Initialize state...')
        for sprite in self.sprite_group:
            sprite.draw(self.screen)
        if self.onlyOnce:
            self.onlyOnce = False
            recoder = Recorder()
            recoder.start_AV_recording()
            self.window.set_recorder(recoder)

            # 動画、音声ファイルをアップロード
            exclude_paths = recoder.file_paths()
            upload_file_paths = filter_able_path(data_dir(), exclude_paths)
            Aws().process_s3_upload_files(upload_file_paths, Aws.DATA_DIR)

            self.window.switch_scene(CAMERA_SCENE_NAME)

    def click_notify(self, position):
        pass

    def before_finish(self):
        pass

    def defer(self):
        pass

    class LoadingLabel(pygame.sprite.Sprite):

        content = None
        content_rect = None
        background = None

        WIDTH = WINDOW_WIDTH - 20
        HEIGHT = 80

        def __init__(self, scene, *groups):
            super().__init__(*groups)
            self.scene = scene


        def set_text(self, text):
            font = pygame.font.SysFont(None, 16)
            font_color = (0, 0, 0)
            self.content = font.render(text, True, font_color)
            font_size = font.size(text)
            content_center = UI.string_center((WINDOW_WIDTH/2, WINDOW_HEIGHT/2), font_size)
            self.rect = Rect(content_center[0], content_center[1], font_size[0], font_size[1])

        def draw(self, screen):
            screen.blit(self.content, self.rect)


