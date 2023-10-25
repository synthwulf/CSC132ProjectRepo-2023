import customtkinter
import datetime
import pickle
import os
import threading
from tempfile import NamedTemporaryFile

from PIL import Image, ImageTk
import cv2

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')
root = customtkinter.CTk()
root.geometry('800x600')

file_path = os.path.dirname(__file__)
data_file = file_path + '/' + "users.pkl"

camera_mode = ["normal"]  # Initialize camera mode as a list

def login_time():
    today = datetime.datetime.now()
    t = today.strftime("%m/%d/%Y, %I:%M:%S")
    tdb = open(file_path + "/" + 'Time_Log.txt', 'a')
    tdb.write(t + '\n')
    return 'Logged in at {} '.format(t)

def clear_frame():
    for widgets in root.winfo_children():
        widgets.destroy()

def display_greyscale():
    camera_mode[0] = "greyscale"

def display_normal_video():
    camera_mode[0] = "normal"

def display_camera():
    clear_frame()
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill='both', expand=True)

    time_text = login_time()
    button = customtkinter.CTkButton(frame, text='Greyscale', command=display_greyscale)
    button.pack(padx=12, pady=0)

    button2 = customtkinter.CTkButton(frame, text='Normal Video', command=display_normal_video)
    button2.pack(pady=12, padx=0)

    label = customtkinter.CTkLabel(frame, text=time_text)
    label.pack(pady=10, padx=10)

    logout_button = customtkinter.CTkButton(master=frame, text='Logout', command=login_page)
    logout_button.pack(pady=5, padx=10)

    cam_label = customtkinter.CTkLabel(frame)
    cam_label.pack(pady=1, padx=1)

    def update_camera():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to access the webcam.")
            return

        while True:
            ret, frame = cap.read()
            if ret:
                if camera_mode[0] == "greyscale":
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                img = Image.fromarray(frame)
                tkimg = ImageTk.PhotoImage(image=img)

                cam_label.configure(image=tkimg)
                cam_label.image = tkimg

                root.update()

    camera_thread = threading.Thread(target=update_camera)
    camera_thread.daemon = True
    camera_thread.start()

def check_data():
    try:
        with open(data_file, 'rb') as t:
            retrieved_data = pickle.load(t)
    except:
        retrieved_data = {'testing': 'password1'}
    return retrieved_data

def hasNumber(input):
    return any(char.isdigit() for char in input)

infoDisplay_counter1 = 0
infoDisplay_counter2 = 0
infoDisplay_counter3 = 0

def rewrite(user, password):
    if user == '' or password == '':
        empty_username = customtkinter.CTkLabel(root, text='Username or Password not filled',
                                                font=("Times New Roman", 25), text_color='#fc2c03')
        empty_username.pack_forget()
        infoDisplay_counter1 += 1
        empty_username.pack(pady=1, padx=2)
        if infoDisplay_counter1 == 2:
            empty_username.destroy()
            infoDisplay_counter1 = 1
        return

    if len(user) < 5:
        too_short = customtkinter.CTkLabel(root, text='Username must have at least 5 characters',
                                           font=("Times New Roman", 25), text_color='#fc2c03')
        too_short.pack_forget()
        infoDisplay_counter2 += 1
        too_short.pack(pady=1, padx=2)
        if infoDisplay_counter2 == 2:
            too_short.destroy()
            infoDisplay_counter2 = 1
        return

    if not hasNumber(password):
        no_number = customtkinter.CTkLabel(root, text='Password must have at least 1 number',
                                           font=("Times New Roman", 25), text_color='#fc2c03')
        no_number.pack_forget()
        infoDisplay_counter3 += 1
        no_number.pack(pady=1, padx=2)
        if infoDisplay_counter3 == 2:
            no_number.destroy()
            infoDisplay_counter3 = 1
        return

    infoDisplay_counter1 = 0
    infoDisplay_counter2 = 0
    infoDisplay_counter3 = 0
    retrieved_data = check_data()
    with open(data_file, 'wb') as t:
        retrieved_data.update({user: password})
        pickle.dump(retrieved_data, t)

    with NamedTemporaryFile("wb", dir=file_path, delete=False) as t:
        pickle.dump(retrieved_data, t)
    os.replace(t.name, data_file)
    login_page()

def new_user():
    clear_frame()
    retrieved_data = check_data()

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill='both', expand=True)

    c_username = customtkinter.CTkEntry(master=frame, placeholder_text='Create Username')
    c_username.pack(pady=12, padx=10)

    c_password = customtkinter.CTkEntry(master=frame, placeholder_text='Create Password')
    c_password.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text='Create', command=lambda: [rewrite(c_username.get(), c_password.get())])
    button.pack(pady=12, padx=10)

    back_button = customtkinter.CTkButton(master=frame, text='Back', command=lambda: login_page())
    back_button.pack(pady=5, padx=10)

wrongDisplay_counter = 0

def check(user, password):
    retrieved_data = check_data()
    global wrongDisplay_counter
    wrong = customtkinter.CTkLabel(root, text='Username or Password is incorrect',
                                   font=("Times New Roman", 25), text_color='#fc2c03')
    wrong.pack_forget()

    if retrieved_data.get(user) == password:
        clear_frame()
        display_camera()
        wrongDisplay_counter = 0
    else:
        wrongDisplay_counter += 1
        wrong.pack(pady=1, padx=2)
        if wrongDisplay_counter == 2:
            wrong.destroy()
            wrongDisplay_counter = 1

def login_page():
    clear_frame()
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill='both', expand=True)

    label = customtkinter.CTkLabel(master=frame, text='Eye-Spy', font=("Times New Roman", 24))
    label.pack(pady=12, padx=10)

    username = customtkinter.CTkEntry(master=frame, placeholder_text='Username')
    username.pack(pady=12, padx=10)

    password = customtkinter.CTkEntry(master=frame, placeholder_text='Password', show='*')
    password.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text='Login', command=lambda: check(username.get(), password.get()))
    button.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame, text='New User', command=lambda: new_user())
    button2.pack(pady=12, padx=10)

login_page()
root.mainloop()