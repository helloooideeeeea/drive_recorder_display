import pygame


class CameraSettings:

    #TODO どこに書くべきかわからない
    @staticmethod
    def convert_opencv_img_to_pygame(opencv_image):
        opencv_image = opencv_image[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')
        return pygame_image