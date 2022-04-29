
class UI:

    @staticmethod
    def string_center(center_position, font_size):
        font_width = font_size[0]
        font_height = font_size[1]
        center_x = center_position[0]
        center_y = center_position[1]
        return center_x - font_width / 2, center_y - font_height / 2