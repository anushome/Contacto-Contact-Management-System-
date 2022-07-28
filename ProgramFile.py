# importing required libraries
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import os.path
import sqlite3
import webbrowser
import smtplib
import re
import json
import urllib.request
from urllib.request import urlopen

# setting the root
root = tk.Tk()
# title of the root
root.title("ContactoSpot: Contact Management System")
# icon of the root
root.iconbitmap(r'front_icon.ico')
# Defining its dimension
root.geometry("3000x4000")
# Setting its background photo
back_ground = PhotoImage(file="./test_photo_.png")
bg_label = Label(root, image=back_ground)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Location of the user
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
city = data['city']
region = data['region']
country = data['country']
# Warning message for accessing the user location
MsgBox = tk.messagebox.askquestion('Warning', 'This app will access your location want to proceed', icon='warning')

if MsgBox == 'no':

    root.destroy()
else:
    # Starting the project from here-----------------------------
    tk.messagebox.showinfo('Thanks', 'Thanks For Choosing Us!!!')

    # setting the frame
    frame = tk.Frame(root, bg='#ffffff')
    frame.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)

    # Setting the fonts for database
    LARGEFONT = ("Verdana", 35)
    # Default database
    x = "CONTACT"


    # Code for the database
    def Database():
        global conn, cursor
        # creating contact database
        conn = sqlite3.connect(x)
        cursor = conn.cursor()
        # creating REGISTRATION table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS REGISTRATION (RID INTEGER PRIMARY KEY NOT NULL, FNAME TEXT, AGE TEXT, "
            "GENDER TEXT, ADDRESS TEXT, PCONTACT TEXT, HCONTACT TEXT, OCONTACT TEXT, EMAIL TEXT, STATUS TEXT)")
        cursor.execute("SELECT * FROM REGISTRATION ORDER BY FNAME ASC")


    # For inputting the values
    def register():
        Database()

        # getting form data
        fname1 = fname.get()
        age1 = age.get()
        gender1 = gender.get()
        address1 = address.get()
        pcontact1 = pcontact.get()
        ocontact1 = ocontact.get()
        hcontact1 = hcontact.get()
        status1 = status.get()

        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        if pcontact1 != '':
            try:
                pcontact1 = int(pcontact1)
            except:
                pcontact1 = 's'

        if (ocontact1 != ''):
            try:
                ocontact1 = int(ocontact1)
            except:
                ocontact1 = 's'

        if (hcontact1 != ''):
            try:
                hcontact1 = int(hcontact1)
            except:
                hcontact1 = 's'

        if (age1 != ''):
            try:
                age1 = int(age1)
            except:
                age1 = 's'

        email1 = email.get();
        if (re.search(regex, email1)):
            email1 = str(email1);
        else:
            email1 = 's';

        # applying empty validation
        if fname1 == '' or age1 == '' or gender1 == '' or address1 == '' or email1 == '' or status1 == '':
            tkMessageBox.showwarning("Warning", "fill the empty field!!!")

        elif pcontact1 == '' and ocontact1 == '' and hcontact1 == '':
            tkMessageBox.showwarning("Warning", "fill atleast one contact")

        elif age1 == 's':
            tkMessageBox.showwarning("Warning", "Fill integer value in Age!!!")

        elif pcontact1 == 's' or ocontact1 == 's' or hcontact1 == 's':
            tkMessageBox.showwarning("Warning", "Fill integer value in Contacts!!!")

        elif email1 == 's':
            tkMessageBox.showwarning("Warning", "Fill correct email address!!!")

        else:

            # execute query
            conn.execute('INSERT INTO REGISTRATION (FNAME,AGE,GENDER,ADDRESS,PCONTACT,HCONTACT,OCONTACT,EMAIL,STATUS) \
              VALUES (?,?,?,?,?,?,?,?,?)',
                         (fname1, age1, gender1, address1, pcontact1, hcontact1, ocontact1, email1, status1));
            conn.commit()
            cursor.execute("SELECT * FROM REGISTRATION ORDER BY FNAME ASC")
            tkMessageBox.showinfo("Message", "Stored successfully")
            # refresh table data
            DisplayData()
            conn.close()


    # function to update data into database
    def Update():
        Database()

        # getting form data
        fname1 = fname.get()
        age1 = age.get()
        gender1 = gender.get()
        address1 = address.get()
        pcontact1 = pcontact.get()
        ocontact1 = ocontact.get()
        hcontact1 = hcontact.get()
        email1 = email.get()
        status1 = status.get()

        if (pcontact1 != ''):
            try:
                pcontact1 = int(pcontact1)
            except:
                pcontact1 = 's'

        if (ocontact1 != ''):
            try:
                ocontact1 = int(ocontact1)
            except:
                ocontact1 = 's'

        if (hcontact1 != ''):
            try:
                hcontact1 = int(hcontact1)
            except:
                hcontact1 = 's'

        if (age1 != ''):
            try:
                age1 = int(age1)
            except:
                age1 = 's'

        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        email1 = email.get();
        if (re.search(regex, email1)):
            email1 = str(email1);
        else:
            email1 = 's';

        # applying empty validation
        if fname1 == '' or age1 == '' or gender1 == '' or address1 == '' or email1 == '' or status1 == '':
            tkMessageBox.showwarning("Warning", "fill the empty field!!!")

        elif pcontact1 == '' and ocontact1 == '' and hcontact1 == '':
            tkMessageBox.showwarning("Warning", "fill at least one contact")

        elif age1 == 's':
            tkMessageBox.showwarning("Warning", "Fill integer value in Age!!!")

        elif pcontact1 == 's' or ocontact1 == 's' or hcontact1 == 's':
            tkMessageBox.showwarning("Warning", "Fill integer value in Contacts!!!")

        elif email1 == 's':
            tkMessageBox.showwarning("Warning", "Fill correct email address!!!")
        else:
            # getting selected data
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            # update query
            conn.execute(
                'UPDATE REGISTRATION SET FNAME=?,AGE=?,GENDER=?,ADDRESS=?,PCONTACT=?,HCONTACT=?,OCONTACT=?,EMAIL=?,STATUS=? WHERE RID = ?',
                (fname1, age1, gender1, address1, pcontact1, hcontact1, ocontact1, email1, status1, selecteditem[0]))
            conn.commit()
            cursor.execute("SELECT * FROM REGISTRATION ORDER BY FNAME ASC")
            tkMessageBox.showinfo("Message", "Updated successfully")
            # reset form
            Reset()
            # refresh table data
            DisplayData()
            conn.close()


    # function deleting a record from database
    def Delete():
        Database()
        if not tree.selection():
            tkMessageBox.showwarning("Warning", "Select data to delete")
        else:
            result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                              icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                cursor = conn.execute("DELETE FROM REGISTRATION WHERE RID = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()


    # function for reseting the entries to null
    def Reset():
        # clear current data from table
        tree.delete(*tree.get_children())
        # refresh table data
        DisplayData()
        # clear search text
        SEARCH.set("")
        fname.set("")
        age.set("")
        gender.set("")
        address.set("")
        pcontact.set("")
        hcontact.set("")
        ocontact.set("")
        email.set("")
        status.set("")


    # function to search data from the book
    def SearchRecord():
        # open database
        Database()
        # checking search text is empty or not
        if SEARCH.get() != "":
            # clearing current display data
            tree.delete(*tree.get_children())
            # select query with where clause
            cursor = conn.execute("SELECT * FROM REGISTRATION WHERE FNAME LIKE ?", ('%' + str(SEARCH.get()) + '%',))
            # fetch all matching records
            fetch = cursor.fetchall()
            # loop for displaying all records into GUI
            for data in fetch:
                tree.insert('', 'end', values=data)
            cursor.close()
            conn.close()


    # defining function to access data from SQLite database
    def DisplayData():
        # open database
        Database()
        # clear current data
        tree.delete(*tree.get_children())
        # select query
        cursor = conn.execute("SELECT * FROM REGISTRATION ORDER BY FNAME ASC")
        # fetch all data from database
        fetch = cursor.fetchall()
        # loop for displaying all data in GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
            tree.bind("<Double-1>", OnDoubleClick)
        cursor.close()
        conn.close()


    # function for filling the entries on double click
    def OnDoubleClick(self):
        # getting focused item from tree view
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']

        # set values in the fields
        fname.set(selecteditem[1])
        age.set(selecteditem[2])
        gender.set(selecteditem[3])
        address.set(selecteditem[4])
        pcontact.set(selecteditem[5])
        hcontact.set(selecteditem[6])
        ocontact.set(selecteditem[7])
        email.set(selecteditem[8])
        status.set(selecteditem[9])


    def openweb():
        webbrowser.open('https://www.google.com/settings/security/lesssecureapps')


    mail = " "
    # global variables
    password = " "
    rmail = " "
    mss = " "


    # send_Email method
    def Send_Email(text1, text2):
        NewWindow = Tk()
        NewWindow['background'] = "orange"
        NewWindow.title("Contact List")
        width = 400
        height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = ((screen_width / 2) - 55) - (width / 2)
        y = ((screen_height / 2) + 150) - (height / 2)
        NewWindow.resizable(0, 0)
        NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

        def send():
            text3 = rmail.get()
            text4 = mss.get()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(text1, text2)

            try:
                server.sendmail(text1, text3, text4)
                MsgBox = tk.messagebox.askquestion('Success', 'Message Sent!!! \n Do you want to send more',
                                                   icon='info')
                if MsgBox == 'yes':
                    tk.messagebox.showinfo('Return', 'Thanks For choosing us.')
                else:
                    NewWindow.destroy()
            except:
                tkMessageBox.showerror("Warning", "There is some error... \n Try Again")

        Label(NewWindow, text="Send Email", bg="orange", fg="white", font=("Bahnschrift", 30, "bold")).pack(
            side=TOP, fill=X, padx=15)

        Label(NewWindow, text="Enter recipient Address ", font=("Bahnschrift", 17, "bold"), bg="orange",
              fg="black").pack(side=TOP, padx=10)
        rmail = Entry(NewWindow, width=45, font=("Bahnschrift", 17, "bold"))
        rmail.pack(side=TOP, padx=20)

        Label(NewWindow, text="Enter your message", font=("Bahnschrift", 17, "bold"), bg="orange", fg="black").pack(
            side=TOP, padx=10)
        mss = Entry(NewWindow, width=45, font=("Bahnschrift", 17, "bold"))
        mss.pack(side=TOP, padx=20)

        Button(NewWindow, text="Send Message", command=send, font=('Bahnschrift', 15), bg="#7E7E7E", fg="white").place(x=130,y=220)


    # email login method
    def Email_login():
        global mail
        global password

        NewWindow = Tk()
        NewWindow.title("Contact List")
        NewWindow['background'] = "orange"
        width = 400
        height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = ((screen_width / 2) - 55) - (width / 2)
        y = ((screen_height / 2) + 150) - (height / 2)
        NewWindow.resizable(0, 0)
        NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

        def printx():
            text1 = mail.get()
            text2 = password.get()

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            try:
                server.login(text1, text2)
                tkMessageBox.showinfo("Info", "Login successful \n")
                NewWindow.destroy()
                Send_Email(text1, text2)
            except:
                tkMessageBox.showerror("Warning",
                                       "Email invalid or Password invalid or \nPlease, check your accessibility setting \nfor sending the email \nTry Again !!!")

        Label(NewWindow, text="Login Your Email", bg="orange", fg="white", font=("Bahnschrift", 30, "bold")).pack(
            side=TOP, fill=X, padx=15)

        Label(NewWindow, text="Enter your Email ", font=("Bahnschrift", 17, "bold"), bg="orange", fg="black").pack(
            side=TOP, padx=10)
        mail = Entry(NewWindow, width=45, font=("Bahnschrift", 17, "bold"))
        mail.pack(side=TOP, padx=20)
        Label(NewWindow, text="Enter your password ", font=("Bahnschrift", 17, "bold"), bg="orange", fg="black").pack(
            side=TOP, padx=10)
        password = Entry(NewWindow, width=45, show="*", font=("Bahnschrift", 17, "bold"))
        password.pack(side=TOP, padx=20)

        Button(NewWindow, text="Login", command=printx, font=('Bahnschrift', 15), bg="#7E7E7E", fg="white").place(x=90,
                                                                                                                  y=220)
        Button(NewWindow, text="Give Access", command=openweb, font=('Bahnschrift', 15), bg="#7E7E7E",
               fg="white").place(
            x=190, y=220)


    # function for exiting the application
    def ExitApplication():
        MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                           icon='warning')
        if MsgBox == 'yes':
            root.destroy()
        else:
            tk.messagebox.showinfo('Return', 'You will now return to the application screen')


    # welcome page
    def page1():
        frame1 = tk.Frame(frame, bg='#ffffff')
        frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)

        def delay():
            def call_button():
                loading.destroy()
                progress_bar.destroy()
                create1 = Button(frame1, text="Create Contact Book", font=('Bahnschrift', 30, "bold"),
                                 background="#FF8C00",
                                 fg='#ffffff', activebackground='#7E7E7E', activeforeground='#FF8C00', relief=RIDGE,
                                 width=20, border=0, command=page2)
                create1.place(x=120, y=450)

                create2 = Button(frame1, text="Existing Contact Book", font=('Bahnschrift', 30, "bold"),
                                 background="#FF8C00",
                                 fg='#ffffff', activebackground='#7E7E7E', activeforeground='#FF8C00', relief=RIDGE,
                                 width=20, border=0, command=page3)
                create2.place(x=670, y=450)

            start_button.destroy()
            loading = Label(frame1, text="Loading...", font=" 20", bg="#ffffff", fg="#7E7E7E")
            loading.place(x=110, y=450)
            style = ttk.Style()
            style.theme_use('default')
            style.configure("grey.Horizontal.TProgressbar", background='orange')
            progress_bar = ttk.Progressbar(frame1, orient=HORIZONTAL, length=2000, mode='determinate',
                                           style='grey.Horizontal.TProgressbar')
            progress_bar.place(x=110, y=500)
            progress_bar.start(20)

            frame1.after(3000, call_button)

        photo = PhotoImage(file='./front_icon.png')
        photo = photo.subsample(2)
        lbl = Label(frame1, image=photo, background='#ffffff', justify=CENTER)
        lbl.image = photo
        lbl.pack()

        # set the text
        text_label1 = Label(frame1, text="ContactoSpot")
        text_label1.configure(font=('Comic Sans MS', 60, "bold"), background='#ffffff', foreground='#7E7E7E',
                              justify=CENTER)
        text_label1.pack()
        text_label2 = Label(frame1, text="CONTACT MANAGEMENT SYSTEM")
        text_label2.configure(font=('Comic Sans MS', 15, "bold"), background='#ffffff', foreground='#7E7E7E',
                              justify=CENTER)
        text_label2.pack()

        start_button = Button(frame1, text="GET STARTED", font=('Bahnschrift', 30, "bold"), background="#FF8C00",
                              fg='#ffffff', activebackground='#7E7E7E', activeforeground='#FF8C00', relief=RIDGE,
                              width=20,
                              justify=CENTER, border=0, command=delay)
        start_button.pack(pady=90)


    # creating new contact book page2 method
    def page2():
        frame2 = tk.Frame(frame, bg='#ffffff')
        frame2.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)

        def submit():
            if os.path.isfile('A_data.dat') == False:
                file_object = open("A_data.dat", "w")
                file_object.write("CONTACT")
                file_object.close()

            a = input_var.get()
            a = a.upper()
            file_object = open("A_data.dat", "r")  # opens the file in read mode
            books = file_object.read().splitlines()  # puts the file into an array
            flag = 0
            for j in books:
                if j == a:
                    flag = 1
                elif a == "":
                    flag = 2
            file_object.close()
            if flag == 1:
                # add messagebox
                tkMessageBox.askretrycancel("Application", "Name is Already Used")
            elif flag == 2:
                tkMessageBox.askretrycancel("Application", "Give the input")
            else:
                tkMessageBox.showinfo("Message", "Updated successfully")
                file_object = open('A_data.dat', 'a')
                file_object.write('\n')
                # Append new contact book at the end of file
                file_object.write(a)
                # Close the file
            file_object.close()

        TopViewForm = Frame(frame2, width=600, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        # label for heading
        text_label1 = Label(frame2, text="CREATE NEW CONTACT BOOK")
        text_label1.configure(font=('Bahnschrift', 60, "bold"), background='#ffffff', foreground='orange',
                              justify=CENTER)
        text_label1.pack(fill=X)

        text_label1 = Label(frame2, text="Enter New Contact Book")
        text_label1.configure(font=('Comic Sans MS', 25, 'bold'), background='#ffffff', foreground='#7E7E7E',
                              justify=CENTER)
        text_label1.pack(fill=X, pady=50)

        input_var = Entry(frame2, font=("Bahnschrift", 30, "bold"), background="#7E7E7E", foreground='#ffffff',
                          justify=CENTER)
        input_var.pack()

        sub_btn = Button(frame2, text='SUBMIT', font=('Bahnschrift', 30, "bold"), background="#FF8C00",
                         fg='#ffffff', activebackground='#7E7E7E', activeforeground='#FF8C00', relief=RIDGE, width=20,
                         justify=CENTER, command=submit)
        sub_btn.pack(pady=20)

        button1 = Button(frame2, text="SELECT FROM EXISTING BOOK", font=('Bahnschrift', 30, "bold"),
                         background="#FF8C00",
                         fg='#ffffff', activebackground='#7E7E7E', activeforeground='#FF8C00', relief=RIDGE, width=20,
                         justify=CENTER, command=page3)
        button1.pack(fill=X, pady=70)


    # selecting from existing contact
    def page3():
        v = StringVar()

        # function to select the database
        def ShowChoice():
            global x
            x = v.get()
            tkMessageBox.showinfo("Selected Value", "The selected book is: " + x)

        frame3 = tk.Frame(frame, bg='#ffffff')
        frame3.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)

        frame3["background"] = '#ffffff'

        # label for heading
        TopViewForm = Frame(frame3, width=600, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        # label for heading
        text_label1 = Label(frame3, text="EXISTING CONTACT BOOK")
        text_label1.configure(font=('Bahnschrift', 60, "bold"), background='#ffffff', foreground='orange',
                              justify=CENTER)
        text_label1.pack(side=TOP, fill=X)
        LFrom = Frame(frame3, width=350, background='#ffffff')
        LFrom.pack(side=LEFT, fill=Y)
        LeftViewForm = Frame(frame3, width=300, bg="#ffffff")
        LeftViewForm.pack(side=RIGHT, fill=Y)
        MidViewForm = Frame(frame3, width=1000, bg="#ffffff")
        MidViewForm.pack(side=LEFT, fill=Y)

        button1 = Button(MidViewForm, text="OPEN SELECTED BOOK", font=('Bahnschrift', 17, "bold"), background="#7E7E7E",
                         justify=CENTER, foreground="#ffffff", command=page4)
        button1.pack(fill=X, pady=3)

        Label(MidViewForm, text=" ", background="#ffffff").pack(fill=X, ipady=10)

        if os.path.isfile('A_data.dat') == False:
            file_object1 = open("A_data.dat", "w")
            file_object1.write("CONTACT")
            file_object1.close()

        file_object1 = open("A_data.dat", "r")  # opens the file in read mode
        books = file_object1.read().splitlines()  # puts the file into an array

        for i in range(len(books)):
            Radiobutton(MidViewForm, variable=v, text=books[i], indicator=0, command=ShowChoice, value=books[i],
                        bg="orange", font=('Bahnschrift', 19, "bold"), background="#FF8C00",
                        activebackground="orange", relief=RIDGE, padx=200).pack(
                fill=X, ipady=2)
            Label(MidViewForm, text=" ", background="#ffffff").pack(fill=X, ipady=1)

        file_object1.close()


    # Displaying the selected or default contact book
    def page4():
        frame4 = tk.Frame(frame, bg='#ffffff')
        frame4.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
        global tree
        global SEARCH

        global fname, age, gender, address, pcontact, hcontact, ocontact, email, status

        SEARCH = StringVar()
        fname = StringVar()
        age = StringVar()
        gender = StringVar()
        address = StringVar()
        pcontact = StringVar()
        hcontact = StringVar()
        ocontact = StringVar()
        email = StringVar()
        status = StringVar()

        # creating frames for layout

        # topview frame for heading
        TopViewForm = Frame(frame4, width="600", relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)

        global x, city, region
        # label for heading
        lbl_text = Label(TopViewForm, text=x + " BOOK (" + city + ", " + region + ")", font=('Bahnschrift', 50, "bold"),
                         width=600,
                         bg="white", fg="orange")
        lbl_text.pack(fill=X)

        # first left frame for registration from
        LFrom = Frame(frame4, width=200, bg="orange")
        LFrom.pack(side=LEFT, fill=Y)

        # second right frame for search form
        LeftViewForm = Frame(frame4, width="900", bg="orange")
        LeftViewForm.pack(side=RIGHT, fill=Y)

        # mid frame for displaying record
        MidViewForm = Frame(frame4, width=600)
        MidViewForm.pack()

        # creating registration form in first left frame
        Label(LFrom, text="  Name  ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=fname).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Age  ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=age).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Gender ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        gender.set("")
        content = {'Male', 'Female'}
        OptionMenu(LFrom, gender, *content).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Address ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=address).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Personal Number ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(
            side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=pcontact).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Home Number ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=hcontact).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Office Number ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=ocontact).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Email ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=email).pack(side=TOP, padx=10, fill=X)

        Label(LFrom, text="Status ", font=("Bahnschrift", 12, "bold"), bg="orange", fg="#000000").pack(side=TOP)
        Entry(LFrom, font=("Bahnschrift", 10), textvariable=status).pack(side=TOP, padx=10, fill=X)

        Button(LFrom, text="SUBMIT", font=("Bahnschrift", 15, "bold"), command=register, bg="#7E7E7E", fg="white").pack(
            side=BOTTOM,
            padx=10,
            pady=5,
            fill=X)

        # creating search label and entry in second frame
        lbl_txtsearch = Label(LeftViewForm, text="Enter Name You Want To Search", font=('Bahnschrift', 12), fg="black",
                              bg="orange")
        lbl_txtsearch.pack()

        # creating search entry
        search = Entry(LeftViewForm, textvariable=SEARCH, font=('Bahnschrift', 15), width=10)
        search.pack(side=TOP, padx=20, fill=X)
        # creating search button
        btn_search = Button(LeftViewForm, text="Search", command=SearchRecord, font=('Bahnschrift', 15), bg="#7E7E7E",
                            fg="white")
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        # creating view button
        btn_view = Button(LeftViewForm, text="View All", command=DisplayData, font=('Bahnschrift', 15), bg="#7E7E7E",
                          fg="white")
        btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
        # creating reset button
        btn_reset = Button(LeftViewForm, text="Reset", command=Reset, font=('Bahnschrift', 15), bg="#7E7E7E",
                           fg="white")
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        # creating delete button
        btn_delete = Button(LeftViewForm, text="Delete", command=Delete, font=('Bahnschrift', 15), bg="#7E7E7E",
                            fg="white")
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        # create update button
        btn_delete = Button(LeftViewForm, text="Update", command=Update, font=('Bahnschrift', 15), bg="#7E7E7E",
                            fg="white")
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        # create send email button
        btn_send = Button(LeftViewForm, text="Send Email", command=Email_login, font=('Bahnschrift', 15), bg="#7E7E7E",
                          fg="white")
        btn_send.pack(side=TOP, padx=10, pady=10, fill=X)
        # setting scrollbar
        scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)

        tree = ttk.Treeview(MidViewForm, columns=(
            "Student Id", "Name", "Age", "Gender", "Address", "PContact", "HContact", "OContact", "Email", "Status"),
                            selectmode="extended", height=100, yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        # setting headings for the columns
        tree.heading('Student Id', text="Id", anchor=W)
        tree.heading('Name', text="Name", anchor=W)
        tree.heading('Age', text="Age", anchor=W)
        tree.heading('Gender', text="Gender", anchor=W)
        tree.heading('Address', text="Address", anchor=W)
        tree.heading('PContact', text="Personal Number", anchor=W)
        tree.heading('HContact', text="Home Number", anchor=W)
        tree.heading('OContact', text="Office Number", anchor=W)
        tree.heading('Email', text="Email", anchor=W)
        tree.heading('Status', text="Status", anchor=W)

        # setting width of the columns
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=0)
        tree.column('#2', stretch=NO, minwidth=0, width=150)
        tree.column('#3', stretch=NO, minwidth=0, width=50)
        tree.column('#4', stretch=NO, minwidth=0, width=80)
        tree.column('#5', stretch=NO, minwidth=0, width=150)
        tree.column('#6', stretch=NO, minwidth=0, width=120)
        tree.column('#7', stretch=NO, minwidth=0, width=120)
        tree.column('#8', stretch=NO, minwidth=0, width=120)
        tree.column('#9', stretch=NO, minwidth=0, width=190)
        tree.column('#10', stretch=NO, minwidth=0, width=120)

        tree.pack()
        DisplayData()


    # calling page1 at the start
    page1()
    # navigation bar
    menu_bar = Menu(root)
    # assigning home at navigation bar
    menu_bar.add_command(label="Home", command=page1)

    menu_bar.add_command(label="Create new Book", command=page2)

    menu_bar.add_command(label="Select Book", command=page3)

    menu_bar.add_command(label="Open Your Book", command=page4)

    menu_bar.add_command(label="Exit", command=ExitApplication)

    root.config(menu=menu_bar)

root.mainloop()
