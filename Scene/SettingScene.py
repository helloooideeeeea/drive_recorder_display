import pygame
from Scene import Scene
from pygame.locals import *
from Constraints import *


class SettingScene(Scene):

    window = None
    screen = None

    def __init__(self, window):
        self.window = window
        self.screen = window.screen

    def loop(self):
        self.screen.fill((255, 255, 255))

    def click_notify(self, position):
        pass

    def before_finish(self):
        pass