Clinical Data Warehouse UI (HI 741 Final Project)

This is a role-based graphical user interface (GUI) application developed in Python using Tkinter, designed for clinical data interaction and visualization. Users such as clinicians, nurses, administrators, and managers can securely log in to access, manage, and analyze patient data stored in CSV files.



Features:

Login System
- Authenticates users using credentials stored in `data/Credentials.csv`
- Differentiates user roles: `clinician`, `nurse`, `admin`, and `management`
- Tracks successful and failed login attempts

Role-Based Functionality:


Core Functionalities:

- Retrieve Patient Info: View latest visit data for a patient
- Add New Patient: GUI form to input patient details and create a new visit
- Remove Patient: Deletes all records associated with a given Patient ID
- Count Visits by Date: Calculates and displays the number of visits for a selected date
- View Clinical Notes: Retrieves visit-specific notes for a patient on a selected date
- Generate Statistics: Produces a bar chart showing patient race distribution

Logging:

- All actions (including failed logins) are logged to `output/usage_log.csv` with timestamps
- Patient additions/removals update `output/updated_patient_data.csv` accordingly



Project Structure:


clinical-ui-project/
├── data/                         # Input CSVs: Credentials.csv, Patient_data.csv, Notes.csv, Credentials.csv
├── output/                       # Output CSVs + statistics image
│   ├── updated_patient_data.csv
│   ├── usage_log.csv
│   └── statistics_plot.png
├── src/                          # Source code
│   ├── main.py
│   ├── ui_app.py
│   ├── user.py
│   ├── patient.py
│   ├── note.py
│   └── stats.py
├── UML_diagram.png               # UML diagram of class design (to be included)
├── README.md
└── requirements.txt


How to Run

1. Set up the environment
   bash
   pip install -r requirements.txt
   

2. Ensure the following directories and CSV files exist:
   - `data/Credentials.csv`
   - `data/Patient_data.csv`
   - `data/Notes.csv`
   - Create empty `output/` folder if missing

3. Run the application
   bash
   python main.py
   


Requirements:

Install the dependencies using pip:
bash
pip install -r requirements.txt


Major dependencies:
- `pandas`
- `matplotlib`
- `tkinter` (usually included with Python)
- `numpy`, `pillow`, etc. (for matplotlib rendering)


Developer Notes:

- All code follows modular design using object-oriented programming
- 4 core classes: `User`, `Patient`, `Note`, and `App` (GUI controller)
- Designed for extensibility with separated GUI logic and backend processing
- Each action is safely wrapped with error handling for user feedback and logging


UML Diagram:

Please refer to `UML_diagram.png` for class relationships and structure.

Github:


