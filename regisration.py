from tkinter import *
import psycopg2

conn = psycopg2.connect(user="postgres",
                        password="root",
                        host="localhost",
                        port="5432",
                        database="renteasy")
with conn:
    cursor = conn.cursor()

    def addBut():
        cursor.execute(f'SELECT `id`, `login`, `password` FROM `user` WHERE `login`="{login.get()}" AND `password`="{Password.get()}"')
        records =cursor.fetchall()
        print(records)
        if len(records)!=0:
            text.delete("0.0",END)  
            text.insert("1.0", "Вход успешно выполнен") 
        else:
            text.delete("0.0",END)
            text.insert("1.0", "Неверный логин или пароль")
        

    def resetList():
        cursor.execute("SELECT * FROM `user` ")
    
    def register():
        cursor.execute(f'SELECT `id`, `login` FROM `user` WHERE `login`="{login.get()}"')
        prov=cursor.fetchall()
        if len(prov)!=0:
            text.delete("0.0",END)
            text.insert("1.0", "Такой логин уже существует ")
            
        else:
            if len(Password.get()) < 8:
                text.delete("0.0",END)
                text.insert("1.0","Ваш пароль менее 8 символов")
            elif not any(map(str.isdigit, Password.get())):
                text.delete("0.0",END)
                text.insert("1.0","Убедитесь, что в вашем пароле есть цифра")
            elif not any(map(str.isupper, Password.get())):
                text.delete("0.0",END)
                text.insert("1.0","Убедитесь, что в вашем пароле есть заглавная буква")
            else:   
                cursor.execute(f"INSERT INTO `user`(`login`, `password`) VALUES ('{login.get()}','{Password.get()}')")
                conn.commit()
                resetList()
                text.delete("0.0",END)
                text.insert("1.0", "Вы успешно зарегестрировались")
    
root = Tk()
root.configure(bg="#ffffff")
root.geometry("600x400")
login_btn = PhotoImage(file = "2.png")
reg_btn = PhotoImage(file = "3.png")


text = Text(height=2, width= 29,background="#ffffff")
login=Entry(background="#6d6d6d")
Password=Entry(background="#6d6d6d")
Btn1 = Button(text="Вход", command=addBut,image = login_btn,border=0,background="#ffffff")
Btn2 = Button(text="Регистрация",command=register,image = reg_btn,border=0,background="#ffffff")
Lablog=Label(text="Login:",background="#E2E2E2")
Labpass=Label(text="Password:",background="#E2E2E2")



login.place(x=200,y=150,width=200 , height=35)
Password.place(x=200,y=220,width=200,height=35)
Btn1.place(x=200, y=300 , width= 200 , height= 50 )
Btn2.place(x=200, y=350 , width= 200 , height= 50)
Lablog.place(x=220,y=123,width=150)
Labpass.place(x=220,y=190,width=150)
text.pack( expand=0,)

root.mainloop()