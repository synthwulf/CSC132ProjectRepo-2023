import customtkinter
import datetime
import pickle
import os
from tempfile import NamedTemporaryFile

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
    
    t = today.strftime("%m/%d/%Y, %I:%M:%S")# ------> retrieve documen.              
    tdb = open('Time Log.txt', 'a')
    tdb.write(t+ '\n')
        
    return 'Logged in at {} '.format(t)

def clear_frame():
    for widgets in root.winfo_children(): ######### refrence #######  #gets every child widget and kills it.
        widgets.destroy()


def display_camera():   #### displays camera with options (Greyscale, or Normal Video) #[[[[TODO# embed video into frame]]]]]
    clear_frame()
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = 'both', expand= True)
    
    time_text = login_time()
    button = customtkinter.CTkButton(root, text = 'Greyscale')
    button.pack(padx = 12, pady = 0)
    
    button2 = customtkinter.CTkButton(root, text = 'Normal Video')
    button2.pack(pady = 12, padx = 0)
    
    label = customtkinter.CTkLabel(root, text = time_text)
    label.pack(pady = 10, padx = 10)
    
    logout_button = customtkinter.CTkButton(master = frame, text = 'Logout', command = lambda: login_page())
    logout_button.pack(pady = 5, padx = 10)
    
def check_data():
    try:
        with open(data_file, 'rb') as t:
            retrieved_data = pickle.load(t) #### loads data into a variable
    except:
        retrieved_data = {'test':'nuts'}
    return retrieved_data

def hasNumber(input):
    return any(char.isdigit() for char in input)

infoDisplay_counter1 = 0
infoDisplay_counter2= 0
infoDisplay_counter3 = 0
def rewrite(user,password):
    global infoDisplay_counter1
    global infoDisplay_counter2
    global infoDisplay_counter3
    if (user == '' or password == ''):
        empty = customtkinter.CTkLabel(root, text = 'Username or Password not filled', font = ("Times New Roman", 25), text_color='#fc2c03')
        empty.pack_forget()
        infoDisplay_counter1 += 1
        empty.pack(pady = 1, padx = 2)
        print(infoDisplay_counter1)
        if infoDisplay_counter1 == 2:
            empty.destroy()
            infoDisplay_counter1 = 1
        return
        
    if (len(user) < 5):
        short = customtkinter.CTkLabel(root, text = 'Username must have at least 5 characters', font = ("Times New Roman", 25), text_color='#fc2c03')
        short.pack_forget()
        infoDisplay_counter2 += 1
        short.pack(pady = 1, padx = 2)
        if infoDisplay_counter2 == 2:
            short.destroy()
            infoDisplay_counter2 = 1
        return
            
    if (hasNumber(password) == False):
        no_number = customtkinter.CTkLabel(root, text = 'Password must have at least 1 number', font = ("Times New Roman", 25), text_color='#fc2c03')
        no_number.pack_forget()
        infoDisplay_counter3 += 1
        no_number.pack(pady = 1, padx = 2)
        if infoDisplay_counter3 == 2:
            no_number.destroy()
            infoDisplay_counter3 = 1
        return
    
    infoDisplay_counter1 = 0
    infoDisplay_counter2 = 0
    infoDisplay_counter3 = 0
    retrieved_data = check_data()
    with open('users.pkl', 'wb') as t:
        retrieved_data.update({user:password})
        pickle.dump(retrieved_data, t)                                            #### created as a pkl file
    with NamedTemporaryFile("wb", dir=os.path.dirname(data_file),delete=False) as t: #### create a temp file to store data to later then be                                                                             
        pickle.dump(retrieved_data,t)                                                #### created as a pkl file
    os.replace(t.name,"users.pkl")
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
    
    # with NamedTemporaryFile("wb", dir=os.path.dirname(data_file),delete=False) as t: #### create a temp file to store data to later then be                                                                             
    #     os.replace(t.name,"Users.pkl")

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

    # checkbox = customtkinter.CTkCheckBox(master = frame, text = 'Remember me') --> stay logged in
    # checkbox.pack(padx = 12, pady = 10)
    
    #### new_user_funciton() takes in 
    
login_page()

root.mainloop()



