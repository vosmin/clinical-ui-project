import pandas as pd

class Note:
    def __init__(self, patient_id, visit_date):
        self.patient_id = str(patient_id).strip()
        self.visit_date = str(visit_date).strip()

    def fetch_notes(self):
        try:
            df_notes = pd.read_csv("data/Notes.csv")
            df_patients = pd.read_csv("data/Patient_data.csv", delimiter=",")
            df_patients["Patient_ID"] = df_patients["Patient_ID"].astype(str).str.strip()
            df_patients["Visit_time"] = df_patients["Visit_time"].astype(str).str.strip()
            df_notes["Note_ID"] = df_notes["Note_ID"].astype(str).str.strip()

            matches = df_patients[
                (df_patients["Patient_ID"] == self.patient_id) &
                (df_patients["Visit_time"] == self.visit_date)
            ]

            if matches.empty:
                return "No visit found for that patient on given date."

            note_ids = matches["Note_ID"].astype(str).unique()
            df_notes["Note_ID"] = df_notes["Note_ID"].astype(str)
            selected_notes = df_notes[df_notes["Note_ID"].isin(note_ids)]

            if selected_notes.empty:
                return "No notes found."
            return selected_notes[["Note_text"]].to_string(index=False)
        except Exception as e:
            return f"Error viewing note: {e}"
