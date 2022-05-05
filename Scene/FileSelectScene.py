from Scene import Scene
from pygame.locals import *
from Library import make_random_str, inside_video_data_dir, outside_video_data_dir
from Library.UI import UI
from Constraints import *
import glob
import math


class FileSelectScene(Scene):
    PER_MOVIES_NUM = 6
    ITEM_HEIGHT = 50
    MARGIN_TOP = 30
    MARGIN_MAIN_TOP = 60
    MARGIN_LEFT = 30
    window = None
    screen = None
    items = []

    def __init__(self, window, data = None):
        if data is None:
            self.page = 1
        else:
            self.page = data['page']
        self.window = window
        self.screen = window.screen

        self.items = self.dir_salvage()
        self.pager_switch()
        self.back_surface, self.back_rect = UI.create_back()

    def pager_switch(self):
        self.pager_info_surface, self.pager_info_rect, self.next_surface, self.next_rect, self.prev_surface, self.prev_rect = self.create_pager()

    def dir_salvage(self):
        items = []
        files = []
        inside_files = glob.glob(inside_video_data_dir() + "*")
        outside_files = glob.glob(outside_video_data_dir() + "*")
        files.extend(inside_files)
        files.extend(outside_files)

        arr = []
        for dir in files:
            video_date = dir.split('/')[-1]
            which = dir.split('/')[-2]
            arr.append({'video_date': video_date, 'which': which})

        sorted_arr = sorted(arr, key=lambda x: x['video_date'], reverse=True)

        for index, dir in enumerate(sorted_arr):
            path = '/'.join([dir['which'], dir['video_date']])
            surface, rect = self.create_item(index, path)
            items.append({"surface": surface, "rect": rect, "path": path})

        return items

    # def dummy_items(self):
    #     items = []
    #     for i in range(15):
    #         surface, rect = self.create_item(i, make_random_str(10))
    #         items.append({"surface":surface,"rect":rect})
    #     return items

    def create_item(self, index, text):
        surface, font_size = UI.font_surface(text, 50)
        font_width = font_size[0]

        return surface, Rect(WINDOW_WIDTH/2-font_width/2, self.MARGIN_MAIN_TOP + (index%self.PER_MOVIES_NUM * self.ITEM_HEIGHT), font_width + 20, self.ITEM_HEIGHT)

    def items_height(self):
        return self.MARGIN_MAIN_TOP + (self.PER_MOVIES_NUM * self.ITEM_HEIGHT) + self.MARGIN_TOP

    def pager_items(self):
        return self.items[(self.page-1)*self.PER_MOVIES_NUM:(self.page-1)*self.PER_MOVIES_NUM + self.PER_MOVIES_NUM]

    def create_pager(self):
        pager_counts = self.page * self.PER_MOVIES_NUM
        movies_num = len(self.items)
        is_exist_next = pager_counts < movies_num
        is_exist_prev = self.page > 1
        page_sum = math.ceil(movies_num/self.PER_MOVIES_NUM)

        next_surface = None
        next_rect = None
        prev_surface = None
        prev_rect = None

        if is_exist_next:
            next_surface, font_size = UI.font_surface("Next", 50)
            font_width = font_size[0]
            next_rect = Rect(WINDOW_WIDTH - font_width - self.MARGIN_LEFT - 10, self.items_height(), font_width + 20,
                             self.ITEM_HEIGHT)

        if is_exist_prev:
            prev_surface, font_size = UI.font_surface("Prev", 50)
            font_width = font_size[0]
            prev_rect = Rect(self.MARGIN_LEFT + 10, self.items_height(), font_width + 20, self.ITEM_HEIGHT)

        pager_info_surface, font_size = UI.font_surface(f"{self.page} / {page_sum}", 50)
        font_width = font_size[0]
        pager_info_rect = Rect(WINDOW_WIDTH/2 - font_width/2, self.items_height(), font_width+20, self.ITEM_HEIGHT)

        return pager_info_surface, pager_info_rect, next_surface, next_rect, prev_surface, prev_rect



    def loop(self):
        self.screen.fill((255, 255, 255))  # 背景色
        self.screen.blit(self.back_surface, self.back_rect)
        for item_view in self.pager_items():
            self.screen.blit(item_view["surface"], item_view["rect"])
        if self.prev_surface is not None and self.prev_rect is not None:
            self.screen.blit(self.prev_surface, self.prev_rect)
        if self.next_surface is not None and self.next_rect is not None:
            self.screen.blit(self.next_surface, self.next_rect)
        if self.pager_info_surface is not None and self.pager_info_rect is not None:
            self.screen.blit(self.pager_info_surface, self.pager_info_rect)

    def click_notify(self, position):
        if self.back_rect.collidepoint(position):
            self.window.switch_scene(CAMERA_SCENE_NAME)
            return
        for index, item_view in enumerate(self.items):
            if item_view["rect"].collidepoint(position):
                self.window.switch_scene(MOVIE_SCENE_NAME, data={'path': self.pager_items()[index]['path'], 'page': self.page})
                return
        if self.prev_rect is not None and self.prev_rect.collidepoint(position):
            self.page = self.page - 1
            self.pager_switch()
            return
        if self.next_rect is not None and self.next_rect.collidepoint(position):
            self.page = self.page + 1
            self.pager_switch()
            return

    def before_finish(self):
        pass



