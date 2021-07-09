import tkinter
from tkinter import *
from tkinter import messagebox
import mysql.connector as mysql
from PIL import ImageTk, Image
from datetime import *
from tkinter.ttk import Combobox, Treeview

# window set up
root = Tk()
root.geometry("500x500")
root.config(bg="#000000")
root.title("Login Form")

# variables
now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")


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
            query = "SELECT IDNumber, Password, UserID FROM register"
            foreign_id = cursor.lastrowid
            cursor.execute(query)
            my_result = cursor.fetchall()

            for x in my_result:
                if x[0] == str(ent_idnum.get()) and x[1] == str(ent_passwd.get()):
                    foreign_id = x[2]
                    second_query = "INSERT INTO timesheet (LoggedInDate, LoggedInTime, IDNum, UserID) VALUES (%s, %s, " \
                                   " %s, %s) "
                    second_values = (now, date, ent_idnum.get(), foreign_id)
                    cursor.execute(second_query, second_values)
                    db.commit()
                    messagebox.showinfo("Success", "You Have Successfully Logged In")
                else:
                    messagebox.showerror("Error", "Incorrect ID Number/ Password combination")

        def user_logout():
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            cursor = db.cursor()
            query = "SELECT IDNumber, Password FROM register"
            # foreign_id = cursor.lastrowid
            cursor.execute(query)
            results = cursor.fetchall()

            for x in results:
                if x[0] == str(ent_idnum.get()) and x[1] == str(ent_passwd.get()):
                    second_query = "UPDATE timesheet SET LoggedOutDate = %s, LoggedOutTime = %s WHERE IDNum = %s"
                    second_values = (now, date, ent_idnum.get())
                    cursor.execute(second_query, second_values)
                    db.commit()
                    messagebox.showinfo("Success", "You Have Successfully Logged Out")
                else:
                    messagebox.showerror("Error", "Incorrect ID Number/ Password combination")

        # image
        canvas = Canvas(login, width=200, height=200, borderwidth=0, highlightthickness=0, bg="#000000")
        canvas.place(x=220, y=0)
        img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        canvas.create_image(20, 20, anchor=N, image=img)
        # labels
        lbl_idnum = Label(login, text="ID Number: ", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_idnum.place(x=120, y=225)
        ent_idnum = Entry(login)
        ent_idnum.place(x=245, y=225)
        lbl_passwd = Label(login, text="Password: ", bg="#000000", fg="#a5cf00", font="Halvetica 12 bold")
        lbl_passwd.place(x=120, y=255)
        ent_passwd = Entry(login)
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
        register.geometry("500x550")
        register.config(bg="#000000")

        def new_user():
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            if len(ent_idnum.get()) == 0 or len(ent_passwd.get()) == 0 or len(ent_cellnum.get()) == 0 or len(
                    ent_nextkin.get()) == 0 or len(ent_nextkincell.get()) == 0:
                messagebox.showerror("Error", "Please Fill In Each Field Correctly")
            elif combo_unit.get() == "Select Your Unit":
                messagebox.showerror("Error", "Please Select Your LC Unit")
            else:
                cursor = db.cursor()
                query = "INSERT INTO register (FullName, IDNumber, Password, CellNum, Unit) VALUES (%s, %s, %s, %s, %s)"
                values = (
                    ent_fullname.get(), ent_idnum.get(), ent_passwd.get(), ent_cellnum.get(), combo_unit.get())
                cursor.execute(query, values)
                db.commit()

                reusable_id = cursor.lastrowid

                second_query = "INSERT INTO emergency (UserID, IDNum, NextOfKin, NextOfKinNum) VALUES (%s, %s, %s, %s)"
                second_values = (reusable_id, ent_idnum.get(), ent_nextkin.get(), ent_nextkincell.get())
                cursor.execute(second_query, second_values)
                db.commit()

                messagebox.showinfo("Success", "You have Successfully Registered! Please Login On The Previous Window!")
                register.withdraw()
                self.login_window()

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
        # button
        btn_register = Button(register, text="Register", bg="#a5cf00", fg="#000000", font="Halvetica 12 bold",
                              borderwidth=10,
                              highlightthickness=0, command=new_user)
        btn_register.place(x=200, y=490)

        # combo box
        combo_unit = Combobox(register, width=17)
        combo_unit["values"] = ("Academy", "Business", "Staff")
        combo_unit["state"] = "readonly"
        combo_unit.set("Select Your Unit")
        combo_unit.place(x=280, y=380)
        # global combo_unit

        register.mainloop()

    def admin_window(self):
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
            query = "SELECT IDNumber, Password, Unit FROM register"
            foreign_id = cursor.lastrowid
            cursor.execute(query)
            my_result = cursor.fetchall()

            for x in my_result:
                if x[0] == str(ent_idnum2.get()) and x[1] == str(ent_passwd2.get()) and x[2] == "Staff":
                    messagebox.showinfo("Success", "You Have Successfully Logged In")
                    admin.withdraw()
                    self.admin_table()
                else:
                    messagebox.showerror("Error", "You Do Not Have Admin Privileges")

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
        ent_passwd2 = Entry(admin)
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

            def insert_user():
                tv_window = Frame(window, width=400, height=400, bg="#000000")
                tv_window.place(x=500, y=260)

                def submit():
                    my_db = mysql.connect(
                        host="localhost",
                        user="root",
                        passwd="@Lifechoices1234",
                        database="lifechoicesonline"
                    )

                    if len(ent1.get()) == 0 or len(ent2.get()) == 0 or len(ent3.get()) == 0 or len(
                            ent4.get()) == 0 or len(ent6.get()) == 0 or len(ent7.get()) == 0:
                        messagebox.showerror("Error", "Please Fill In Each Field Correctly")
                    elif combo_unit.get() == "Select Your Unit":
                        messagebox.showerror("Error", "Please Select Your LC Unit")
                    else:
                        my_cursor = my_db.cursor()
                        query = "INSERT INTO register (FullName, IDNumber, Password, CellNum, Unit) VALUES (%s, %s, " \
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

            # scroll bar
            # sb = Scrollbar(window, orient=HORIZONTAL)
            # sb.place(x=50, y=250)
            # tree.config(xscrollcommand=sb.set)
            # sb.config(command=tree.xview())

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

            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="@Lifechoices1234",
                database="lifechoicesonline"
            )

            cursor = db.cursor()
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
            btn_add.place(x=250, y=250)
            btn_edit = Button(window, text="Edit User", highlightthickness=0, borderwidth=10, font="Halvetica 12 bold")
            btn_edit.place(x=250, y=300)
            btn_remove = Button(window, text="Remove User", highlightthickness=0, borderwidth=10,
                                font="Halvetica 12 bold")
            btn_remove.place(x=230, y=350)

            window.mainloop()

        def remove_user():
            pass

        # image
        canvas = Canvas(admin_page, width=500, height=250, borderwidth=0, highlightthickness=0, bg="#000000")
        canvas.place(x=125, y=0)
        img = ImageTk.PhotoImage(Image.open("./Images/logo-2.jpg"))
        canvas.create_image(20, 20, anchor=NW, image=img)

        # buttons
        btn_tv1 = Button(admin_page, text="Admin Table", bg="#a5cf00", fg="#000000", font="Halvetica 12 bold",
                         borderwidth=10,
                         highlightthickness=0, command=table_1)
        btn_tv1.place(x=170, y=250)

        admin_page.mainloop()


AllInOne(root)
root.mainloop()
