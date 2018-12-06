# -*- coding:utf-8 -*-
"""
@File      : capture.py
@Software  : DeepOCR
@Time      : 2018/4/21 12:23
@Author    : yubb
"""
import cv2


def capture():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface.xml')
    cap = cv2.VideoCapture(0)
    num = 0
    while True:
        # get a frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces):
            for (x, y, h, w) in faces:
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if not num % 50:
                    cv2.imwrite('./tmp/%s.jpg' % (str(num)), frame)
                num += 1
        # show a frame
        cv2.imshow("Face Recognition Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


capture()
