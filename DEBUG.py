import os  #for path

import json

from tkinter import *
import tkinter.messagebox

from PIL import ImageTk, Image
import tkinter.font as tkFont

import random
import time
from datetime import datetime

import pymysql as mysql

mysql_conn = mysql.connect(host='127.0.0.1',user='root',passwd='shikhar007@#',database='sys')
cursor = mysql_conn.cursor()


root=Tk()
root.title("TYPE PACE ANALYSER")
root.geometry("1920x1200")
root.attributes("-fullscreen", True)

def esc_key_pressed(event):
    root.attributes("-fullscreen", False)
root.bind("<Escape>",esc_key_pressed)

img = ImageTk.PhotoImage(Image.open(r"qwerty.png")) #front_page_image
img_log = ImageTk.PhotoImage(Image.open(r"login.png")) #login_page_image
img_reg = ImageTk.PhotoImage(Image.open(r"register.png")) #register_page_image
img_sen_test = ImageTk.PhotoImage(Image.open(r"qwerty_.png"))
img_hist = ImageTk.PhotoImage(Image.open(r"records.png"))

front_label=Label(root,image=img).pack()

#login_module
def login():
    root.withdraw()

    log=Toplevel(root)
    log.title("LOGIN : ")
    log.geometry("1920x1200")
    log.attributes("-fullscreen", True)

    def esc_key_pressed(event):
        log.attributes("-fullscreen", False)
    log.bind("<Escape>", esc_key_pressed)

    l_log=Label(log,image=img_log).pack()

    def check_vals(): 

        check_query="SELECT username FROM users"
        cursor.execute(check_query)
        res=cursor.fetchall()
        if ((user_var.get(),) not in res):
            tkinter.messagebox.showinfo('WARNING !!!', 'NO SUCH USER EXIST !! REGISTRATION REQUIRED')
        else:
            check_query=f"SELECT password FROM users WHERE username='{user_var.get()}'"
            cursor.execute(check_query)
            res=cursor.fetchone()[0]
            if (res!=pswd_var.get()):
                tkinter.messagebox.showinfo('WARNING !!!', 'WRONG PASSWORD !!! \n TRY AGAIN')
            else:
                user_id=user_var.get()

                # game_module
                def random_sen_test():
                    log.withdraw()

                    sen_test = Toplevel()

                    sen_test.title("Random Sentence Speed Typing Test")
                    sen_test.geometry("1920x1200")
                    sen_test.attributes("-fullscreen", True)

                    def esc_key_pressed(event):
                        sen_test.attributes("-fullscreen", False)

                    sen_test.bind("<Escape>", esc_key_pressed)

                    l_san_test = Label(sen_test, image=img_sen_test).pack()

                    
                    title = Label(sen_test, text="TYPING SPEED TEST", anchor=CENTER, font="Arial 50 bold", bg="#00154F",
                                  fg='#F2BC94', relief="solid")
                    title.place(x=440, y=10)

                    # DISPLAY SENTENCES
                    fontStyle = tkFont.Font(family="Lucida Grande", size=25)
                    text = Label(sen_test, height='6', width='40', fg='gold', bg='red', font=fontStyle, wraplength=500,
                                 anchor=CENTER, justify=LEFT)
                    text.place(x='420', y='150')

                    def randomTXT():
                        f=open('Sentence.json')
                        data=json.load(f)
                        sentences=data['sentences']
                        # f = open('Sentence.txt').read()
                        # sentences = f.split('\n')
                        display = random.choice(sentences)
                        text.config(text=display)

                    randomTXT()
                    switch = Button(sen_test, text="SWITCH-UP", bg='red', fg='black', font="helvetica 20", padx=10,
                                    pady=10,
                                    relief=RAISED, command=randomTXT)
                    switch.place(x=700, y=470)

                    # // INPUT BOX FROM THE USER    //##
                    large_font = ('Verdana', 20)
                    e = Entry(sen_test, width='55', bg="#F2BC94", fg="black", font=large_font)
                    e.place(x=330, y=400)
                    e.focus()

                    # CREATING RESET BUTTON
                    def clearfunc():
                        global t0
                        t0=time.time()
                        print(t0)
                        e.delete(0, 'end')

                    reset = Button(sen_test, text="RESET", bg="black", fg="white", font="helvetica 20", padx=20,
                                   pady=10,
                                   relief=RAISED, command=clearfunc)
                    reset.place(x=450, y=470)


                    def calculate(*args, **kwargs):
                        t1 = time.time()
                        print(t1," ",t0)
                        st = e.get()
                        w_count = len(st.split())
                        mylabel = Label(sen_test, text="TOTAL WORDS: " + str(w_count))
                        mylabel.place(x=450, y=550)
                        mylabel = Label(sen_test, text="TIME TAKEN: " + str(round(t1 - t0)))
                        mylabel.place(x=700, y=550)
                        if (t1 - t0) >= 60:
                            temp = "POOR"
                            mylabel = Label(sen_test, text="SPEED: POOR")
                            mylabel.place(x=1000, y=550)
                        elif (t1 - t0) >= 30 and (t1 - t0) <= 60:
                            temp = "AVERAGE"
                            mylabel = Label(sen_test, text="SPEED: AVERAGE")
                            mylabel.place(x=1000, y=550)
                        else:
                            temp = "EXCELLENT"
                            mylabel = Label(sen_test, text="SPEED: EXCELLENT")
                            mylabel.place(x=1000, y=550)

                        now = datetime.now()
                        insert_query=f"INSERT INTO {user_id}_HISTORY(date_time,word_count,time_taken,speed) VALUES('"+str(now.strftime("%d/%m/%Y, %H:%M:%S"))+f"','{str(w_count)}','{str(round(t1 - t0))}','{temp}')"
                        cursor.execute(insert_query)
                        mysql_conn.commit()
                        time.sleep(1)
                        clearfunc()
                    clearfunc()
                    #calculate()
                    text_type_btn = Button(sen_test, text="RESULT", font="helvetica 20", padx=10, pady=10,
                                           relief=RAISED,
                                           command=calculate).place(x=1000, y=470)

                    # back_key_pressed
                    def back_to_login():
                        sen_test.withdraw()
                        log.deiconify()
                    back = Button(sen_test, text="BACK", font="helvetica 20", padx=10, pady=10, relief=RAISED,
                                  command=back_to_login).place(x=592, y=600)

                    def history():
                        sen_test.withdraw()
                        hist = Toplevel()

                        hist.title("HISTORY")
                        hist.geometry("1920x1200")
                        hist.attributes("-fullscreen", True)

                        def esc_key_pressed(event):
                            hist.attributes("-fullscreen", False)

                        hist.bind("<Escape>", esc_key_pressed)

                        l_san_test = Label(hist, image=img_hist).pack()

                        def back_to_sen_test():
                            hist.withdraw()
                            sen_test.deiconify()

                        f_hist = Frame(hist, bg="black", relief=SUNKEN, borderwidth=20, padx=50, pady=10)
                        f_hist.place(relx=0.42, rely=0.8)
                        b = Button(f_hist, text="BACK", bg="firebrick1", fg="white", font="algerian 20 bold italic",
                                   command=back_to_sen_test).pack()


                        check_query=f"SELECT * FROM {user_id}_HISTORY"
                        cursor.execute(check_query)

                        if(len(cursor.fetchall())<5):
                            print(cursor.execute(check_query))
                            tkinter.messagebox.showinfo('COME AGAIN !!!', 'YOU HAVE NOT USED THIS PROGRAM MUCH \nFOR ANALYSING DETAILS!!!' )
                        else:
                            check_query=f"SELECT * FROM {user_id}_HISTORY ORDER BY ID DESC LIMIT 5"
                            cursor.execute(check_query)
                            (records_list1,records_list2,records_list3,records_list4,records_list5)=cursor.fetchall()
                            
                            show = Frame(hist, width=1200, height=800, bg="azure3", padx=40, pady=40)
                            show.place(relx=0.25, rely=0.4)
                            

                            d_t = Label(show, width='20', height='2', text="DATE AND TIME ", font="Arial 10 bold").grid(
                                row=0, column=0)
                            w = Label(show, width='20', height='2', text="WORD COUNT ", font="Arial 10 bold").grid(
                                row=0, column=1)
                            t = Label(show, width='20', height='2', text="TIME TAKEN ", font="Arial 10 bold").grid(
                                row=0, column=2)
                            s = Label(show, width='20', height='2', text="SPEED ", font="Arial 10 bold").grid(
                                row=0, column=3)

                            d_t1 = Label(show, width='20', height='2', text=str(records_list1[1]), font="Arial 10 bold").grid(
                                row=1, column=0)
                            w = Label(show, width='20', height='2', text=str(records_list1[2]), font="Arial 10 bold").grid(
                                row=1, column=1)
                            t = Label(show, width='20', height='2',text=str(records_list1[3]), font="Arial 10 bold").grid(
                                row=1, column=2)
                            s = Label(show, width='20', height='2',text=str(records_list1[4]), font="Arial 10 bold").grid(
                                row=1, column=3)

                            d_t1 = Label(show, width='20', height='2', text=str(records_list2[1]),
                                         font="Arial 10 bold").grid(
                                row=2, column=0)
                            w = Label(show, width='20', height='2', text=str(records_list2[2]),
                                      font="Arial 10 bold").grid(
                                row=2, column=1)
                            t = Label(show, width='20', height='2', text=str(records_list1[3]),
                                      font="Arial 10 bold").grid(
                                row=2, column=2)
                            s = Label(show, width='20', height='2', text=str(records_list1[4]),
                                      font="Arial 10 bold").grid(
                                row=2, column=3)

                            d_t1 = Label(show, width='20', height='2', text=str(records_list3[1]),
                                         font="Arial 10 bold").grid(
                                row=3, column=0)
                            w = Label(show, width='20', height='2', text=str(records_list3[2]),
                                      font="Arial 10 bold").grid(
                                row=3, column=1)
                            t = Label(show, width='20', height='2', text=str(records_list3[3]),
                                      font="Arial 10 bold").grid(
                                row=3, column=2)
                            s = Label(show, width='20', height='2', text=str(records_list3[4]),
                                      font="Arial 10 bold").grid(
                                row=3, column=3)

                            d_t1 = Label(show, width='20', height='2', text=str(records_list4[1]),
                                         font="Arial 10 bold").grid(
                                row=4, column=0)
                            w = Label(show, width='20', height='2', text=str(records_list4[2]),
                                      font="Arial 10 bold").grid(
                                row=4, column=1)
                            t = Label(show, width='20', height='2', text=str(records_list4[3]),
                                      font="Arial 10 bold").grid(
                                row=4, column=2)
                            s = Label(show, width='20', height='2', text=str(records_list4[4]),
                                      font="Arial 10 bold").grid(
                                row=4, column=3)

                            d_t1 = Label(show, width='20', height='2', text=str(records_list5[1]),
                                         font="Arial 10 bold").grid(
                                row=5, column=0)
                            w = Label(show, width='20', height='2', text=str(records_list5[2]),
                                      font="Arial 10 bold").grid(
                                row=5, column=1)
                            t = Label(show, width='20', height='2', text=str(records_list5[3]),
                                      font="Arial 10 bold").grid(
                                row=5, column=2)
                            s = Label(show, width='20', height='2', text=str(records_list5[4]),
                                      font="Arial 10 bold").grid(
                                row=5, column=3)


                    his = Button(sen_test, text="HISTORY", font="helvetica 20", padx=10, pady=10, relief=RAISED,
                                 command=history).place(x=870, y=600)
                random_sen_test()


    f_log = Frame(log, width=1200, height=800, bg="azure3",padx=40,pady=40)
    f_log.place(relx=0.3, rely=0.4)

    user = Label(f_log,width='20',height='2', text="USERNAME -> ",font="Arial 10 bold").grid(row=0, column=0,pady=40)
    pswd = Label(f_log,width='20',height='2', text="PASSWORD -> ",font="Arial 10 bold").grid(row=1, column=0,pady=40)

    user_var = StringVar()
    pswd_var = StringVar()

    user_entry = Entry(f_log,width='30', textvariable=user_var,font=10).grid(row=0, column=1,padx=10)
    pswd_entry = Entry(f_log,width='30', textvariable=pswd_var,font=10).grid(row=1, column=1,padx=10)

    submit = Button(f_log,width='20',height='2', text="SUBMIT", command=check_vals,font="Arial 10 bold").grid(column=1,pady=30)

    # back_key_pressed
    def back_to_main():
        log.withdraw()
        root.deiconify()
    back = Button(f_log,width='20',height='2', text="BACK", command=back_to_main,font="Arial 10 bold").grid(row=2,column=0,padx=20)

#register_module
def register():
    root.withdraw()

    #back_key_pressed
    def back_to_main():
        reg.withdraw()
        root.deiconify()

    reg=Toplevel(root)
    reg.title("REGISTER : ")
    reg.geometry("1920x1200")
    reg.attributes("-fullscreen", True)

    def esc_key_pressed(event):
        reg.attributes("-fullscreen", False)
    reg.bind("<Escape>", esc_key_pressed)

    l_reg=Label(reg,image=img_reg).pack()

    def getvals():
        check_query="SELECT username FROM users"
        cursor.execute(check_query)
        res=cursor.fetchall()
        if ((user_var.get(),) in res):
            tkinter.messagebox.showinfo('WARNING !!!', 'Username Exists !!! \n Try Another User Name')
        if (pswd_var.get() != c_pswd_var.get()):
            tkinter.messagebox.showinfo('WARNING !!!', 'Password not matched \n Confirm Password Again')
        else:
            insert_query=f"INSERT INTO users(name, username, password) VALUES('{name_var.get()}','{user_var.get()}','{pswd_var.get()}')"
            cursor.execute(insert_query)
            create_query=f"CREATE TABLE {user_var.get()}_HISTORY(ID INT AUTO_INCREMENT PRIMARY KEY, date_time VARCHAR(45), word_count VARCHAR(45), time_taken VARCHAR(45), speed VARCHAR(12))"
            cursor.execute(create_query)
            mysql_conn.commit()
            tkinter.messagebox.showinfo('EXECUTED !!!', 'Registered Successfully! \n Enter Login Page')


    f_reg = Frame(reg, width=1200,height=800,bg="azure3",padx=40,pady=40)
    f_reg.place(relx=0.25,rely=0.4)

    name=Label(f_reg,width='20',height='2',text="NAME -> ",font="Arial 10 bold").grid(row=0,column=0,pady=10)
    email=Label(f_reg,width='20',height='2',text="E-Mail Id -> ",font="Arial 10 bold").grid(row=1,column=0,pady=10)
    user = Label(f_reg,width='20',height='2', text="USERNAME -> ",font="Arial 10 bold").grid(row=2, column=0,pady=10)
    pswd = Label(f_reg,width='20', height='2',text="PASSWORD -> ",font="Arial 10 bold").grid(row=3, column=0,pady=10)
    c_pswd = Label(f_reg,width='20',height='2', text="CONFIRM PASSWORD -> ",font="Arial 10 bold").grid(row=4, column=0,pady=10)

    name_var=StringVar()
    email_var = StringVar()
    user_var = StringVar()
    pswd_var = StringVar()
    c_pswd_var = StringVar()

    name_entry=Entry(f_reg, width='25',textvariable=name_var,font="10").grid(row=0,column=1,padx=10)
    email_entry = Entry(f_reg, width='25',textvariable=email_var,font='10').grid(row=1,column=1,padx=10)
    user_entry = Entry(f_reg,width='25', textvariable=user_var,font='10').grid(row=2,column=1,padx=10)
    pswd_entry = Entry(f_reg,width='25', textvariable=pswd_var,font='10').grid(row=3,column=1,padx=10)
    c_pswd_entry = Entry(f_reg,width='25', textvariable=c_pswd_var,font='10').grid(row=4,column=1,padx=10)

    submit=Button(f_reg,width='30',height='2',text="SUBMIT",font="Arial 10 bold",command=getvals).grid(column=1,pady=30)

    def back_to_main(): # back_key_pressed
        reg.withdraw()
        root.deiconify()
    back=Button(f_reg,width='30',height='2',text="BACK",font="Arial 10 bold",command=back_to_main).grid(row=5,column=0,padx=40)

#exit_module
def exit():
    root.destroy()

#Login Button
f1=Frame(front_label,bg="black",relief=SUNKEN,borderwidth=20,padx=50,pady=10)
f1.place(relx=0.05,rely=0.65)
b1=Button(f1,text=" LOGIN ",bg="firebrick1",fg="white",font="algerian 20 bold italic",command=login).pack()

#Register Button
f2=Frame(front_label,bg="black",relief=SUNKEN,borderwidth=20,padx=50,pady=10)
f2.place(relx=0.75,rely=0.65)
b2=Button(f2,text="REGISTER",bg="firebrick1",fg="white",font="algerian 20 bold italic",command=register).pack()

#Exit Button
f=Frame(front_label,bg="black",relief=SUNKEN,borderwidth=20,padx=50,pady=10)
f.place(relx=0.42,rely=0.8)
b=Button(f,text="EXIT",bg="firebrick1",fg="white",font="algerian 20 bold italic",command = exit).pack()

root.mainloop()