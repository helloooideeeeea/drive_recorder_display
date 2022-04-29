from Library.Backend import Backend
from Library import get_logger


def main():

    is_inside_process_launch = False
    is_outside_process_launch = False

    is_inside_process_launch = Backend.launch_process_inside_camera_streaming_bifurcation()
    if is_inside_process_launch:
        is_outside_process_launch = Backend.launch_process_outside_camera_streaming_bifurcation()

    if is_inside_process_launch and is_outside_process_launch:
        get_logger().info("仮想デバイスへのストリーミングを開始しました。")
        return 0
    else:
        get_logger().error("仮想デバイスへのストリーミングに失敗しました。")
        return -1


if __name__ == "__main__":
    main()