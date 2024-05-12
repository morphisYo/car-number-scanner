import cv2
import pytesseract
from PIL import Image
import PySimpleGUI as sg
import time

sg.theme('Black')

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


# img = cv2.imread("auto.jpg")
# cv2.imshow("My Image", img)
# cv2.waitKey(delay=None)


def capture(img):
    cv2.imwrite("original.jpg", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray.jpg", gray)
    blur = cv2.medianBlur(gray, 3)
    cv2.imwrite("blur.jpg", blur)
    # cv2.imshow("Adaptive", adaptive)
    # cv2.waitKey(delay=None)
    adaptive = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.imwrite("adaptive.jpg", adaptive)
    text = pytesseract.image_to_string(Image.open("original.jpg"), lang="rus")
    text = text.upper()
    trash = "[!@#$|{}.,‚()+=%/?^\"\'`]:;\\'&*`~<>-_› ‘©®ЙЦГШЩЗФЫПЛДЖЭЯЧЬЪБЮ"
    for char in trash: text = text.replace(char, "")

    #print(text)

    t1 = []
    t1[:] = text
    if len(t1) == 8 or len(t1) == 9:
        if t1[0] == "0":
            t1[0] = "О"
        elif t1[0] == "4":
            t1[0] = "А"
        elif t1[0] == "8":
            t1[0] = "В"
        elif t1[0] == "5":
            t1[0] = "В"
        elif t1[0] == "3":
            t1[0] = "В"

        if t1[1] == "З":
            t1[1] = "3"
        elif t1[1] == "В":
            t1[1] = "8"

        if t1[2] == "В":
            t1[2] = "8"
        elif t1[2] == "В":
            t1[2] = "8"

        if t1[3] == "З":
            t1[3] = "3"
        elif t1[3] == "В":
            t1[3] = "8"

        if t1[4] == "0":
            t1[4] = "О"
        elif t1[4] == "4":
            t1[4] = "А"
        elif t1[4] == "8":
            t1[4] = "В"

        if t1[5] == "0":
            t1[5] = "О"
        elif t1[5] == "4":
            t1[5] = "А"
        elif t1[5] == "8":
            t1[5] = "В"

    text = "".join(t1[:-1])

    #print(text)

    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    illegal = ["Й", "Ц", "Г", "Ш", "Щ", "З", "Ф", "Ы", "П", "Л", "Д", "Ж", "Э", "Я", "Ч", "Ь", "Ъ", "Б", "Ю"]
    regions = ["01", "101", "02", "102", "702", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "113",
               "14", "15", "16", "116", "716", "17", "18", "19", "21", "121", "22", "23", "93", "123", "193", "24",
               "124", "25", "125", "26", "126", "27", "28", "29", "30", "31", "32", "33", "34", "134", "35", "36",
               "136", "37", "38", "138", "39", "40", "41", "42", "142", "43", "44", "45", "46", "47", "147", "48", "49",
               "50", "90", "150", "190", "750", "790", "51", "52", "152", "53", "54", "154", "55", "56", "156", "57",
               "58", "59", "159", "60", "61", "161", "761", "62", "63", "163", "763", "64", "164", "65", "66", "96",
               "196", "67", "68", "69", "70", "71", "72", "73", "173", "82", "74", "174", "774", "75", "76", "77", "97",
               "99", "177", "197", "199", "777", "797", "799", "78", "98", "178", "198", "79", "82", "83", "86", "186",
               "87", "89", "92", "95"]

    if len(text) >= 8:
        if text[0] not in nums and text[0] not in illegal:
            if text[1] in nums and text[2] in nums and text[3] in nums:
                if text[4] not in nums and text[5] not in nums and text[4] not in illegal and text[5] not in illegal:
                    if text[6:] in regions:
                        print("Найден:", text)


def webcam():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Camera Settings
    camera_Width = 640  # 480 # 640 # 1024 # 1280
    camera_Heigth = 480  # 320 # 480 # 780  # 960
    frameSize = (camera_Width, camera_Heigth)

    # def webcam col
    colwebcam1_layout = [[sg.Text("Вывод камеры", size=(60, 1), justification="center")],
                         [sg.Image(filename="", key="cam1")]]
    colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center')
    colslayout = [colwebcam1]
    layout = [colslayout]

    window = sg.Window("Программа по распознаванию номеров авто", layout,
                       no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                       return_keyboard_events=True, location=(100, 100))

    while True:
        start_time = time.time()
        event, values = window.read(timeout=20)

        res, img = camera.read()
        cv2.imshow("WEBCAM", img)

        ret, frameOrig = camera.read()
        frame = cv2.resize(frameOrig, frameSize)

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["cam1"].update(data=imgbytes)

        if cv2.waitKey(1) & 0xFF == 27 or event == sg.WIN_CLOSED:
            break

    camera.release()
    cv2.destroyAllWindows()


def showPlates():
    # Camera Settings
    camera_Width = 640  # 480 # 640 # 1024 # 1280
    camera_Heigth = 480  # 320 # 480 # 780  # 960
    frameSize = (camera_Width, camera_Heigth)

    plates_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    colwebcam1_layout = [[sg.Text("Найденные номера", size=(60, 1), justification="center")],
                         [sg.Image(filename="", key="cam1")],
                         [sg.Output(size=(50, 6))],
                         [sg.Button('Выход', size=(10, 1), font='Helvetica 14')]]
    colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center')
    colslayout = [colwebcam1]
    layout = [colslayout]

    window = sg.Window("Программа по распознаванию номеров авто", layout,
                       no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                       return_keyboard_events=True, location=(100, 100))

    while True:
        start_time = time.time()
        event, values = window.read(timeout=20)

        res, img = camera.read()

        ret, frameOrig = camera.read()
        frame = cv2.resize(frameOrig, frameSize)

        plates = plates_db.detectMultiScale(img, 1.1, 19)
        for (x, y, w, h) in plates:
            capture(img[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow("WEBCAM", img)
        if cv2.waitKey(1) & 0xFF == 27 or event == 'Выход' or event == sg.WIN_CLOSED:
            break

    camera.release()
    cv2.destroyAllWindows()


def byImage(img):
    plates_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
    plates = plates_db.detectMultiScale(img, 1.1, 19)
    for (x, y, w, h) in plates:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        capture(img[y:y + h, x:x + w])

showPlates()
