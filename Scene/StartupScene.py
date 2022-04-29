import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *
from Library.Backend import Backend
from Library.UI import UI
from enum import IntEnum, auto
import time


class StartupScene(Scene):

    class ProcessType(IntEnum):
        NOT_YET = auto()
        LAUNCHING_INSIDE_CAMERA_STREAMING_BIFURCATION = auto()
        LAUNCHING_OUTSIDE_CAMERA_STREAMING_BIFURCATION = auto()
        LAUNCHING_INSIDE_CAMERA_RECORDING = auto()
        LAUNCHING_OUTSIDE_CAMERA_RECORDING = auto()
        SUCCESS_PROCESS_LAUNCHED = auto()

    process_status = ProcessType.NOT_YET

    FAILED_COUNT_NUM = 10

    def __init__(self, window):

        self.window = window
        self.screen = window.screen
        self.sprite_group = pygame.sprite.RenderUpdates()

        self.label = self.LoadingLabel(self)
        self.sprite_group.add(self.label)

        self.command1 = Backend.create_inside_camera_streaming_bifurcation_command()
        self.command2 = Backend.create_outside_camera_streaming_bifurcation_command()
        self.command3 = Backend.create_inside_recording_command()
        self.command4 = Backend.create_outside_recording_command()

        self.backend = Backend()

    def loop(self):

        self.screen.fill((255, 255, 255))

        if self.process_status == self.ProcessType.NOT_YET:
            self.label.set_text('Initialize state...')
            self.process_status = self.ProcessType.LAUNCHING_INSIDE_CAMERA_STREAMING_BIFURCATION
            if not Backend.is_arrive_process(self.command1):
                Backend.launch_process(self.command1)

        elif self.process_status == self.ProcessType.LAUNCHING_INSIDE_CAMERA_STREAMING_BIFURCATION:
            self.label.set_text('Launching inside camera streaming bifurcation...')
            if self.backend.is_arrive_process_with_failed_count(self.command1):
                self.label.set_text('Launched inside camera streaming bifurcation...')
                self.process_status = self.ProcessType.LAUNCHING_OUTSIDE_CAMERA_STREAMING_BIFURCATION
                Backend.launch_process(self.command2)
            else:
                if self.backend.failed_counter < self.FAILED_COUNT_NUM:
                    self.label.set_text(f'Failed inside camera streaming bifurcation...retry:{self.backend.failed_counter}')
                    Backend.launch_process(self.command1)
                else:
                    self.label.set_text('Failed inside camera streaming bifurcation...please restart')

        elif self.process_status == self.ProcessType.LAUNCHING_OUTSIDE_CAMERA_STREAMING_BIFURCATION:
            self.label.set_text('Launching outside camera streaming bifurcation...')
            if self.backend.is_arrive_process_with_failed_count(self.command2):
                self.label.set_text('Launched outside camera streaming bifurcation...')
                self.process_status = self.ProcessType.LAUNCHING_INSIDE_CAMERA_RECORDING
                Backend.launch_process(self.command3)
            else:
                if self.backend.failed_counter < self.FAILED_COUNT_NUM:
                    self.label.set_text(f'Failed outside camera streaming bifurcation...retry:{self.backend.failed_counter}')
                    Backend.launch_process(self.command2)
                else:
                    self.label.set_text('Failed outside camera streaming bifurcation...please restart')

        elif self.process_status == self.ProcessType.LAUNCHING_INSIDE_CAMERA_RECORDING:
            self.label.set_text('Launching inside camera recording...')
            if self.backend.is_arrive_process_with_failed_count(self.command3):
                self.label.set_text('Launched inside camera recording...')
                self.process_status = self.ProcessType.LAUNCHING_OUTSIDE_CAMERA_RECORDING
                Backend.launch_process(self.command4)
            else:
                if self.backend.failed_counter < self.FAILED_COUNT_NUM:
                    self.label.set_text(f'Failed inside camera recording...retry:{self.backend.failed_counter}')
                    Backend.launch_process(self.command3)
                else:
                    self.label.set_text('Failed inside camera recording...please restart')

        elif self.process_status == self.ProcessType.LAUNCHING_OUTSIDE_CAMERA_RECORDING:
            self.label.set_text('Launching outside camera recording...')
            if self.backend.is_arrive_process_with_failed_count(self.command4):
                self.label.set_text('Initialized Success !!')
                self.process_status = self.ProcessType.SUCCESS_PROCESS_LAUNCHED
                self.window.switch_scene(CAMERA_SCENE_NAME)
                self.defer()
            else:
                if self.backend.failed_counter < self.FAILED_COUNT_NUM:
                    self.label.set_text(f'Failed outside camera recording...retry:{self.backend.failed_counter}')
                    Backend.launch_process(self.command4)
                else:
                    self.label.set_text('Failed outside camera recording...please restart')

        for sprite in self.sprite_group:
            sprite.draw(self.screen)

        pygame.time.wait(3000)


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
            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.rect = Rect(WINDOW_WIDTH/2 - self.WIDTH/2, WINDOW_HEIGHT/2 - self.HEIGHT, self.WIDTH, self.HEIGHT)

        def set_text(self, text):
            font = pygame.font.SysFont(None, 16)
            font_color = (0, 0, 0)
            self.content = font.render(text, True, font_color)
            font_size = font.size(text)
            content_center = UI.string_center((self.WIDTH/2, self.HEIGHT/2), font_size)
            self.content_rect = Rect(content_center[0], content_center[1], font_size[0], font_size[1])

        def draw(self, screen):
            screen.blit(self.background, self.rect)
            screen.blit(self.content, self.content_rect)


