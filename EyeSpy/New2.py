import customtkinter
import datetime
import pickle
import os 
from tempfile import NamedTemporaryFile
import pineworkslabs.RPi as GPIO
from PIL import Image, ImageTk
import cv2
import imutils
import threading
from twilio.rest import Client
from time import sleep

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
Shoulditext = 0
GPIO.setmode(GPIO.LE_POTATO_LOOKUP)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
cap.release()


Text = False
Text_mode = False
Text_counter = 0
### {usename : password}
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')
root = customtkinter.CTk()
root.geometry('800x600')

file_path = os.path.dirname(__file__)       ###directory of where python file is being ran at
data_file = file_path + '/'+ "users.pkl"
def login_time():
    today = datetime.datetime.now() #### I is 12- hour ##### computer thing
    
    ##### display at top (or bottom) of frame after login button was pressed ####
    t = today.strftime("%m/%d/%Y, %I:%M:%S")# ------> https://docs.python.org/3/library/time.html ; https://stackoverflow.com/questions/14762518/python-datetime-strptime-and-strftime-how-to-preserve-the-timezone-informat              
    tdb = open(file_path + "/" + 'Time_Log.txt', 'a')
    tdb.write(t+ '\n')
        
    return 'Logged in at {} '.format(t)

def clear_frame():
    for widgets in root.winfo_children(): ######### refrence #######  #gets every child of a specific widget and kills it.
        widgets.destroy()

def display_camera():
    def security_syst():
        nonlocal cap
        thresh = 0
        _, start_frame = cap.read()
        start_frame = imutils.resize(start_frame, width=500)
        start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
        start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
        while True:
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=500)
            if ret:
                frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_bw = cv2.GaussianBlur(frame_bw, (5, 5),0)
                difference = cv2.absdiff(frame_bw, start_frame)
                threshold = cv2.threshold(difference, 25,255, cv2.THRESH_BINARY)[1]
                start_frame = frame_bw
                img = Image.fromarray(threshold)
                tkimg = ImageTk.PhotoImage(image=img)

                cam_label.configure(image=tkimg)  # Rewrite the image to display the grayscale frame
                cam_label.image = tkimg
                if threshold.sum() > 30000:
                    for i in range(1):
                        thresh += 1
                        if thresh > 10:
                            print('alarm')
                            thresh = 0
                            GPIO.output(20, GPIO.HIGH)
                            sleep(.25)
                            GPIO.output(20, GPIO.LOW)
                            GPIO.output(17, GPIO.HIGH)
                            sleep(.25)
                            GPIO.output(17, GPIO.LOW)
                            GPIO.output(25, GPIO.HIGH)
                            sleep(.25)
                            GPIO.output(25, GPIO.LOW)
                            GPIO.output(12, GPIO.HIGH)
                            sleep(.25)
                            GPIO.output(12, GPIO.LOW)
                            message = client.messages.create(
                                from_="",
                                body='Alert at camera',
                                to=''
                            )
                root.update()  # Update the tkinter window
    def convert_to_grayscale():
        nonlocal cap
        while True:
            ret, frame = cap.read()
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                img = Image.fromarray(gray_frame)
                tkimg = ImageTk.PhotoImage(image=img)

                cam_label.configure(image=tkimg)  # Rewrite the image to display the grayscale frame
                cam_label.image = tkimg

                root.update()  # Update the tkinter window

    def display_normal_video():
        nonlocal cap
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                img = Image.fromarray(frame)
                tkimg = ImageTk.PhotoImage(image=img)

                cam_label.configure(image=tkimg)  # Rewrite the image to display the normal video frame
                cam_label.image = tkimg

                root.update()  # Update the tkinter window

    clear_frame()
    # Camera capture and display
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill='both', expand=True)

    time_text = login_time()
    button = customtkinter.CTkButton(frame, text='Security', command=security_syst)  # Added command to call convert_to_grayscale
    button.pack(padx=12, pady=0)
    button = customtkinter.CTkButton(frame, text='Greyscale', command=convert_to_grayscale)  # Added command to call convert_to_grayscale
    button.pack(padx=12, pady=0)

    button2 = customtkinter.CTkButton(frame, text='Normal Video', command=display_normal_video)  # Added command to call display_normal_video
    button2.pack(pady=12, padx=0)

    label = customtkinter.CTkLabel(frame, text=time_text)
    label.pack(pady=10, padx=10)

    logout_button = customtkinter.CTkButton(master=frame, text='Logout', command=lambda: [login_page(), cap.release()])
    logout_button.pack(pady=5, padx=10)

    cam_label = customtkinter.CTkLabel(frame, text="")
    cam_label.pack(pady=1, padx=1)

    # Display the normal video by default
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            img = Image.fromarray(frame)
            tkimg = ImageTk.PhotoImage(image=img)

            cam_label.configure(image=tkimg)
            cam_label.image = tkimg

            root.update()  # Update the tkinter window

def check_data():
    try:
        with open(data_file, 'rb') as t:
            retrieved_data = pickle.load(t) #### loads data into a variable
    except:
        retrieved_data = {'testing': 'password1'}
    return retrieved_data

def hasNumber(input):
    return any(char.isdigit() for char in input)

infoDisplay_counter = 0
def rewrite(user,password):
    global infoDisplay_counter
    global error_label
    if (user == '' or password == ''):
        try:
            error_label.configure(text = "Username or Password not filled")
        except:
            error_label = customtkinter.CTkLabel(root, text = 'Username or Password not filled', font = ("Times New Roman", 25), text_color='#fc2c03')
            error_label.pack_forget()
            infoDisplay_counter += 1
            error_label.pack(pady = 1, padx = 2)
            print(infoDisplay_counter)
            if infoDisplay_counter == 2:
                error_label.destroy()
                infoDisplay_counter = 1
        return
        
    if (len(user) < 5):
        try:
            error_label.configure(text = "Username must have at least 5 characters")
        except:
            error_label = customtkinter.CTkLabel(root, text = 'Username must have at least 5 characters', font = ("Times New Roman", 25), text_color='#fc2c03')
            error_label.pack_forget()
            infoDisplay_counter += 1
            error_label.pack(pady = 1, padx = 2)
            if infoDisplay_counter == 2:
                error_label.destroy()
                infoDisplay_counter = 1
        return
            
    if (hasNumber(password) == False):
        try:
            error_label.configure(text = "Password must have at least 1 number")
        except:
            error_label = customtkinter.CTkLabel(root, text = 'Password must have at least 1 number', font = ("Times New Roman", 25), text_color='#fc2c03')
            error_label.pack_forget()
            infoDisplay_counter += 1
            error_label.pack(pady = 1, padx = 2)
            if infoDisplay_counter == 2:
                error_label.destroy()
                infoDisplay_counter = 1
        return
    
    infoDisplay_counter = 0
    retrieved_data = check_data()
    with open(data_file, 'wb') as t:
        retrieved_data.update({user:password})
        pickle.dump(retrieved_data, t)#### created as a pkl file
        
    with NamedTemporaryFile("wb", dir=file_path,delete=False) as t: #### create a temp file to store data to later then be                                                                             
        pickle.dump(retrieved_data,t)                                                #### created as a pkl file
    os.replace(t.name,data_file)
    login_page()

def new_user():
    clear_frame()
    retrieved_data = check_data()
    
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = 'both', expand= True)
    
    c_username = customtkinter.CTkEntry(master = frame, placeholder_text= 'Create Username')
    c_username.pack(pady = 12, padx = 10)

    c_password = customtkinter.CTkEntry(master = frame, placeholder_text= 'Create Password')
    c_password.pack(pady = 12, padx = 10)
    
    button = customtkinter.CTkButton(master = frame, text = 'Create', command = lambda:[rewrite(c_username.get(),c_password.get())])
    button.pack(pady = 12, padx = 10)
    
    back_button = customtkinter.CTkButton(master = frame, text = 'Back', command = lambda: login_page())
    back_button.pack(pady = 5, padx = 10)

wrongDisplay_counter = 0
def check(user,password):
    retrieved_data = check_data()
    global wrongDisplay_counter
    wrong = customtkinter.CTkLabel(root, text = 'Username or Password is incorect', font = ("Times New Roman", 25), text_color='#fc2c03')
    wrong.pack_forget()
    
    # credentials = [user.lower().strip(), password]
    # try:
    if retrieved_data.get(user) == password:
        clear_frame()                              #then clear frame and display the camera
        display_camera()
        wrongDisplay_counter = 0
    else:
        wrongDisplay_counter += 1
        wrong.pack(pady = 1, padx = 2)
        if wrongDisplay_counter == 2:
            wrong.destroy()
            wrongDisplay_counter = 1
        
def login_page():
    clear_frame()
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = 'both', expand= True)
    
    label = customtkinter.CTkLabel(master = frame, text = 'Eye-Spy', font = ("Times New Roman", 24))
    label.pack(pady = 12, padx = 10)

    username = customtkinter.CTkEntry(master = frame, placeholder_text= 'Username')
    username.pack(pady = 12, padx = 10)

    password = customtkinter.CTkEntry(master = frame, placeholder_text= 'Password', show = '*')
    password.pack(pady = 12, padx = 10)

    button = customtkinter.CTkButton(master = frame, text = 'Login', command = lambda:check(username.get(), password.get()))
    button.pack(pady = 12, padx = 10)
    
    button2 = customtkinter.CTkButton(master = frame, text = 'New User', command = lambda: new_user())
    button2.pack(pady = 12, padx = 10)
    
login_page()

root.mainloop()
