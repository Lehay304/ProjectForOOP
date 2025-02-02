import tkinter as tk
import json
from tkinter import *
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title('Вход')
        master.geometry('300x150')

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.label_username = ttk.Label(master, text='Логин')
        self.label_password = ttk.Label(master, text='Пароль')
        self.entry_username = ttk.Entry(master)
        self.entry_password = ttk.Entry(master, show="*")
        self.button_login = ttk.Button(master, text = 'Войти', command = self.login)
        self.button_registration = ttk.Button(master, text = 'Регистрация', command = self.open_registration)

        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_registration.grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Ошибка", "Все поля должны быть зарлнены")
            return

        if self.check_credentials(username, password):
            self.master.destroy()
            self.open_main_app(username)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def check_credentials(self, username, password):
        try:
            with open("user.json", "r") as file:
                user = json.load(file)
                if username in user and user[username] == password:
                    return True
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не был найден")
        return False

    def open_registration(self):
        RegisrationWindow(tk.Toplevel(self.master))

    def open_main_app(self, username):
        root = tk.Tk()
        app = MainApplication(root, username)
        root.mainloop()

class RegisrationWindow:
    def __init__(self, master):
        self.master = master
        master.title("Регистрация")
        master.geometry("300x200")

        self.label_username = ttk.Label(master, text="Логин")
        self.label_password = ttk.Label(master, text="Пароль")
        self.label_confirm = ttk.Label(master, text="Повторите пароль")
        self.entry_username = ttk.Entry(master)
        self.entry_password = ttk.Entry(master, show="*")
        self.entry_confirm = ttk.Entry(master, show="*")
        self.button_register = ttk.Button(master, text="Зарегистрироваться", command=self.register)
        
        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.label_confirm.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.entry_confirm.grid(row=2, column=1, padx=10, pady=5)
        self.button_register.grid(row=3, column=0, columnspan=2, pady=10)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()

        if not username or not password or not confirm:
            messagebox.showwarning("Ошибка", "Все поля должны быть зарлнены")
            return

        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
        
        try:
            with open("user.json", "r") as file:
                try:
                    user = json.load(file)
                except json.JSONDecodeError:
                    user = {}
        except FileNotFoundError:
            user = {}

        if username in user:
            messagebox.showerror("Ошибка", "Пользователь уже зарегестрирован")
            return

        user[username] = password

        with open("user.json", "w") as file:
            user = json.dump(user, file)
        
        messagebox.showinfo("Успех!", "Регистрация завершена")
        self.master.destroy()

class MainApplication:
    def __init__(self, master, username):
        self.master = master
        master.title = ("Главное окно")
        master.geometry = ("300x100")

        self.label = ttk.Label(master, text=f"Добро пожаловать, {username}!")
        self.label.pack(pady=20)

        self.button_exit = ttk.Button(master, text="Выход", command=master.destroy)
        self.button_exit.pack()

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()
        
