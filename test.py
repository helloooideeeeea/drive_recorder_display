import cv2, os
from dotenv import load_dotenv
load_dotenv()  # .env読込
filepath = 'test.avi'

cap = cv2.VideoCapture(os.getenv('OUTSIDE_CAMERA'))
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"w: {w} h:{h} fps:{fps}")

video = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'XVID'), fps, (int(w), int(h)))
while(True):
    # カメラから映像を１枚読込む
    ret, img = cap.read()

    # カメラから読込んだ映像をファイルに書き込む
    video.write(img)

    # カメラから読み込んだ映像を画面に表示する
    cv2.imshow('frame',img)

    # エスケープキーが押されたら処理終了
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Videoを作成時には、開放処理が必要
video.release()
# カメラを使った処理には開放粗利が必要
cap.release()
# Windowを開いた場合は閉じる処理が必要
cv2.destroyAllWindows()