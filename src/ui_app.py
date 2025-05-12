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
            tk.Button(self.window, text="Retrieve Patient", command=self.retrieve_patient_ui).pack()
            tk.Button(self.window, text="Add Patient", command=self.add_patient_ui).pack()
            tk.Button(self.window, text="Remove Patient", command=self.remove_patient_ui).pack()
            tk.Button(self.window, text="Count Visits", command=self.count_visits_ui).pack()
            tk.Button(self.window, text="View Note", command=self.view_note_ui).pack()
        elif self.user_role == "admin":
            tk.Button(self.window, text="Count Visits", command=self.count_visits_ui).pack()
        elif self.user_role == "management":
            tk.Button(self.window, text="Generate Statistics", command=self.generate_statistics_ui).pack()
        tk.Button(self.window, text="Exit", command=self.window.quit).pack()

    def log_action(self, action):
        with open("output/usage_log.csv", "a") as f:
            time = datetime.datetime.now().isoformat()
            f.write(f"{self.username},{self.user_role},{action},{time}\n")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()

    def retrieve_patient_ui(self):
        pid = self.prompt("Enter Patient ID")
        info = retrieve_patient(pid)
        messagebox.showinfo("Patient Info", info)
        self.log_action("retrieve_patient")

    def add_patient_ui(self):
        add_patient_gui(self.window, self.log_action)

    def remove_patient_ui(self):
        pid = self.prompt("Enter Patient ID to remove")
        msg = remove_patient(pid)
        messagebox.showinfo("Remove Patient", msg)
        self.log_action("remove_patient")

    def count_visits_ui(self):
        date = self.prompt("Enter date (YYYY-MM-DD)")
        result = count_visits_by_date(date)
        messagebox.showinfo("Visit Count", result)
        self.log_action("count_visits")

    def view_note_ui(self):
        pid = self.prompt("Enter Patient ID")
        date = self.prompt("Enter Date (YYYY-MM-DD)")
        note = view_note_by_date(pid, date)
        messagebox.showinfo("Clinical Note", note)
        self.log_action("view_note")

    def generate_statistics_ui(self):
        stats_path = generate_statistics()
        messagebox.showinfo("Key Statistics", f"Statistics saved to {stats_path}")
        self.log_action("generate_statistics")

    def prompt(self, msg):
        win = tk.Toplevel()
        win.title("Input")
        tk.Label(win, text=msg).pack()
        entry = tk.Entry(win)
        entry.pack()
        output = []
        def submit():
            output.append(entry.get())
            win.destroy()
        tk.Button(win, text="Submit", command=submit).pack()
        win.grab_set()
        win.wait_window()
        return output[0] if output else ""
