import cv2
import numpy as np
import dlib
from math import hypot
from win10toast import ToastNotifier
import tkinter as tk
import PIL
from PIL import Image, ImageTk

#ตัวเเปร
time = 0
tt=0

root = tk.Tk()
root.geometry('625x800')
root.title("EyeSight BesideYou")

#โลโก้
logo = Image.open('LogoR.png')
logo = logo.resize((int(logo.width *.9), int(logo.height *.9)))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.place(x=100,y=15)


label = tk.Label(root, fg="blue", text="")


label.pack()



#ตัวเเสกน
def page_2():
    cap = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")



    def midpoint(p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


    font = cv2.FONT_HERSHEY_DUPLEX

    def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

        hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

        ratio = hor_line_lenght / ver_line_lenght
        return ratio

    EYE_AR_THRESH = 4.9
    EYE_AR_CONSEC_FRAMES = 3
    COUNTER = 0
    TOTAL = 0

    while True:
        global tt
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            #x, y = face.left(), face.top()
            #x1, y1 = face.right(), face.bottom()
            #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

            landmarks = predictor(gray, face)

            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

           #เวลา
            tt+=1
            if(tt % 19 == 0):
                global time
                time += 1
                label.config(text=str(time))
                label.after(1000, page_2, label)
                tt=0


            if blinking_ratio < EYE_AR_THRESH:
                COUNTER += 1

            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                COUNTER = 0


            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (90, 400, 30), 4)

            cv2.putText(frame, "Scale: {}".format(blinking_ratio), (10, 460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (90, 400, 30), 2)

            cv2.putText(frame, "time: {}".format(time), (500, 460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (90, 400, 30), 2)



            if (time == 60) and (TOTAL <= 20):
               time = 0
               TOTAL = 0
               toaster = ToastNotifier()
               toaster.show_toast("EyeSightBesideYou", "คุณมีอาการตาล้า", icon_path="eyesight.ico", duration=5,)
            elif (time == 60) and (TOTAL > 22):
                time=0
                TOTAL=0


        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

#ปุ่ม

buttonScan =tk.Button(root, text="Scan",width=25,height = 30 ,font="MMNiratParis-Regular  55",fg = "#d39f75",bg ="#F6DDCC" , command = page_2)
buttonScan.pack()
buttonScan.place(x=200,y=400,width=250,height=60)

buttonScan =tk.Button(root, text="Exit",width=25,height = 30 ,font="MMNiratParis-Regular  55",fg = "#d39f75",bg ="#F6DDCC" , command = root.destroy)
buttonScan.pack()
buttonScan.place(x=200,y=500,width=250,height=60)


root.mainloop()
