import subprocess
import time
from Constraints import *
from Library import log_dir, ymd, video_path
import psutil


class Backend:

    @staticmethod
    def kill_process(command):
        pass

    @staticmethod
    def is_arrive_process(command):
        for proc in psutil.process_iter():
            cmd = ' '.join(proc.cmdline())
            if cmd == command:
                return True
        return False

    @staticmethod
    def create_streaming_bifurcation_command(camera_hard_device,
                                             camera_frame_rate,
                                             camera_recording_device,
                                             camera_shower_device):
        command = \
            f"gst-launch-1.0 v4l2src device={camera_hard_device} ! " \
            f"image/jpeg,width={RECORDING_RESOLUTION_WIDTH},height={RECORDING_RESOLUTION_HEIGHT},framerate={camera_frame_rate} ! " \
            f"jpegdec ! " \
            f"videoconvert ! " \
            f"video/x-raw,format=I420,width={RECORDING_RESOLUTION_WIDTH},height={RECORDING_RESOLUTION_HEIGHT},framerate={camera_frame_rate} ! " \
            f"tee name=tp tp. ! " \
            f"queue ! " \
            f"v4l2sink device={camera_recording_device} tp. ! " \
            f"queue ! " \
            f"v4l2sink device={camera_shower_device}"
        return command

    @staticmethod
    def create_inside_camera_streaming_bifurcation_command():
        return Backend.create_streaming_bifurcation_command(INSIDE_CAMERA_HARD_DEVICE,
                                                            INSIDE_CAMERA_FRAME_RATE,
                                                            INSIDE_CAMERA_RECORDING_DEVICE,
                                                            INSIDE_CAMERA_SHOWER_DEVICE)

    @staticmethod
    def create_outside_camera_streaming_bifurcation_command():
        return Backend.create_streaming_bifurcation_command(OUTSIDE_CAMERA_HARD_DEVICE,
                                                            OUTSIDE_CAMERA_FRAME_RATE,
                                                            OUTSIDE_CAMERA_RECORDING_DEVICE,
                                                            OUTSIDE_CAMERA_SHOWER_DEVICE)

    @staticmethod
    def create_inside_recording_command():
        mp4 = video_path('inside_camera')
        command = \
            f"gst-launch-1.0 -e v4l2src device={INSIDE_CAMERA_RECORDING_DEVICE} ! " \
            f"queue ! " \
            f"videoconvert ! " \
            f"v4l2h264enc ! " \
            f"'video/x-h264,level=(string)4' ! " \
            f"h264parse ! " \
            f"mux. alsasrc device='hw:audio-inside,0' ! " \
            f"queue ! " \
            f"audioconvert ! " \
            f"voaacenc ! " \
            f"mp4mux name=mux ! " \
            f"filesink location={mp4} sync=false"
        return command

    @staticmethod
    def create_outside_recording_command():
        mp4 = video_path('outside_camera')
        command = \
            f"gst-launch-1.0 -e v4l2src device={OUTSIDE_CAMERA_RECORDING_DEVICE} ! " \
            f"videoconvert ! " \
            f"v4l2h264enc ! " \
            f"'video/x-h264,level=(string)4' ! " \
            f"h264parse ! " \
            f"mp4mux name=mux ! " \
            f"filesink location={mp4} sync=false"
        return command

    @staticmethod
    def launch_process(command):
        subprocess.Popen(Backend.nohup_wrap_command(command), shell=True)
        time.sleep(1)

    @staticmethod
    def nohup_wrap_command(command):
        stderr_path = f'{log_dir()}nohup_error_{ymd()}.log'
        return f"nohup {command} 2>>{stderr_path} 1>/dev/null &"
