import pandas as pd
import os
import random
import string
import tkinter as tk
from tkinter import messagebox

class Patient:
    def __init__(self, patient_id):
        self.patient_id = str(patient_id).strip()

    def retrieve_latest_visit(self):
        try:
            path = "output/updated_patient_data.csv" if os.path.exists("output/updated_patient_data.csv") else "data/Patient_data.csv"
            df = pd.read_csv(path, delimiter=",")
            df.columns = df.columns.str.strip()
            df["Patient_ID"] = df["Patient_ID"].astype(str).str.strip()
            visits = df[df["Patient_ID"] == self.patient_id]
            if visits.empty:
                return "Patient ID not found."
            latest = visits.sort_values(by="Visit_time", ascending=False).iloc[0]
            return latest.to_string()
        except Exception as e:
            return f"Error retrieving patient: {e}"

    def remove_from_file(self):
        try:
            df = pd.read_csv("data/Patient_data.csv", delimiter=",")
            df["Patient_ID"] = df["Patient_ID"].astype(str).str.strip()
            df = df[df["Patient_ID"] != self.patient_id]
            df.to_csv("output/updated_patient_data.csv", index=False)
            return f"All records for Patient {self.patient_id} removed."
        except Exception as e:
            return f"Error removing patient: {e}"

    @staticmethod
    def count_visits_by_date(date_str):
        try:
            df = pd.read_csv("data/Patient_data.csv", delimiter=",")
            df.columns = df.columns.str.strip()
            df["Visit_time"] = df["Visit_time"].astype(str).str.strip()
            count = df[df["Visit_time"] == str(date_str).strip()].shape[0]
            return f"Total visits on {date_str}: {count}"
        except Exception as e:
            return f"Error counting visits: {e}"

    @staticmethod
    def add_patient_gui(window, log_action):
        top = tk.Toplevel(window)
        top.title("Add Patient")

        fields = ["Patient_ID", "Visit_time", "Visit_department", "Gender", "Race", "Age", "Ethnicity", "Insurance", "Zip_code", "Chief complaint", "Note_ID", "Note_type"]
        entries = {}

        for field in fields:
            tk.Label(top, text=field).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries[field] = entry

        def submit():
            try:
                df = pd.read_csv("data/Patient_data.csv", delimiter=",")
                df.columns = df.columns.str.strip()
                data = {k.strip(): e.get().strip() for k, e in entries.items()}
                patient_id = data["Patient_ID"]
                visit_id = ''.join(random.choices(string.digits, k=6))
                data["Visit_ID"] = visit_id
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                df.to_csv("output/updated_patient_data.csv", index=False)
                log_action("add_patient")
                messagebox.showinfo("Success", f"Patient {patient_id} added with Visit ID {visit_id}")
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text="Submit", command=submit).pack()