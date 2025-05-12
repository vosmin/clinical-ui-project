import tkinter as tk
from tkinter import messagebox
from user import authenticate_user
from patient import *
from note import *
from stats import *
import datetime

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Clinical Data Warehouse UI")
        self.user_role = None
        self.username = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()
        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()
        tk.Button(self.window, text="Login", command=self.handle_login).pack()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = authenticate_user(username, password)
        if role:
            self.user_role = role
            self.username = username
            self.log_action("login_success")
            self.create_main_menu()
        else:
            self.log_action("login_failed")
            messagebox.showerror("Login Failed", "Invalid credentials")

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.window, text=f"Logged in as: {self.user_role}").pack()
        if self.user_role in ["nurse", "clinician"]:
            tk.Button(self.window, text="Retrieve Patient", command=self.dummy_action).pack()
            tk.Button(self.window, text="Add Patient", command=self.dummy_action).pack()
            tk.Button(self.window, text="Remove Patient", command=self.dummy_action).pack()
            tk.Button(self.window, text="Count Visits", command=self.dummy_action).pack()
            tk.Button(self.window, text="View Note", command=self.dummy_action).pack()
        elif self.user_role == "admin":
            tk.Button(self.window, text="Count Visits", command=self.dummy_action).pack()
        elif self.user_role == "management":
            tk.Button(self.window, text="Generate Statistics", command=self.dummy_action).pack()
        tk.Button(self.window, text="Exit", command=self.window.quit).pack()

    def log_action(self, action):
        with open("output/usage_log.csv", "a") as f:
            time = datetime.datetime.now().isoformat()
            f.write(f"{self.username},{self.user_role},{action},{time}\n")

    def dummy_action(self):
        messagebox.showinfo("Not Implemented", "This button is a placeholder.")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()
