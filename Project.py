import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.title("Отель Handsome")
root.geometry("400x450")

counts = 0

def vhod():
    counts =+ 1
    global labalg
    labalg["text"] = f"Вход не удался {counts} раз"

btnsend = ttk.Button(text="Вход", command=vhod)
btnsend.place(width=70, height=40, x=170, y=330)


labalg = ttk.Label(text="")
labalg.pack()

enterlogin = ttk.Entry()
enterlogin.place(width=200, height=30,)

root.mainloop()

class Hotel:
    def __init__(self, customer, room, employee, service, hotelsystem, ia):
        self.customer = customer
        self.room = room
        self.employee = employee
        self.service = service
        self.hotelsystem = hotelsystem
        self.ia = ia

