# Bruno Capuano 2020
# display the camera feed using OpenCV
# display the camera feed with grayscale using OpenCV

import time
import cv2
import PySimpleGUI as sg

# Camera Settings
camera_Width = 640 # 480 # 640 # 1024 # 1280
camera_Heigth = 480  # 320 # 480 # 780  # 960
frameSize = (camera_Width, camera_Heigth)

# def webcam col
colwebcam1_layout = [[sg.Text("Вывод камеры", size=(60, 1), justification="center")],
                     [sg.Image(filename="", key="cam1")]]
colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center')
colslayout = [colwebcam1]
layout = [colslayout]

window = sg.Window("El Bruno – Webcams and GrayScale with PySimpleGUI", layout,
                   no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                   return_keyboard_events=True, location=(100, 100))
while True:
    start_time = time.time()
    event, values = window.read(timeout=20)

    if event == sg.WIN_CLOSED:
        break

    # get camera frame
    ret, frameOrig = video_capture.read()
    frame = cv2.resize(frameOrig, frameSize)

    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["cam1"].update(data=imgbytes)

video_capture.release()
cv2.destroyAllWindows()
