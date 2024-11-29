from tkinter import *
from tkinter import ttk
import catalog

def close_window(root):
    root.destroy()
    catalog.create_catalog()

def create_card():
    root = Tk()
    root.configure(bg="#ffffff")
    root.geometry("600x400")
    panel = Label(text="Товар")
    panel.pack()
    panel.place(height=150,width=150,x=100,y=50)
    panel1 = Label(text="Здесь должно быть описание")
    panel1.pack()
    panel1.place(height=150,width=250,x=300,y=50)
    btn1 = Button(text="Арендовать")
    btn1.place(x=120,y=250,height=50,width=100)
    panel2 = Label(text="Здесь должны быть  отзывы")
    panel2.pack()
    panel2.place(height=150,width=250,x=300,y=220)
    spinbox = ttk.Spinbox(from_=1.0, to=100.0)
    spinbox.pack(anchor=W)
    spinbox.place(height=20,width=70,x=50,y=260)
    spinbox_var = StringVar(value=1)
    Btn3 = Button(text="Вернутся")
    Btn3.place(height=50,width=100,x=120,y=300)
    Btn3.bind("<Button-1>", lambda event: close_window(root))
    root.mainloop()