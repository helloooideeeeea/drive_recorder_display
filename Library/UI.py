from Library.SpriteSheet import SpriteSheet
from Library import assets_dir
from pygame.locals import Rect


class UI:

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
        cut_x = 235
        cut_y = 357
        width = 65
        height = 72

        play_image = ss.image_at((cut_x, cut_y, width, height))
        # play_image = pygame.transform.scale(play_image, (40, 40))
        return play_image
