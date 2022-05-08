import subprocess
from Constraints import *
from Library import log_dir, ymd, create_video_path
import psutil
from loguru import logger

class Backend:

    failed_counter = 0

    def is_arrive_process_with_failed_count(self, command):
        if Backend.is_arrive_process(command):
            self.failed_counter = 0
            return True
        else:
            self.failed_counter += 1
            return False

    @staticmethod
    def kill_process(command):
        pass

    @staticmethod
    def is_arrive_process(command):
        s_command = command[0:49]
        for proc in psutil.process_iter():
            cmd = ' '.join(proc.cmdline())[0:49]
            if cmd == s_command:
                return True
        return False

    @staticmethod
    def create_streaming_bifurcation_command(camera_resolution_width,
                                             camera_resolution_height,
                                             camera_framerate,
                                             camera_hard_device,
                                             camera_shower_device,
                                             path):
        command = \
            f"gst-launch-1.0 v4l2src device={camera_hard_device} ! " \
            f"image/jpeg,width={camera_resolution_width},height={camera_resolution_height},framerate={camera_framerate} ! " \
            f"jpegdec ! " \
            f"videoconvert ! " \
            f"tee name=tp tp. ! " \
            f"queue ! " \
            f"v4l2sink device={camera_shower_device} tp. ! " \
            f"queue ! " \
            f"v4l2h264enc ! " \
            f"'video/x-h264,level=(string)4' ! " \
            f"h264parse ! " \
            f"mpegtsmux name=mux ! " \
            f"hlssink max-files=0 target-duration=60 location={path}segment%05d.ts playlist-location={path}playlist.m3u8"

        logger.info(f"command:{command}")
        return command


    @staticmethod
    def create_inside_camera_streaming_bifurcation_command():
        path = create_video_path('inside')
        return Backend.create_streaming_bifurcation_command(INSIDE_CAMERA_RECORDING_RESOLUTION_WIDTH,
                                                            INSIDE_CAMERA_RECORDING_RESOLUTION_HEIGHT,
                                                            INSIDE_CAMERA_FRAME_RATE,
                                                            INSIDE_CAMERA_HARD_DEVICE,
                                                            INSIDE_CAMERA_SHOWER_DEVICE,
                                                            path)

    @staticmethod
    def create_outside_camera_streaming_bifurcation_command():
        path = create_video_path('outside')
        return Backend.create_streaming_bifurcation_command(OUTSIDE_CAMERA_RECORDING_RESOLUTION_WIDTH,
                                                            OUTSIDE_CAMERA_RECORDING_RESOLUTION_HEIGHT,
                                                            OUTSIDE_CAMERA_FRAME_RATE,
                                                            OUTSIDE_CAMERA_HARD_DEVICE,
                                                            OUTSIDE_CAMERA_SHOWER_DEVICE,
                                                            path)

    @staticmethod
    def launch_process(command):
        subprocess.Popen(command, shell=True)

    @staticmethod
    def launch_process_with_nohup(command):
        subprocess.Popen(Backend.nohup_wrap_command(command), shell=True)

    @staticmethod
    def nohup_wrap_command(command):
        stderr_path = f'{log_dir()}nohup_error_{ymd()}.log'
        return f"nohup {command} 2>>{stderr_path} 1>/dev/null &"
