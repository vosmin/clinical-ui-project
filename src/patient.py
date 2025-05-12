import pandas as pd
import random
import string

def retrieve_patient(patient_id):
    try:
        df = pd.read_csv("data/Patient_data.csv", delimiter='\t')
        patient_visits = df[df['Patient_ID'] == patient_id]
        if patient_visits.empty:
            return "Patient ID not found."
        latest = patient_visits.sort_values(by="Visit_time", ascending=False).iloc[0]
        return latest.to_string()
    except Exception as e:
        return f"Error retrieving patient: {e}"

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
            df = pd.read_csv("data/Patient_data.csv", delimiter='\t')
            data = {k: e.get() for k, e in entries.items()}
            patient_id = data["Patient_ID"]
            visit_id = ''.join(random.choices(string.digits, k=6))
            data["Visit_ID"] = visit_id
            df = df.append(data, ignore_index=True)
            df.to_csv("output/updated_patient_data.csv", index=False)
            log_action("add_patient")
            messagebox.showinfo("Success", f"Patient {patient_id} added with Visit ID {visit_id}")
            top.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(top, text="Submit", command=submit).pack()

def remove_patient(patient_id):
    try:
        df = pd.read_csv("data/Patient_data.csv", delimiter='\t')
        if patient_id not in df['Patient_ID'].values:
            return "Patient ID not found."
        df = df[df['Patient_ID'] != patient_id]
        df.to_csv("output/updated_patient_data.csv", index=False)
        return f"All records for Patient {patient_id} removed."
    except Exception as e:
        return f"Error removing patient: {e}"

def count_visits_by_date(date_str):
    try:
        df = pd.read_csv("data/Patient_data.csv", delimiter='\t')
        count = df[df['Visit_time'] == date_str].shape[0]
        return f"Total visits on {date_str}: {count}"
    except Exception as e:
        return f"Error counting visits: {e}"
