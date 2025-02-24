import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class Room:
    def __init__(self, room_number, room_type, price_per_night):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night

    def __str__(self):
        return f"Номер {self.room_number} ({self.room_type}): {self.price_per_night} Руб/ночь"

    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type": self.room_type,
            "price_per_night": self.price_per_night
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["room_number"], data["room_type"], data["price_per_night"])

class Guest:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.bookings = []

    def add_booking(self, booking):
        self.bookings.append(booking)

    def cancel_booking(self, booking):
        booking.cancel()

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "bookings": [booking.to_dict() for booking in self.bookings]
        }

    @classmethod
    def from_dict(cls, data):
        guest = cls(data["name"], data["phone"], data["email"])
        for booking_data in data["bookings"]:
            booking = Booking.from_dict(booking_data)
            guest.add_booking(booking)
        return guest

class Booking:
    def __init__(self, guest, room, check_in_date, check_out_date):
        self.guest = guest
        self.room = room
        self.check_in_date = datetime.strptime(check_in_date, "%d-%m-%Y")
        self.check_out_date = datetime.strptime(check_out_date, "%d-%m-%Y")
        self.status = "Забронированно"

    def calculate_total_cost(self):
        nights = (self.check_out_date - self.check_in_date).days
        return self.room.price_per_night * nights

    def cancel(self):
        self.status = "Закрыто"

    def to_dict(self):
        return {
            "guest_name": self.guest.name,
            "room_number": self.room.room_number,
            "check_in_date": self.check_in_date.strftime("%d-%m-%Y"),
            "check_out_date": self.check_out_date.strftime("%d-%m-%Y"),
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        guest = next((g for g in HotelApp.hotel.guests if g.name == data["guest_name"]), None)
        room = next((r for r in HotelApp.hotel.rooms if r.room_number == data["room_number"]), None)
        if guest and room:
            return cls(guest, room, data["check_in_date"], data["check_out_date"])
        return None

class Hotel:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.rooms = []
        self.guests = []
        self.bookings = []

    def add_room(self, room):
        self.rooms.append(room)

    def remove_room(self, room):
        self.rooms.remove(room)

    def add_guest(self, guest):
        self.guests.append(guest)

    def find_available_rooms(self, check_in_date, check_out_date):
        check_in = datetime.strptime(check_in_date, "%d-%m-%Y")
        check_out = datetime.strptime(check_out_date, "%d-%m-%Y")
        available_rooms = []
        for room in self.rooms:
            conflict = False
            for booking in self.bookings:
                if booking.room == room and booking.status == "Забронированно":
                    if not (check_out <= booking.check_in_date or check_in >= booking.check_out_date):
                        conflict = True
                        break
            if not conflict:
                available_rooms.append(room)
        return available_rooms

    def create_booking(self, guest, room, check_in_date, check_out_date):
        available_rooms = self.find_available_rooms(check_in_date, check_out_date)
        if room in available_rooms:
            new_booking = Booking(guest, room, check_in_date, check_out_date)
            self.bookings.append(new_booking)
            guest.add_booking(new_booking)
            return new_booking
        else:
            return None

    def cancel_booking(self, booking):
        booking.cancel()

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "rooms": [room.to_dict() for room in self.rooms],
            "guests": [guest.to_dict() for guest in self.guests],
            "bookings": [booking.to_dict() for booking in self.bookings]
        }

    @classmethod
    def from_dict(cls, data):
        hotel = cls(data["name"], data["address"])
        for room_data in data["rooms"]:
            room = Room.from_dict(room_data)
            hotel.add_room(room)
        for guest_data in data["guests"]:
            guest = Guest.from_dict(guest_data)
            hotel.add_guest(guest)
        for booking_data in data["bookings"]:
            booking = Booking.from_dict(booking_data)
            if booking:
                hotel.bookings.append(booking)
        return hotel

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение управлением отеля")
        self.hotel = Hotel("Вежливый лось", "ул. Попова 185")
        self.load_data()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_rooms_tab()
        self.create_guests_tab()
        self.create_bookings_tab()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_rooms_tab(self):
        rooms_tab = ttk.Frame(self.notebook)
        self.notebook.add(rooms_tab, text="Комнаты")

        ttk.Label(rooms_tab, text="Номер комнаты:").grid(row=0, column=0, padx=5, pady=5)
        self.room_number_entry = ttk.Entry(rooms_tab)
        self.room_number_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(rooms_tab, text="Тип комнаты:").grid(row=1, column=0, padx=5, pady=5)
        self.room_type_entry = ttk.Entry(rooms_tab)
        self.room_type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(rooms_tab, text="Цена за ночь:").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(rooms_tab)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(rooms_tab, text="Добавить", command=self.add_room).grid(row=3, column=0, columnspan=2, pady=10)

        self.rooms_listbox = tk.Listbox(rooms_tab)
        self.rooms_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.update_rooms_listbox()

    def create_guests_tab(self):
        guests_tab = ttk.Frame(self.notebook)
        self.notebook.add(guests_tab, text="Гости")

        ttk.Label(guests_tab, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.guest_name_entry = ttk.Entry(guests_tab)
        self.guest_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(guests_tab, text="Телефон:").grid(row=1, column=0, padx=5, pady=5)
        self.guest_phone_entry = ttk.Entry(guests_tab)
        self.guest_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(guests_tab, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.guest_email_entry = ttk.Entry(guests_tab)
        self.guest_email_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(guests_tab, text="Добавить", command=self.add_guest).grid(row=3, column=0, columnspan=2, pady=10)

        self.guests_listbox = tk.Listbox(guests_tab)
        self.guests_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.update_guests_listbox()

    def create_bookings_tab(self):
        bookings_tab = ttk.Frame(self.notebook)
        self.notebook.add(bookings_tab, text="Бронь")

        ttk.Label(bookings_tab, text="Гость:").grid(row=0, column=0, padx=5, pady=5)
        self.guest_combobox = ttk.Combobox(bookings_tab)
        self.guest_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.update_guest_combobox()

        ttk.Label(bookings_tab, text="Комната:").grid(row=1, column=0, padx=5, pady=5)
        self.room_combobox = ttk.Combobox(bookings_tab)
        self.room_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.update_room_combobox()

        ttk.Label(bookings_tab, text="Начало брони:").grid(row=2, column=0, padx=5, pady=5)
        self.check_in_entry = ttk.Entry(bookings_tab)
        self.check_in_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(bookings_tab, text="Конец брони:").grid(row=3, column=0, padx=5, pady=5)
        self.check_out_entry = ttk.Entry(bookings_tab)
        self.check_out_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(bookings_tab, text="Забронировать", command=self.create_booking).grid(row=4, column=0, columnspan=2, pady=10)

        self.bookings_listbox = tk.Listbox(bookings_tab)
        self.bookings_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.update_bookings_listbox()

    def add_room(self):
        room_number = self.room_number_entry.get()
        room_type = self.room_type_entry.get()
        price = self.price_entry.get()

        if room_number and room_type and price:
            try:
                price = float(price)
                room = Room(room_number, room_type, price)
                self.hotel.add_room(room)
                self.update_rooms_listbox()
                self.update_room_combobox()
                self.room_number_entry.delete(0, tk.END)
                self.room_type_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Ошибка", "цена должна быть указана как число.")
        else:
            messagebox.showerror("Ошибка", "заполнте все поля.")

    def add_guest(self):
        name = self.guest_name_entry.get()
        phone = self.guest_phone_entry.get()
        email = self.guest_email_entry.get()

        if name and phone and email:
            guest = Guest(name, phone, email)
            self.hotel.add_guest(guest)
            self.update_guests_listbox()
            self.update_guest_combobox()
            self.guest_name_entry.delete(0, tk.END)
            self.guest_phone_entry.delete(0, tk.END)
            self.guest_email_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "заполините все поля.")

    def create_booking(self):
        guest_index = self.guest_combobox.current()
        room_index = self.room_combobox.current()
        check_in = self.check_in_entry.get()
        check_out = self.check_out_entry.get()

        if guest_index != -1 and room_index != -1 and check_in and check_out:
            guest = self.hotel.guests[guest_index]
            room = self.hotel.rooms[room_index]
            booking = self.hotel.create_booking(guest, room, check_in, check_out)
            if booking:
                self.update_bookings_listbox()
                self.check_in_entry.delete(0, tk.END)
                self.check_out_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "комната уже забронираванна на эти даты.")
        else:
            messagebox.showerror("Ошибка", "заполните все поля")

    def update_rooms_listbox(self):
        self.rooms_listbox.delete(0, tk.END)
        for room in self.hotel.rooms:
            self.rooms_listbox.insert(tk.END, str(room))

    def update_guests_listbox(self):
        self.guests_listbox.delete(0, tk.END)
        for guest in self.hotel.guests:
            self.guests_listbox.insert(tk.END, f"{guest.name} ({guest.phone})")

    def update_bookings_listbox(self):
        self.bookings_listbox.delete(0, tk.END)
        for booking in self.hotel.bookings:
            self.bookings_listbox.insert(tk.END, f"{booking.guest.name} - {booking.room.room_number} ({booking.check_in_date.strftime('%d-%m-%Y')} до {booking.check_out_date.strftime('%d-%m-%Y')})")

    def update_guest_combobox(self):
        self.guest_combobox["values"] = [f"{guest.name} ({guest.phone})" for guest in self.hotel.guests]

    def update_room_combobox(self):
        self.room_combobox["values"] = [str(room) for room in self.hotel.rooms]

    def load_data(self):
        if os.path.exists("hotel_data.json"):
            with open("hotel_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.hotel = Hotel.from_dict(data)

    def save_data(self):
        with open("hotel_data.json", "w", encoding="utf-8") as file:
            json.dump(self.hotel.to_dict(), file, ensure_ascii=False , indent=4)

    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()