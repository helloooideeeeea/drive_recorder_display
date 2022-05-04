from Library.SpriteSheet import SpriteSheet
from Library import assets_dir
import pygame
from pygame.locals import Rect


class UI:

    @staticmethod
    def create_back():
        back_surface, font_size = UI.font_surface(">> Back", 50)
        font_width = font_size[0]
        back_rect = Rect(10, 10, font_width + 20, 50)
        return back_surface, back_rect

    @staticmethod
    def font_surface(text, font_size):
        font = pygame.font.SysFont(None, font_size)
        font_color = (0, 0, 0)
        return font.render(text, True, font_color), font.size(text)

    @staticmethod
    def string_center(center_position, font_size):
        font_width = font_size[0]
        font_height = font_size[1]
        center_x = center_position[0]
        center_y = center_position[1]
        return center_x - font_width / 2, center_y - font_height / 2

    @staticmethod
    def centered_rect(center_x: float, center_y: float, width: float, height: float):
        return Rect(center_x - width/2, center_y - height/2, width, height)

    @staticmethod
    def slice_icon_video_player():
        ss = SpriteSheet(assets_dir()+'video_player.png')
        play_image = UI._play_icon(ss)
        return play_image

    @staticmethod
    def _play_icon(sprite_sheet):
        cut_x = 235
        cut_y = 357
        width = 65
        height = 72
        return sprite_sheet.image_at((cut_x, cut_y, width, height))
        # play_image = pygame.transform.scale(play_image, (40, 40))

    # @staticmethod
    # def _play_icon(sprite_sheet):