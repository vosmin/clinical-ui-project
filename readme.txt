# Clinical Data Warehouse UI (HI 741 Final Project)

This project is a graphical user interface (GUI) application developed in Python using Tkinter to interact with a clinical data warehouse. It enables different types of healthcare users (clinicians, nurses, admins, management) to view, manage, and analyze patient data.

---

## ✅ Features

- **Login System**: Authenticates users using `Credentials.csv`, with role-based access
- **Role-Based UI**:
  - `admin`: count visits
  - `management`: generate statistics
  - `nurse` & `clinician`: full access (add, remove, view patients, read notes, count visits)
- **Core Actions**:
  - Retrieve Patient Info
  - Add/Remove Patient Records
  - Count Visits by Date
  - View Clinical Notes by Date
  - Generate Key Statistics (e.g. patient demographics)
- **Data Logging**:
  - Logs each login and action performed
  - Tracks failed login attempts
- **CSV Integration**:
  - Updates `Patient_data.csv` and `usage_log.csv` in real time

---

## 🗂 Project Structure

