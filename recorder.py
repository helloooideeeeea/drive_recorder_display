




#ffmpeg -f alsa -thread_queue_size 8192 -i plughw:4 -f v4l2 -thread_queue_size 8192 -s 640x480 -i /dev/video4 -c:v h264_omx -b:v 768k -c:a aac output.mp4