import cv2, os
file_path = 'data/outside_202205141220.avi'
cap = cv2.VideoCapture(file_path)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        cv2.putText(frame,
                    text='sample text',
                    org=(0, 450),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.6,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4)

        cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()