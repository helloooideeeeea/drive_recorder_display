import cv2
import pygame

class CameraSettings:

    @staticmethod
    def decode_fourcc(v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

    @staticmethod
    def set(frame):

        # フォーマット・解像度・FPSの設定
        frame.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        frame.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        frame.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame.set(cv2.CAP_PROP_FPS, 30)

        # フォーマット・解像度・FPSの取得
        fourcc = CameraSettings.decode_fourcc(frame.get(cv2.CAP_PROP_FOURCC))
        width = frame.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = frame.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = frame.get(cv2.CAP_PROP_FPS)
        #print("fourcc:{} fps:{}　width:{}　height:{}".format(fourcc, fps, width, height))

    #TODO どこに書くべきかわからない
    @staticmethod
    def convert_opencv_img_to_pygame(opencv_image):
        opencv_image = opencv_image[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
        shape = opencv_image.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
        pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')
        return pygame_image