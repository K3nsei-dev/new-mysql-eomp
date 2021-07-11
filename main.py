import smtplib
from tkinter import *
from tkinter import messagebox
import mysql.connector as mysql
from PIL import ImageTk, Image
from datetime import *
from tkinter.ttk import Combobox, Treeview
import rsaidnumber
from playsound import playsound
import re

# window set up
root = Tk()
root.geometry("500x500")
root.config(bg="#000000")
root.title("Login Form")

# variables
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")

# regular expression for validating email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

# key-binding
root.bind('<a>', lambda x: [self.admin_window(event=None)])


class AllInOne:
    def __init__(self, master):
        # image
        self.canvas = Canvas(master, width=200, height=200, borderwidth=0, highlightthickness=0, bg="#000000")
        self.canvas.place(x=220, y=0)
        self.img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        self.canvas.create_image(20, 20, anchor=N, image=self.img)
        # buttons
        self.btn_sign = Button(master, text="Sign In", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                               font="Halvetica 12 bold", command=self.login_window)
        self.btn_sign.place(x=220, y=200)
        self.btn_admin = Button(master, text="Admin", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                                font="Halvetica 12 bold", command=self.admin_window)
        self.btn_admin.place(x=220, y=300)
        self.btn_exit = Button(master, text="Exit", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                               font="Halvetica 12 bold", width=5, command=self.exit_code)
        self.btn_exit.place(x=220, y=400)

    def exit_code(self):
        return root.destroy()

    def login_window(self):
        root.withdraw()
        login = Toplevel()
        login.geometry("500x500")
        login.config(bg="#000000")
        login.title("Login Form")

        def clear_program():
            ent_idnum.delete(0, END)
            ent_passwd.delete(0, END)

        def exit_program():
            return root.destroy()

        def user_login():
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            cursor = db.cursor()
            query = "SELECT IDNumber, Password, UserID FROM register WHERE IDNumber = %s"
            value = ent_idnum.get()
            foreign_id = cursor.lastrowid
            cursor.execute(query, (value,))
            my_result = cursor.fetchone()
            try:
                id_number = rsaidnumber.parse(ent_idnum.get())
                if my_result[0] == ent_idnum.get() and my_result[1] == ent_passwd.get():
                    foreign_id = my_result[2]
                    second_query = "INSERT INTO timesheet (LoggedInDate, LoggedInTime, IDNum, UserID) VALUES (%s, %s, " \
                                   " %s, %s) "
                    second_values = (now, date, ent_idnum.get(), foreign_id)
                    cursor.execute(second_query, second_values)
                    db.commit()
                    playsound("./Audio/login.mp3")
                    messagebox.showinfo("Success", "You Have Successfully Logged In")
                elif id_number is False:
                    messagebox.showerror("Error", "Please Enter A Valid 13 Digit ID Number")
                else:
                    messagebox.showerror("Error", "Incorrect ID Number/ Password combination")
            except ValueError:
                messagebox.showerror("Error", "Invalid ID Number")

        def user_logout():
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            cursor = db.cursor()
            query = "SELECT IDNumber, Password FROM register WHERE IDNumber = %s"
            value = ent_idnum.get()
            cursor.execute(query, (value,))
            results = cursor.fetchone()
            try:
                id_number = rsaidnumber.parse(ent_idnum.get())
                if results[0] == ent_idnum.get() and results[1] == ent_passwd.get():
                    second_query = "UPDATE timesheet SET LoggedOutDate = %s, LoggedOutTime = %s WHERE IDNum = %s"
                    second_values = (now, date, ent_idnum.get())
                    cursor.execute(second_query, second_values)
                    db.commit()
                    playsound("./Audio/logout.mp3")
                    messagebox.showinfo("Success", "You Have Successfully Logged Out")
                elif id_number is False:
                    messagebox.showerror("Error", "Please Enter A Valid 13 Digit ID Number")
                else:
                    messagebox.showerror("Error", "Incorrect ID Number/ Password combination")
            except ValueError:
                messagebox.showerror("Error", "Please Enter A Valid ID Number")

        # image
        canvas = Canvas(login, width=200, height=200, borderwidth=0, highlightthickness=0, bg="#000000")
        canvas.place(x=220, y=0)
        img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        canvas.create_image(20, 20, anchor=N, image=img)
        # labels and entries
        lbl_idnum = Label(login, text="ID Number: ", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_idnum.place(x=120, y=225)
        ent_idnum = Entry(login)
        ent_idnum.place(x=245, y=225)
        lbl_passwd = Label(login, text="Password: ", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_passwd.place(x=120, y=255)
        ent_passwd = Entry(login, show="*")
        ent_passwd.place(x=245, y=255)
        # buttons
        btn_exit = Button(login, text="Exit", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                          font="Halvetica 12 bold", command=exit_program)
        btn_exit.place(x=70, y=300)
        btn_login = Button(login, text="Login", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                           font="Halvetica 12 bold", command=user_login)
        btn_login.place(x=150, y=300)
        btn_logout = Button(login, text="Logout", bg="#a5cf00", fg="#000000", highlightthickness=0,
                            borderwidth=10,
                            font="Halvetica 12 bold", command=user_logout)
        btn_logout.place(x=250, y=300)
        btn_clear = Button(login, text="Clear", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                           font="Halvetica 12 bold", command=clear_program)
        btn_clear.place(x=350, y=300)
        btn_register = Button(login, text="Register As A New User", bg="#a5cf00", fg="#000000",
                              highlightthickness=0, borderwidth=10, font="Halvetica 12 bold",
                              command=self.register_window)
        btn_register.place(x=140, y=360)

        login.mainloop()

    def register_window(self):
        register = Toplevel()
        register.title("Register User")
        register.geometry("500x600")
        register.config(bg="#000000")

        def new_user():
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )
            try:
                email = ent_email.get()
                id_number = rsaidnumber.parse(ent_idnum.get())
                phone_number = int(ent_cellnum.get())
                nok_number = int(ent_nextkincell.get())
                if re.search(regex, email):
                    pass
                else:
                    messagebox.showinfo("Failure", "Invalid Email")
                if id_number is False:
                    messagebox.showerror("Error", "Please Enter A Valid ID Number")
                elif type(phone_number) == str or type(nok_number) == str:
                    messagebox.showerror("Error", "Please Use Digits For Cell Number(s)")
                elif len(ent_idnum.get()) == 0 or len(ent_passwd.get()) == 0 or len(ent_cellnum.get()) == 0 or len(
                        ent_nextkin.get()) == 0 or len(ent_nextkincell.get()) == 0:
                    messagebox.showerror("Error", "Please Fill In Each Field Correctly")
                elif len(ent_cellnum.get()) < 10 or len(ent_nextkincell.get()) < 10:
                    messagebox.showerror("Error", "Please Enter A Valid 10 Digit Cell Number")
                elif len(ent_idnum.get()) < 13:
                    messagebox.showerror("Error", "Please Enter A Valid 13 Digit ID Number")
                elif len(ent_cellnum.get()) < 10 or len(ent_nextkincell.get()) < 10 or len(ent_idnum.get()) < 13:
                    messagebox.showerror("Error", "Please Enter 10 Digits For Your Number And 13 Digits For Your ID "
                                                  "Number")
                elif combo_unit.get() == "Select Your Unit":
                    messagebox.showerror("Error", "Please Select Your LC Unit")
                else:
                    cursor = db.cursor()
                    query = "INSERT INTO register (FullName, IDNumber, Password, CellNum, Unit) VALUES (%s, %s, %s, " \
                            "%s, %s) "
                    values = (
                        ent_fullname.get(), ent_idnum.get(), ent_passwd.get(), ent_cellnum.get(), combo_unit.get())
                    cursor.execute(query, values)
                    db.commit()

                    reusable_id = cursor.lastrowid

                    second_query = "INSERT INTO emergency (UserID, IDNum, NextOfKin, NextOfKinNum) VALUES (%s, %s, " \
                                   "%s, %s) "
                    second_values = (reusable_id, ent_idnum.get(), ent_nextkin.get(), ent_nextkincell.get())
                    cursor.execute(second_query, second_values)
                    db.commit()

                    # creates SMTP session
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    sender_email_id = '	lc.onlinelogin@gmail.com'
                    receiver_email_id = ent_email.get()
                    password = "lifechoices1234"
                    # start TLS for security
                    s.starttls()
                    # Authentication
                    s.login(sender_email_id, password)
                    # message to be sent
                    first_message = "Your Login details are as follows:\n"
                    second_message = first_message + "Your Username:" + ent_idnum.get() + "\n" + "Your Password:" + ent_passwd.get() + "\n" + "Please do not forget to login after receiving this email!"
                    # sending the mail
                    s.sendmail(sender_email_id, receiver_email_id, second_message)
                    # terminating the session
                    s.quit()
                    playsound("./Audio/mail.mp3")
                    messagebox.showinfo("Success", "Please Check Your Email For Further Instructions!")
                    register.withdraw()
            except ValueError:
                messagebox.showerror("Error", "Please Use Digits For ID Number And Cell Phone Numbers Only")

        # labels
        lbl_fullname = Label(register, text="Full Name:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_fullname.place(x=80, y=260)
        lbl_passwd = Label(register, text="Password:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_passwd.place(x=80, y=290)
        lbl_idnum = Label(register, text="ID Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_idnum.place(x=80, y=320)
        lbl_cellnum = Label(register, text="Cell Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_cellnum.place(x=80, y=350)
        lbl_unit = Label(register, text="LC Unit:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_unit.place(x=80, y=380)
        lbl_nextkin = Label(register, text="Next Of Kin:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_nextkin.place(x=80, y=410)
        lbl_nextkincell = Label(register, text="Next Of Kin Number:", bg="#000000", fg="#a5cf00",
                                font="Halvetica 12 bold")
        lbl_nextkincell.place(x=80, y=440)
        lbl_email = Label(register, text="Your Email Address:", bg="#000000", fg="#a5cf00",
                          font="Halvetica 12 bold")
        lbl_email.place(x=80, y=470)
        # image
        canvas = Canvas(register, width=500, height=250, borderwidth=0, highlightthickness=0, bg="#000000")
        canvas.place(x=125, y=0)
        img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        canvas.create_image(20, 20, anchor=NW, image=img)
        # entries
        ent_fullname = Entry(register)
        ent_fullname.place(x=280, y=260)
        ent_passwd = Entry(register)
        ent_passwd.place(x=280, y=290)
        ent_idnum = Entry(register)
        ent_idnum.place(x=280, y=320)
        ent_cellnum = Entry(register)
        ent_cellnum.place(x=280, y=350)
        ent_nextkin = Entry(register)
        ent_nextkin.place(x=280, y=410)
        ent_nextkincell = Entry(register)
        ent_nextkincell.place(x=280, y=440)
        ent_email = Entry(register)
        ent_email.place(x=280, y=470)
        # button
        btn_register = Button(register, text="Register", bg="#a5cf00", fg="#000000", font="Halvetica 12 bold",
                              borderwidth=10,
                              highlightthickness=0, command=new_user)
        btn_register.place(x=200, y=520)

        # combo box
        combo_unit = Combobox(register, width=17)
        combo_unit["values"] = ("Academy", "Business", "Staff")
        combo_unit["state"] = "readonly"
        combo_unit.set("Select Your Unit")
        combo_unit.place(x=280, y=380)

        register.mainloop()

    def admin_window(self, event=None):
        root.withdraw()
        admin = Toplevel()
        admin.geometry("500x500")
        admin.config(bg="#000000")
        admin.title("Admin Login")

        def exit_code2():
            return admin.destroy()

        def clear_code2():
            ent_idnum2.delete(0, END)
            ent_passwd2.delete(0, END)

        def admin_login():
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            cursor = db.cursor()
            query = "SELECT IDNumber, Password, Unit FROM register WHERE IDNumber = %s"
            value = ent_idnum2.get()
            cursor.execute(query, (value,))
            my_result = cursor.fetchone()

            try:
                id_number = rsaidnumber.parse(ent_idnum2.get())
                if id_number is False:
                    messagebox.showerror("Error", "Please Enter A 13 Digit ID Number")
                elif my_result[0] == ent_idnum2.get() and my_result[1] == ent_passwd2.get() and my_result[2] == "Staff":
                    playsound("./Audio/login.mp3")
                    messagebox.showinfo("Success", "You Have Successfully Logged In")
                    admin.withdraw()
                    self.admin_table()
                else:
                    messagebox.showerror("Error", "You Do Not Have Admin Privileges")
            except ValueError:
                messagebox.showerror("Error", "Please Use A Valid ID Number")

        # image
        canvas = Canvas(admin, width=200, height=200, borderwidth=0, highlightthickness=0, bg="#000000")
        canvas.place(x=220, y=0)
        img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        canvas.create_image(20, 20, anchor=N, image=img)

        # labels and entries
        lbl_idnum2 = Label(admin, text="ID Number: ", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_idnum2.place(x=120, y=225)
        ent_idnum2 = Entry(admin)
        ent_idnum2.place(x=245, y=225)
        lbl_passwd2 = Label(admin, text="Password: ", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_passwd2.place(x=120, y=255)
        ent_passwd2 = Entry(admin, show="*")
        ent_passwd2.place(x=245, y=255)

        # button
        btn_login2 = Button(admin, text="Login", bg="#a5cf00", fg="#000000", font="Halvetica 12 bold",
                            borderwidth=10,
                            highlightthickness=0, command=admin_login)
        btn_login2.place(x=193, y=300)
        btn_exit = Button(admin, text="Exit", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                          font="Halvetica 12 bold", command=exit_code2)
        btn_exit.place(x=117, y=300)
        btn_clear = Button(admin, text="Clear", bg="#a5cf00", fg="#000000", highlightthickness=0, borderwidth=10,
                           font="Halvetica 12 bold", command=clear_code2)
        btn_clear.place(x=300, y=300)

        admin.mainloop()

    def admin_table(self):
        # set up
        admin_page = Toplevel()
        admin_page.geometry("500x500")
        admin_page.title("Admin Account")
        admin_page.config(bg="#000000")

        def table_1():
            window = Toplevel()
            window.title('User Information')
            window.geometry('1800x800')

            def edit_user():
                tv5_window = Frame(window, width=400, height=400, bg="#000000")
                tv5_window.place(x=500, y=260)

                def edit():
                    my_db2 = mysql.connect(
                        host="localhost",
                        user="root",
                        passwd="@Lifechoices1234",
                        database="lifechoicesonline"
                    )

                    my_cursor3 = my_db2.cursor()
                    query = "SELECT IDNumber FROM register WHERE IDNumber = %s"
                    value = ent_edit.get()
                    cursor.execute(query, (value,))
                    results = cursor.fetchone()

                    try:
                        id_number = rsaidnumber.parse(ent_edit.get())
                        if results[0] == ent_edit.get():
                            edit_query = "UPDATE register SET Unit = %s WHERE IDNumber = %s"
                            edit_value = (combo_unit.get(), ent_edit.get())
                            my_cursor3.execute(edit_query, edit_value)
                            my_db2.commit()
                            messagebox.showinfo("Success", "You Have Successfully Updated The User")
                            tv5_window.destroy()
                            table_1()
                        elif id_number is False:
                            messagebox.showerror("Error", "Please Enter A Valid ID Number")
                        if len(ent_edit.get()) == 0:
                            messagebox.showerror("Error", "Please Enter The ID Number Of User You Would Like To Edit")

                        elif combo_unit.get() == "Select Your Unit":
                            messagebox.showerror("Error", "Please Select Your LC Unit")
                    except ValueError:
                        messagebox.showerror("Error", "Please Enter A Valid ID Number")

                # label
                lbl_edit = Label(tv5_window, text="ID Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl_edit.place(x=85, y=50)
                lbl_unit = Label(tv5_window, text="LC Unit:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl_unit.place(x=85, y=100)

                # Entry
                ent_edit = Entry(tv5_window)
                ent_edit.place(x=185, y=50)

                # combo box
                combo_unit = Combobox(tv5_window, width=17)
                combo_unit["values"] = ("Academy", "Business", "Staff")
                combo_unit["state"] = "readonly"
                combo_unit.set("Select Your Unit")
                combo_unit.place(x=185, y=100)

                # button
                btn_remove2 = Button(tv5_window, text="Submit", bg="#a5cf00", fg="#000000", highlightthickness=0,
                                     borderwidth=10,
                                     font="Halvetica 12 bold", command=edit)
                btn_remove2.place(x=165, y=150)

                tv5_window.mainloop()

            def grant_privileges():
                tv4_window = Frame(window, width=400, height=400, bg="#000000")
                tv4_window.place(x=500, y=260)

                def grant():
                    my_db2 = mysql.connect(
                        host="localhost",
                        user="root",
                        passwd="@Lifechoices1234",
                        database="lifechoicesonline"
                    )

                    my_cursor3 = my_db2.cursor()

                    try:
                        user = ent_user.get()
                        if len(ent_user.get()) == 0:
                            messagebox.showerror("Error", "Please Insert User ID Number")
                        elif type(user) == str:
                            messagebox.showerror("Error", "Please User Alphabetical Characters Only")
                        else:
                            c_query = "CREATE USER %s@localhost IDENTIFIED BY %s"
                            c_value = (ent_user.get(), ent_pass.get())
                            my_cursor3.execute(c_query, c_value)
                            my_db2.commit()
                            p_query = "GRANT ALL PRIVILEGES ON lifechoicesonline.* TO %s@localhost"
                            sel_data = str(ent_user.get())
                            my_cursor3.execute(p_query, (sel_data,))
                            my_db2.commit()
                            f_query = "FLUSH PRIVILEGES"
                            my_cursor3.execute(f_query)
                            my_db2.commit()
                            messagebox.showinfo("Success", "You Have Successfully Created A User And Granted Them "
                                                           "Privileges")
                            window.destroy()
                            table_1()
                    except ValueError:
                        messagebox.showerror("Error", "Please Enter A Valid Username")

                # label
                lbl_user = Label(tv4_window, text="Username:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl_user.place(x=85, y=50)
                lbl_pass = Label(tv4_window, text="Password:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl_pass.place(x=85, y=100)

                ent_user = Entry(tv4_window)
                ent_user.place(x=185, y=50)
                ent_pass = Entry(tv4_window)
                ent_pass.place(x=185, y=100)

                # button
                btn_remove2 = Button(tv4_window, text="Submit", bg="#a5cf00", fg="#000000", highlightthickness=0,
                                     borderwidth=10,
                                     font="Halvetica 12 bold", command=grant)
                btn_remove2.place(x=165, y=150)

                tv4_window.mainloop()

            def remove_user():
                tv3_window = Frame(window, width=400, height=400, bg="#000000")
                tv3_window.place(x=500, y=260)
                my_db2 = mysql.connect(
                    host="localhost",
                    user="root",
                    passwd="@Lifechoices1234",
                    database="lifechoicesonline"
                )

                my_cursor = my_db2.cursor()

                def remove():
                    if tree.selection() == ():
                        messagebox.showerror("Error", "Please Select A User You Would Like To Grant Privileges")
                    else:
                        selected_item = tree.selection()[0]
                        uid = tree.item(selected_item)['values'][5]
                        del_query = "DELETE FROM timesheet WHERE UserID = %s"
                        del_query2 = "DELETE FROM emergency WHERE UserID = %s"
                        del_query3 = "DELETE FROM register WHERE UserID = %s"
                        sel_data = (uid,)
                        my_cursor.execute(del_query, sel_data)
                        my_cursor.execute(del_query2, sel_data)
                        my_cursor.execute(del_query3, sel_data)
                        my_db2.commit()
                        tree.delete(selected_item)
                        messagebox.showinfo("Success", "You Have Successfully Deleted The User")
                        window.destroy()
                        table_1()

                # button
                btn_remove2 = Button(tv3_window, text="Remove", bg="#a5cf00", fg="#000000", highlightthickness=0,
                                     borderwidth=10,
                                     font="Halvetica 12 bold", command=remove)
                btn_remove2.place(x=165, y=150)

                tv3_window.mainloop()

            def update_user():
                tv6_window = Frame(window, width=400, height=400, bg="#000000")
                tv6_window.place(x=500, y=260)

                def update():
                    try:
                        id_number = rsaidnumber.parse(ent2.get())
                        phone_number = int(ent3.get())
                        nok_number = int(ent7.get())
                        if len(ent1.get()) == 0 or len(ent2.get()) == 0 or len(ent3.get()) == 0 or len(
                                ent4.get()) == 0 or len(ent6.get()) == 0 or len(ent7.get()) == 0:
                            messagebox.showerror("Error", "Please Fill In Each Field Correctly")
                        elif id_number is False:
                            messagebox.showerror("Error", "Please Enter A Valid ID Number")
                        elif type(phone_number) == str or type(nok_number) == str:
                            messagebox.showerror("Error", "Please Enter A Valid Cell Number")
                        elif combo_unit.get() == "Select Your Unit":
                            messagebox.showerror("Error", "Please Select Your LC Unit")
                        else:
                            my_cursor = my_db.cursor()
                            query = "UPDATE register SET FullName = %s, IDNumber = %s, Password = %s, CellNum = %s, " \
                                    "Unit = %s WHERE IDNumber = %s "
                            values = (
                                ent1.get(), ent2.get(), ent3.get(), ent4.get(), combo_unit.get(), ent2.get())
                            my_cursor.execute(query, values)
                            my_db.commit()

                            second_query = "UPDATE emergency SET IDNum = %s, NextOfKin = %s, NextOfKinNum = " \
                                           "%s WHERE IDNum = %s "
                            second_values = (ent2.get(), ent6.get(), ent7.get(), ent2.get())
                            my_cursor.execute(second_query, second_values)
                            my_db.commit()

                            messagebox.showinfo("Success", "You have Successfully Edited The User's Details")
                            window.destroy()
                            table_1()
                    except ValueError:
                        messagebox.showerror("Error", "Please Enter Digits Only For ID Number And Cell Number(s)")

                # labels
                lbl1 = Label(tv6_window, text="Full Name:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl1.place(x=0, y=10)
                lbl2 = Label(tv6_window, text="ID Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl2.place(x=0, y=60)
                lbl3 = Label(tv6_window, text="Password:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl3.place(x=0, y=110)
                lbl4 = Label(tv6_window, text="Cell Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl4.place(x=0, y=160)
                lbl5 = Label(tv6_window, text="LC Unit:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl5.place(x=0, y=210)
                lbl6 = Label(tv6_window, text="Next Of Kin:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl6.place(x=0, y=260)
                lbl7 = Label(tv6_window, text="Next Of Kin Number:", bg="#000000", fg="#a5cf00",
                             font="Halvetica 12 bold")
                lbl7.place(x=0, y=310)

                # entries
                ent1 = Entry(tv6_window)
                ent1.place(x=200, y=10)
                ent2 = Entry(tv6_window)
                ent2.place(x=200, y=60)
                ent3 = Entry(tv6_window)
                ent3.place(x=200, y=110)
                ent4 = Entry(tv6_window)
                ent4.place(x=200, y=160)
                combo_unit = Combobox(tv6_window, width=17)
                combo_unit["values"] = ("Academy", "Business", "Staff")
                combo_unit["state"] = "readonly"
                combo_unit.set("Select Your Unit")
                combo_unit.place(x=200, y=210)
                ent6 = Entry(tv6_window)
                ent6.place(x=200, y=260)
                ent7 = Entry(tv6_window)
                ent7.place(x=200, y=310)

                # button
                btn_submit = Button(tv6_window, text="Submit", bg="#a5cf00", fg="#000000", highlightthickness=0,
                                    borderwidth=10,
                                    font="Halvetica 12 bold", command=update)
                btn_submit.place(x=170, y=350)

                tv6_window.mainloop()

            def insert_user():
                tv_window = Frame(window, width=400, height=400, bg="#000000")
                tv_window.place(x=500, y=260)

                def submit():
                    try:
                        id_number = rsaidnumber.parse(ent2.get())
                        phone_number = int(ent3.get())
                        nok_number = int(ent7.get())
                        if len(ent1.get()) == 0 or len(ent2.get()) == 0 or len(ent3.get()) == 0 or len(
                                ent4.get()) == 0 or len(ent6.get()) == 0 or len(ent7.get()) == 0:
                            messagebox.showerror("Error", "Please Fill In Each Field Correctly")
                        elif id_number is False:
                            messagebox.showerror("Error", "Please Enter A Valid ID Number")
                        elif type(phone_number) == str or type(nok_number) == str:
                            messagebox.showerror("Error", "Please Enter A Valid Cell Number")
                        elif combo_unit.get() == "Select Your Unit":
                            messagebox.showerror("Error", "Please Select Your LC Unit")
                        else:
                            my_cursor = my_db.cursor()
                            query = "INSERT INTO register (FullName, IDNumber, Password, CellNum, Unit) VALUES (%s, " \
                                    "%s, " \
                                    "%s, %s, %s) "
                            values = (
                                ent1.get(), ent2.get(), ent3.get(), ent4.get(), combo_unit.get())
                            my_cursor.execute(query, values)
                            my_db.commit()

                            reusable_id = my_cursor.lastrowid

                            second_query = "INSERT INTO emergency (UserID, IDNum, NextOfKin, NextOfKinNum) VALUES (%s, " \
                                           "%s, %s, %s) "
                            second_values = (reusable_id, ent2.get(), ent6.get(), ent7.get())
                            my_cursor.execute(second_query, second_values)
                            my_db.commit()

                            messagebox.showinfo("Success", "You have Successfully Registered The User")
                            window.destroy()
                            table_1()
                    except ValueError:
                        messagebox.showerror("Error", "Please Enter Digits Only For ID Number And Cell Number(s)")

                # labels
                lbl1 = Label(tv_window, text="Full Name:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl1.place(x=0, y=10)
                lbl2 = Label(tv_window, text="ID Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl2.place(x=0, y=60)
                lbl3 = Label(tv_window, text="Password:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl3.place(x=0, y=110)
                lbl4 = Label(tv_window, text="Cell Number:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl4.place(x=0, y=160)
                lbl5 = Label(tv_window, text="LC Unit:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl5.place(x=0, y=210)
                lbl6 = Label(tv_window, text="Next Of Kin:", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
                lbl6.place(x=0, y=260)
                lbl7 = Label(tv_window, text="Next Of Kin Number:", bg="#000000", fg="#a5cf00",
                             font="Halvetica 12 bold")
                lbl7.place(x=0, y=310)

                # entries
                ent1 = Entry(tv_window)
                ent1.place(x=200, y=10)
                ent2 = Entry(tv_window)
                ent2.place(x=200, y=60)
                ent3 = Entry(tv_window)
                ent3.place(x=200, y=110)
                ent4 = Entry(tv_window)
                ent4.place(x=200, y=160)
                combo_unit = Combobox(tv_window, width=17)
                combo_unit["values"] = ("Academy", "Business", "Staff")
                combo_unit["state"] = "readonly"
                combo_unit.set("Select Your Unit")
                combo_unit.place(x=200, y=210)
                ent6 = Entry(tv_window)
                ent6.place(x=200, y=260)
                ent7 = Entry(tv_window)
                ent7.place(x=200, y=310)

                # button
                btn_submit = Button(tv_window, text="Submit", bg="#a5cf00", fg="#000000", highlightthickness=0,
                                    borderwidth=10,
                                    font="Halvetica 12 bold", command=submit)
                btn_submit.place(x=170, y=350)

            # configure the grid layout
            root.rowconfigure(0, weight=1)
            root.columnconfigure(0, weight=1)

            # create a treeview
            tree = Treeview(window, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), show="headings")
            tree.heading('#0', text='Tables', anchor='center')

            # place the Treeview widget on the root window
            tree.grid(row=0, column=0, sticky='ne')
            tree.column("1", anchor="center")
            tree.column("2", width=90, anchor="center")
            tree.column("4", width=80, anchor="center")
            tree.column("5", width=80, anchor="center")
            tree.column("6", width=50, anchor="center")
            tree.column("8", width=80, anchor="center")
            tree.column("9", anchor="center")
            tree.column("10", anchor="center")
            tree.column("11", anchor="center")
            tree.column("12", anchor="center")

            tree.heading(1, text="Full Name")
            tree.heading(2, text="ID Number")
            tree.heading(3, text="Password")
            tree.heading(4, text="Phone Number")
            tree.heading(5, text="Unit")
            tree.heading(6, text="User ID")
            tree.heading(7, text="Next Of Kin")
            tree.heading(8, text="CellNum")
            tree.heading(9, text="Logged In Date")
            tree.heading(10, text="Logged In Time")
            tree.heading(11, text="Logged Out Date")
            tree.heading(12, text="Logged Out Time")

            my_db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            cursor = my_db.cursor()
            first_query = "SELECT register.FullName, register.IDNumber, register.Password, register.CellNum, " \
                          "register.Unit, " \
                          "register.UserID, emergency.NextOfKin, emergency.NextOfKinNum, timesheet.LoggedInDate, " \
                          "timesheet.LoggedInTime, timesheet.LoggedOutDate, timesheet.LoggedOutTime FROM register " \
                          "INNER JOIN " \
                          "emergency ON register.UserID = emergency.UserID INNER JOIN timesheet ON emergency.UserID = " \
                          "timesheet.UserID "
            cursor.execute(first_query)

            data = cursor.fetchall()

            for i in data:
                tree.insert("", END, values=i, open=False)

            # button
            btn_add = Button(window, text="Add User", highlightthickness=0, borderwidth=10, font="Halvetica 12 bold",
                             command=insert_user)
            btn_add.place(x=220, y=250)
            btn_edit = Button(window, text="Admin Privileges", highlightthickness=0, borderwidth=10,
                              font="Halvetica 12 bold", command=edit_user)
            btn_edit.place(x=220, y=400)
            btn_remove = Button(window, text="Remove User", highlightthickness=0, borderwidth=10,
                                font="Halvetica 12 bold", command=remove_user)
            btn_remove.place(x=220, y=300)
            btn_grant = Button(window, text="Database Privileges", highlightthickness=0, borderwidth=10,
                               font="Halvetica 12 bold",
                               command=grant_privileges)
            btn_grant.place(x=220, y=450)
            btn_grant = Button(window, text="Edit User Details", highlightthickness=0, borderwidth=10,
                               font="Halvetica 12 bold",
                               command=update_user)
            btn_grant.place(x=220, y=350)

            window.mainloop()

        # image
        canvas = Canvas(admin_page, width=500, height=250, borderwidth=0, highlightthickness=0, bg="#000000")
        canvas.place(x=125, y=0)
        img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        canvas.create_image(20, 20, anchor=NW, image=img)

        # buttons
        btn_tv1 = Button(admin_page, text="Admin Table", bg="#a5cf00", fg="#000000", font="Halvetica 12 bold",
                         borderwidth=10,
                         highlightthickness=0, command=table_1)
        btn_tv1.place(x=185, y=250)

        admin_page.mainloop()


AllInOne(root)
root.mainloop()
