from tkinter import *
from functools import partial
from health_tracker.tracker import HealthTracker
from health_tracker.utils import validateLogin

def main():
    print("WELCOME!")
    print('Enter 1 if you are the ADMIN \nEnter 2 if you are a student')
    imp = input('>>>')
    while imp not in ['1', '2']:
        imp = input('Please refrain from entering any values but 1 or 2:')
    if imp == '1':
        HealthTracker().admin_actions()
    elif imp == '2':
        # window
        tkWindow = Tk()
        tkWindow.geometry('400x150')
        tkWindow.title('Horizon International School')

        # username label and text entry box
        usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

        validateLoginFunc = partial(validateLogin, username, password)

        # login button
        loginButton = Button(tkWindow, text="LOGIN", command=validateLoginFunc).grid(row=4, column=1)

        tkWindow.mainloop()

if __name__ == "__main__":
    main()
