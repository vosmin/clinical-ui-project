import pandas as pd

def view_note_by_date(patient_id, date):
    try:
        df_notes = pd.read_csv("data/Notes.csv")
        df_patients = pd.read_csv("data/Patient_data.csv", delimiter='\t')
        matches = df_patients[(df_patients['Patient_ID'] == patient_id) & (df_patients['Visit_time'] == date)]
        if matches.empty:
            return "No visit found for that patient on given date."
        note_ids = matches['Note_ID'].unique()
        selected_notes = df_notes[df_notes['Note_ID'].isin(note_ids)]
        if selected_notes.empty:
            return "No notes found."
        return selected_notes[['Note_type', 'Note_text']].to_string()
    except Exception as e:
        return f"Error viewing note: {e}"