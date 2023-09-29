import customtkinter
import datetime
import pickle
import os

currentfiledir = os.path.dirname(os.path.realpath(__file__))
filedir = currentfiledir + "/time.pkl"

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
saved_name = ['ryan','ryan']
root = customtkinter.CTk()
root.geometry('800x600')

def login_time():
    today = datetime.datetime.now() #### I is 12- hour ##### computer thing
    ##### display at top (or bottom) of frame after login button was pressed ####
    
    t = today.strftime("%m/%d/%Y, %I:%M:%S")# ------> retrieve documen.              
    with open(filedir, 'wb') as file:
        pickle.dump(t, file)
    return 'Logged in at {} '.format(t)
    
def check(user,password):
    credentials = [user.lower().strip(), password] # ---> matching lists
    if credentials == saved_name:
        clear_frame()
        display_camera()
    else:
        wrong = customtkinter.CTkLabel(root, text = 'Invalid User', font = ("Times New Roman", 25), text_color='#fc2c03')
        wrong.pack(pady = 5, padx = 2)

def clear_frame():
    for widgets in root.winfo_children(): ######### refrence #######
        widgets.destroy()
    
def display_camera():
    clear_frame()
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = 'both', expand= True)
    
    time_text = login_time()
    button = customtkinter.CTkButton(root, text = 'Canny Edge')
    button.pack(padx = 12, pady = 0)
    
    button2 = customtkinter.CTkButton(root, text = 'Normal Video')
    button2.pack(pady = 12, padx = 0)
    
    label = customtkinter.CTkLabel(root, text = time_text)
    label.pack(pady = 10, padx = 10)
    
    logout_button = customtkinter.CTkButton(master = frame, text = 'Logout', command = lambda: login_page())
    logout_button.pack(pady = 5, padx = 10)

def new_user():
    clear_frame()
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = 'both', expand= True)
    
    c_username = customtkinter.CTkEntry(master = frame, placeholder_text= 'Create Username')
    c_username.pack(pady = 12, padx = 10)

    c_password = customtkinter.CTkEntry(master = frame, placeholder_text= 'Create Password')
    c_password.pack(pady = 12, padx = 10)
    
    button = customtkinter.CTkButton(master = frame, text = 'Create', command = lambda: login_page())
    button.pack(pady = 12, padx = 10)
    
    back_button = customtkinter.CTkButton(master = frame, text = 'Back', command = lambda: login_page())
    back_button.pack(pady = 5, padx = 10)
    
def login_page():
    clear_frame()
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = 'both', expand= True)
    
    label = customtkinter.CTkLabel(master = frame, text = 'Login System', font = ("Times New Roman", 24))
    label.pack(pady = 12, padx = 10)

    entry1 = customtkinter.CTkEntry(master = frame, placeholder_text= 'Username')
    entry1.pack(pady = 12, padx = 10)

    entry2 = customtkinter.CTkEntry(master = frame, placeholder_text= 'Password', show = '*')
    entry2.pack(pady = 12, padx = 10)

    button = customtkinter.CTkButton(master = frame, text = 'Login', command = lambda:check(entry1.get(), entry2.get()))
    button.pack(pady = 12, padx = 10)
    
    button2 = customtkinter.CTkButton(master = frame, text = 'New User', command = lambda: new_user())
    button2.pack(pady = 12, padx = 10)

    # checkbox = customtkinter.CTkCheckBox(master = frame, text = 'Remember me') --> stay logged in
    # checkbox.pack(padx = 12, pady = 10)
    
    #### new_user_funciton() takes in 
    
login_page()

root.mainloop()



