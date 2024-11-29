from tkinter import *
import database.db as db
import card
def close_window(root):
    root.destroy()
    card.create_card()

def create_catalog():
    root = Tk()
    root.title("Каталог")
    root.geometry("500x500")
    result = db.get_categories()
    btns = [Button(border=0,background="#ffffff", text=str(result[i]['category'])) for i in range(len(result))]

    for btn in btns:
        btn.pack()
        btn.bind("<Button-1>", lambda event: close_window(root))
    for i in range(0, 10):
        if i == 0:
            btns[i].place(x=10, y=10 , height=150 , width=150)
        elif i == 1:
            btns[i].place(x=170, y=10 , height=150 , width=150)
        elif i == 2:
            btns[i].place(x=330, y=10 , height=150 , width=150)
        elif i == 3:
            btns[i].place(x=10, y=170 , height=150 , width=150)
        elif i == 4:
            btns[i].place(x=170, y=170 , height=150 , width=150)
        elif i == 5:
            btns[i].place(x=330, y=170 , height=150 , width=150)
        elif i == 6:
            btns[i].place(x=10, y=330 , height=150 , width=150)
        elif i == 7:
            btns[i].place(x=170, y=330 , height=150 , width=150)
        elif i == 8:
            btns[i].place(x=330, y=330 , height=150 , width=150)


    root.mainloop()