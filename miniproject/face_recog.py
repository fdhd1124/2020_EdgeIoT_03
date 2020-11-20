import face_recognition
import pymysql
import numpy as np
import cv2
import tkinter as tk
import tkinter.font
import datetime
import os
import pandas as pd
import sys
sys.path.append('C:\\Users\\user\\Code\\Flask\\project')


# print(len(os.listdir("C:/Users/user/Code/miniproject/img")))
# member_count = len(os.listdir("C:/Users/user/Code/miniproject/img"))
member_list = os.listdir("C:/Users/user/Code/Flask/project/img")
found_flag = False
login_flag = False

conn = pymysql.connect(
    host="192.168.100.41", user="raspberryPi", password="Ab1!", db="memberdb", charset="utf8", port=9876
)
cur = conn.cursor()
known_face_encodings = []
known_face_names = []
count = 0

# 멤버 데이터 인코딩
for member_name in member_list:
    temp = face_recognition.load_image_file(f"./img/{member_name}")
    known_face_encodings.append(face_recognition.face_encodings(temp)[0])
    known_face_names.append(f"{member_name[:-4]}")

# Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
# known_face_encodings = [member0_face_encoding]
# known_face_names = ["member0"]


def login_session():
    global found_flag, login_flag
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # video_capture = cv2.VideoCapture("http://192.168.100.39:8080/?action=stream")
    video_capture = cv2.VideoCapture(0)

    while login_flag == False:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.45
                )
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    log_time = datetime.datetime.today()
                    sql = f"insert into login_log3 values (NULL ,'{name}', '{log_time}')"
                    cur.execute(sql)
                    conn.commit()
                    found_flag = True
                    login_flag = True
                    label.configure(text=f"you're logged in! welcome {name}")

                     # login alarm

                face_names.append(name)

        if found_flag == True:
            video_capture.release()
            cv2.destroyAllWindows()
            break

        process_this_frame = not process_this_frame

        # Display the results
        if found_flag == False:
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        if found_flag == False:
            cv2.putText(
                frame, "face not found!", (30, 30), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (123, 26, 55), 1
            )
        cv2.imshow("Video", frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release handle to the webcam
    found_flag = False
    video_capture.release()
    cv2.destroyAllWindows()


def papa_video():
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # video_capture = cv2.VideoCapture("http://192.168.100.39:8080/?action=stream")
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.45
                )
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow("Video", frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def sign_up(name, phonenum, email):
    save_flag = False
    retry_flag = False
    sign_label = tk.Label(window, text="")
    sign_label.pack()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame, "press 't' to take picture", (30, 30), font, 1.0, (123, 26, 55), 1)
        if retry_flag == True:
            cv2.putText(
                frame, "face not found, retake picture", (30, 75), font, 1.0, (123, 26, 55), 1
            )
        cv2.imshow("Video", frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            break
        elif key & 0xFF == ord("t"):
            cv2.imwrite(f"./img/{name}.jpg", frame)
            try:
                new_member_img = face_recognition.load_image_file(f"./img/{name}.jpg")
                new_member_face_encoding = face_recognition.face_encodings(new_member_img)[0]
                known_face_encodings.append(new_member_face_encoding)
                known_face_names.append(f"{name}")
                cap.release()
                save_flag = True
            except:
                print("retry...")
                retry_flag = True
                sign_label.configure(text="not found a face, retake a picture")
                os.remove(f"./img/{name}.jpg")
        if save_flag == True:
            break

    cv2.destroyAllWindows()
    sign_label.configure(text="")


def signing_up():
    def get_text():
        name = entry1.get()
        phonenum = entry2.get()
        email = entry3.get()
        print(entry1.get())
        print(entry2.get())
        print(entry3.get())

        sign_up(name, phonenum, email)
        conn = pymysql.connect(host="192.168.100.41", user="raspberryPi", password="Ab1!", db="memberdb", charset='utf8',port=9876)
        curr = conn.cursor()
        sql = "INSERT INTO info values('"+str(name) +"','"+str(phonenum)+"','"+str(email)+"')"
        print(sql)
        curr.execute(sql)
        conn.commit()
    
        curr.close()
        conn.close()
        conn = None
        curr = None
        newwindow.destroy()

    newwindow = tk.Toplevel(window)
    newwindow.geometry("320x320")
    newwindow.title("sign up new member")
    label2 = tk.Label(newwindow, text="enter your name")
    entry1 = tk.Entry(newwindow)

    label3 = tk.Label(newwindow, text="enter your phone number")
    entry2 = tk.Entry(newwindow)

    label4 = tk.Label(newwindow, text="enter your e-mail")
    entry3 = tk.Entry(newwindow)
    button = tk.Button(newwindow, text="ok", command=get_text)

    label2.pack()
    entry1.pack()

    label3.pack()
    entry2.pack()

    label4.pack()
    entry3.pack()
    button.pack()


def log_out():
    global login_flag
    if login_flag == True:
        label.configure(text="log out...you're not logged in")
        login_flag = False
    else:
        pass


if __name__ == "__main__":
    window = tk.Tk()
    mainMenu = tk.Menu(window)
    window.config(menu=mainMenu)
    window.title("face_login_system")

    window.geometry("540x320")

    labelFont3 = tkinter.font.Font(family="맑은 고딕", size=14)
    label = tk.Label(window, text="you're not logged in", font=labelFont3)
    label.pack()

    login_ses = tk.Menu(mainMenu)
    mainMenu.add_cascade(label="login", menu=login_ses)
    login_ses.add_command(label="with face", command=login_session)
    login_ses.add_command(label="logout", command=log_out)
    login_ses.add_command(label="sign up", command=signing_up)

    video = tk.Menu(mainMenu)
    mainMenu.add_cascade(label="video", menu=video)
    video.add_command(label="video!", command=papa_video)

    window.mainloop()
    cur.close()
    conn.close()
