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

        ttk.Label(master, text="Логин").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Label(master, text="пароль").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_username = ttk.Entry(master)
        self.entry_password = ttk.Entry(master, show="*")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)


        ttk.Button(master, text = 'Войти', command = self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(master, text = 'Регистрация', command = self.open_registration).grid(row=3, column=0, columnspan=2)


    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Ошибка", "Все поля должны быть зарлнены")
            return
        user_data = self.check_credentials(username, password)

        if user_data:
            self.master.destroy()
            self.open_main_app(user_data)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")


    def check_credentials(self, username, password):
        try:
            with open("user.json", "r") as file:
                user = json.load(file)
                if username in user and user[username]['password'] == password:
                    return user[username]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            messagebox.showerror("Ошибка", "Файл не был найден")
            return False
        return False


    def open_registration(self):
        RegistrationWindow(tk.Toplevel(self.master))


    def open_main_app(self, user_data):
        root = tk.Tk()
        MainApplication(root, user_data)
        root.mainloop()



class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        master.title("Регистрация")
        master.geometry("300x200")

        fields = [
            ("Логин", 0),
            ("Имя", 1),
            ("Фамилия", 2),
            ("Пароль", 3),
            ("Повторите пароль", 4)
        ]
        
        self.entries = {}
        for text, row in fields:
            label = ttk.Label(master, text=text)
            entry = ttk.Entry(master, show="*" if "пароль" in text.lower() else "")
            label.grid(row = row, column = 0, padx=10, pady=5, sticky=tk.W)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[text.replace(":", "")] = entry

        ttk.Button(master, text="Зарегистрироваться", command=self.register).grid(row=5, column=0, columnspan=2, pady=10)
        

    def register(self):
        data = {
            "login": self.entries["Логин"].get(),
            "first_name": self.entries["Имя"].get(),
            "last_name": self.entries["Фамилия"].get(),
            "password": self.entries["Пароль"].get(),
            "confirm": self.entries["Повторите пароль"].get()
        }
        if any(not value for key, value in data.items() if key != "confirm"):
            messagebox.showwarning("Ошибка", "Все поля должны быть зарлнены")
            return

        if data["password"] != data["confirm"]:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
        
        try:
            with open("user.json", "r") as file:
                user = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user = {}

        if data["login"] in user:
            messagebox.showerror("Ошибка", "Пользователь уже зарегестрирован")
            return

        user[data["login"]] = {
            "password": data["password"],
            "first_name": data["first_name"],
            "last_name": data["last_name"]
        }

        with open("user.json", "w") as file:
            json.dump(user, file, indent=4)
        
        messagebox.showinfo("Успех!", "Регистрация завершена")
        self.master.destroy()

class MainApplication:
    def __init__(self, master, user_data):
        self.master = master
        self.user_data = user_data
        master.title("Главное окно")
        master.geometry("300x500")

        user_info = f"Добро пожаловать, {user_data["first_name"]} {user_data["last_name"]}! \nЧто вы хотите сделать?"

        ttk.Label(master, text=user_info).place(x=85, y=20)
        ttk.Button(master, text="Забронировать комнату",command=self.open_order_room).place(x=1, y=10)
        ttk.Button(master, text="Выход", command=master.destroy).place(x=10, y=467)

    def open_order_room(self, user_data):
        root = tk.Tk()
        OrderRoomWindow(root, user_data)
        root.mainloop()

class OrderRoomWindow:
    def __init__(self, master, user_data):
        self.master = master
        self.user_data = user_data
        master.title("Забронировать комнату")
        master.geometry("600x400")

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()
        
