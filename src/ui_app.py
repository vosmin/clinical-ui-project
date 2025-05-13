import tkinter as tk
from tkinter import messagebox
from user import User
from patient import Patient
from note import Note
from stats import generate_statistics
import datetime
import pandas as pd

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
        user = User(username, password)
        if user.authenticate():
            self.user_role = user.role
            self.username = user.username
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
        if pid:
            patient = Patient(pid)
            info = patient.retrieve_latest_visit()
            messagebox.showinfo("Patient Info", info)
            self.log_action("retrieve_patient")

    def add_patient_ui(self):
        Patient.add_patient_gui(self.window, self.log_action)

    def remove_patient_ui(self):
        pid = self.prompt("Enter Patient ID to remove")
        if pid:
            patient = Patient(pid)
            msg = patient.remove_from_file()
            messagebox.showinfo("Remove Patient", msg)
            self.log_action("remove_patient")

    def count_visits_ui(self):
        top = tk.Toplevel()
        top.title("Count Visits")

        try:
            df = pd.read_csv("data/Patient_data.csv", delimiter=",")
            df.columns = df.columns.str.strip()
            df["Visit_time"] = df["Visit_time"].astype(str).str.strip()
            visit_dates = sorted(df["Visit_time"].unique())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient data: {e}")
            return

        tk.Label(top, text="Select Visit Date").pack()
        date_var = tk.StringVar()
        tk.OptionMenu(top, date_var, *visit_dates).pack()

        def submit():
            date = date_var.get()
            if not date:
                messagebox.showerror("Input Error", "Please select a date.")
                return
            result = Patient.count_visits_by_date(date)
            messagebox.showinfo("Visit Count", result)
            self.log_action("count_visits")
            top.destroy()

        tk.Button(top, text="Count Visits", command=submit).pack()

    def view_note_ui(self):
        top = tk.Toplevel()
        top.title("View Note")

        try:
            df = pd.read_csv("data/Patient_data.csv", delimiter=",")
            df["Patient_ID"] = df["Patient_ID"].astype(str).str.strip()
            df["Visit_time"] = df["Visit_time"].astype(str).str.strip()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient data: {e}")
            return

        tk.Label(top, text="Select Patient ID").pack()
        patient_var = tk.StringVar()
        tk.OptionMenu(top, patient_var, *sorted(df["Patient_ID"].unique())).pack()

        tk.Label(top, text="Select Visit Date").pack()
        date_var = tk.StringVar()
        date_menu = tk.OptionMenu(top, date_var, "")
        date_menu.pack()

        def update_dates(*args):
            pid = patient_var.get()
            dates = df[df["Patient_ID"] == pid]["Visit_time"].unique()
            date_var.set("")
            date_menu["menu"].delete(0, "end")
            for date in sorted(dates):
                date_menu["menu"].add_command(label=date, command=tk._setit(date_var, date))

        patient_var.trace("w", update_dates)

        def submit():
            pid = patient_var.get()
            date = date_var.get()
            if not pid or not date:
                messagebox.showerror("Input Error", "Please select both Patient ID and Date.")
                return
            note = Note(pid, date)
            messagebox.showinfo("Clinical Note", note.fetch_notes())
            self.log_action("view_note")
            top.destroy()

        tk.Button(top, text="View Note", command=submit).pack()

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
