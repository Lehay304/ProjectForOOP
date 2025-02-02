from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import json
import os

# Загрузка файла разметки
Builder.load_file('auth.kv')

# Класс для окна входа
class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        # Проверка введенных данных
        user = self.username.text
        pwd = self.password.text
        
        if not os.path.exists('users.json'):
            self.show_error('Нет зарегистрированных пользователей!')
            return

        with open('users.json', 'r') as f:
            users = json.load(f)
            
        if user in users and users[user] == pwd:
            self.reset_fields()
            self.manager.current = 'welcome'
            self.manager.get_screen('welcome').label.text = f'Добро пожаловать, {user}!'
        else:
            self.show_error('Неверный логин или пароль!')

    def show_error(self, message):
        popup = Popup(title='Ошибка',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def reset_fields(self):
        self.username.text = ''
        self.password.text = ''

# Класс для окна регистрации
class RegisterScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def register(self):
        user = self.username.text
        pwd = self.password.text
        
        if not user or not pwd:
            self.show_error('Заполните все поля!')
            return
            
        users = {}
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
        
        if user in users:
            self.show_error('Пользователь уже существует!')
        else:
            users[user] = pwd
            with open('users.json', 'w') as f:
                json.dump(users, f)
            self.reset_fields()
            self.manager.current = 'login'

    def show_error(self, message):
        popup = Popup(title='Ошибка',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def reset_fields(self):
        self.username.text = ''
        self.password.text = ''

# Экран приветствия
class WelcomeScreen(Screen):
    label = ObjectProperty(None)

# Менеджер экранов
class ScreenManagement(ScreenManager):
    pass

# Основное приложение
class AuthApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    AuthApp().run()