import subprocess
import time
from Constraints import *
from Library import get_logger, log_dir, ymd
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
    def launch_process_inside_camera_streaming_bifurcation():
        command = Backend.create_inside_camera_streaming_bifurcation_command()
        return Backend.launch_process(command)

    @staticmethod
    def launch_process_outside_camera_streaming_bifurcation():
        command = Backend.create_outside_camera_streaming_bifurcation_command()
        return Backend.launch_process(command)

    @staticmethod
    def launch_process(command):
        if Backend.is_arrive_process(command):  # 既にプロセス起動済み
            return True
        else:
            retry_num = 10
            for _ in range(retry_num):
                subprocess.Popen(Backend.nohup_wrap_command(command), shell=True)
                time.sleep(3)
                if Backend.is_arrive_process(command):
                    return True
            get_logger().error(f"プロセス起動に失敗しました。{command} : retry={retry_num}")
            return False

    @staticmethod
    def nohup_wrap_command(command):
        stderr_path = f'{log_dir()}nohup_error_{ymd()}.log'
        return f"nohup {command} 2>>{stderr_path} 1>/dev/null &"

