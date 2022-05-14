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

load_dotenv()  # .env読込


class VideoRecorder:
    frame = None

    def __init__(self, device, prefix, sizex, sizey, fps):
        self.open = True
        self.device = device

        self.video_filename = video_path(prefix)
        self.video_cap = cv2.VideoCapture(self.device)
        self.video_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, sizex)
        self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, sizey)
        self.video_cap.set(cv2.CAP_PROP_FPS, fps)

        w = self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.video_cap.get(cv2.CAP_PROP_FPS)

        self.video_out = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'MJPG'), self.fps, (int(w), int(h)))
        self.frame_counts = 1
        self.start_time = time.time()

    def record(self):
        # counter = 1
        timer_start = time.time()
        timer_current = 0
        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                # 表示フレーム
                self.frame = video_frame

                video_frame = VideoRecorder.frame_processing(video_frame)

                self.video_out.write(video_frame)
                # print(str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current))
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                time.sleep(1 / self.fps)
                # gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('video_frame', gray)
                # cv2.waitKey(1)

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
        if self.open:
            self.open = False
            time.sleep(3)
            self.video_out.release()
            self.video_cap.release()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()


class AudioRecorder:

    def __init__(self, rate=44100, fpb=1024, channels=2):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = audio_path('inside')
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self):
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.audio_filename, 'wb')
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
        self.inside_video_thread = VideoRecorder(device=os.getenv('INSIDE_CAMERA'), prefix="inside", sizex=INSIDE_CAMERA_RECORDING_RESOLUTION_WIDTH, sizey=INSIDE_CAMERA_RECORDING_RESOLUTION_HEIGHT, fps=INSIDE_CAMERA_FRAME_RATE)
        self.outside_video_thread = VideoRecorder(device=os.getenv('OUTSIDE_CAMERA'), prefix="outside", sizex=OUTSIDE_CAMERA_RECORDING_RESOLUTION_WIDTH, sizey=OUTSIDE_CAMERA_RECORDING_RESOLUTION_HEIGHT, fps=OUTSIDE_CAMERA_FRAME_RATE)
        # self.inside_audio_thread = AudioRecorder()
        # self.inside_audio_thread.start()
        self.inside_video_thread.start()
        self.outside_video_thread.start()

    def stop_AV_recording(self):
        # self.inside_audio_thread.stop()
        self.outside_video_thread.stop()
        self.inside_video_thread.stop()

        # Makes sure the threads have finished
        while threading.active_count() > 1:
            time.sleep(1)
