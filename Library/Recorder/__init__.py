from __future__ import print_function, division
import numpy as np
import datetime
import cv2
import pyaudio
import wave
import threading
import time
import os
from Constraints import *
from dotenv import load_dotenv
from Library import video_path, audio_path, is_debug
from loguru import logger

load_dotenv()  # .env読込


class VideoRecorder:
    frame = None
    fps = 5
    frame_rate = 1/5

    def __init__(self, device, prefix, sizex, sizey, fps):
        self.isRunning = True
        self.device = device

        self.file_path = video_path(prefix)
        self.video_cap = cv2.VideoCapture(self.device)
        self.video_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, sizex)
        self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, sizey)
        self.video_cap.set(cv2.CAP_PROP_FPS, fps)

        w = self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.video_out = cv2.VideoWriter(self.file_path, cv2.VideoWriter_fourcc(*'MJPG'), self.fps, (int(w), int(h)))
        # self.start_time = time.time()

    def record(self):
        timer_current = time.time()
        while self.isRunning:
            ret, video_frame = self.video_cap.read()
            if ret:
                # 表示フレーム
                self.frame = video_frame

                video_frame = VideoRecorder.frame_processing(video_frame)

                self.video_out.write(video_frame)

                # 1秒5フレームで保存
                now = time.time()
                frame_time = now - timer_current
                if self.frame_rate > frame_time:
                    time.sleep(self.frame_rate - frame_time)
                else:
                    logger.info(f"frame slow : {frame_time}")
                timer_current = now
        logger.info(f"{self.device} 's thread end.")

    @staticmethod
    def frame_processing(frame):
        cv2.putText(frame,
                    text=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    org=(0, WINDOW_HEIGHT-5),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.6,
                    color=(255, 255, 255),
                    thickness=1,
                    lineType=cv2.LINE_4)
        return frame

    def stop(self):
        self.isRunning = False
        time.sleep(3)
        if self.video_out.isOpened():
            self.video_out.release()
        if self.video_cap.isOpened():
            self.video_cap.release()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()


class AudioRecorder:

    def __init__(self, rate=44100, fpb=1024, channels=2):
        self.isRunning = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.file_path = audio_path('inside')
        # TODO 起動してすぐだとデバイスが見つからないみたい
        time.sleep(3)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        self.stream.start_stream()
        while self.isRunning:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
        logger.info(f"audio recording thread end.")

    def stop(self):
        if self.isRunning:
            self.isRunning = False
            time.sleep(3)
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.file_path, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()


    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()


class Recorder:
    inside_audio_thread = None
    inside_video_thread = None
    outside_video_thread = None

    def start_AV_recording(self):
        inside_camera = os.getenv('INSIDE_CAMERA')
        outside_camera = os.getenv('OUTSIDE_CAMERA')
        while True:
            if os.path.exists(inside_camera) and os.path.exists(outside_camera):
                break
            time.sleep(1)
            logger.info(f"{inside_camera} or {outside_camera} is not found")

        self.inside_video_thread = VideoRecorder(device=inside_camera, prefix="inside", sizex=INSIDE_CAMERA_RECORDING_RESOLUTION_WIDTH, sizey=INSIDE_CAMERA_RECORDING_RESOLUTION_HEIGHT, fps=INSIDE_CAMERA_FRAME_RATE)
        self.outside_video_thread = VideoRecorder(device=outside_camera, prefix="outside", sizex=OUTSIDE_CAMERA_RECORDING_RESOLUTION_WIDTH, sizey=OUTSIDE_CAMERA_RECORDING_RESOLUTION_HEIGHT, fps=OUTSIDE_CAMERA_FRAME_RATE)
        self.inside_audio_thread = AudioRecorder()
        self.inside_audio_thread.start()
        self.inside_video_thread.start()
        self.outside_video_thread.start()

    def stop_AV_recording(self):
        if self.inside_audio_thread is not None:
            self.inside_audio_thread.stop()
        if self.inside_video_thread is not None:
            self.inside_video_thread.stop()
        if self.outside_video_thread is not None:
            self.outside_video_thread.stop()

        # Makes sure the threads have finished
        while threading.active_count() > 1:
            time.sleep(1)

    def file_paths(self):
        list = []
        if self.inside_audio_thread is not None:
            list.append(self.inside_audio_thread.file_path)
        if self.inside_video_thread is not None:
            list.append(self.inside_video_thread.file_path)
        if self.outside_video_thread is not None:
            list.append(self.outside_video_thread.file_path)
        return list
