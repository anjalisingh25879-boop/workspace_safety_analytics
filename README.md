# 🛡️ SafeWork Analytics

**AI-Powered Workplace Safety Analytics Dashboard**

> Built by **Anjali Kumari** · Electrical and Electronics Engineering · Bakhtiyarpur College of Engineering

---

## 📌 Project Overview

SafeWork Analytics is a Python-based interactive dashboard that analyses **fictional** workplace safety reports to surface trends, highlight unresolved issues, and generate preventive recommendations — helping organisations improve women's safety and workplace wellbeing.

> ⚠️ **Disclaimer:** All data in this project is completely fictional. No real individuals, organisations, or incidents are represented. This tool does not predict danger, prove misconduct, or guarantee safety. All suggestions are general best-practice guidance only.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 KPI Cards | Total reports, unresolved count, high-severity count, resolution rate |
| 📈 Interactive Charts | Category bar chart, monthly trend line, severity pie, resolution donut |
| 🔍 Smart Filters | Filter by month, category, severity, and resolution status |
| 💡 Preventive Suggestions | Auto-generated tips based on observed data patterns |
| 📋 Data Table | View all filtered records in an interactive table |
| ⬇️ Download Options | Export filtered data as CSV and a summary report as TXT |
| 🤖 AI Keyword Classifier | Suggests issue category from a typed description — no API key needed |

---

## 🗂️ Project Structure

```
SafeWork_Analytics/
│
├── data/
│   └── safety_reports.csv     ← 20 fictional safety report records
│
├── app.py                     ← Main Streamlit dashboard
├── requirements.txt           ← Python package list
├── README.md                  ← This file
└── .gitignore                 ← Files excluded from Git
```

---

## 🛠️ Technology Stack

- **Python 3.8+**
- **Pandas** – data loading and manipulation
- **Streamlit** – interactive web dashboard
- **Plotly** – interactive charts

---

## 🚀 How to Run Locally (Windows)

### Step 1 – Download or clone the project

If you have Git installed:
```powershell
git clone https://github.com/YOUR_USERNAME/SafeWork_Analytics.git
cd SafeWork_Analytics
```

Or download the ZIP from GitHub and extract it to your Desktop.

### Step 2 – Create and activate a virtual environment

Open PowerShell in the project folder and run:
```powershell
py -m venv venv
venv\Scripts\activate
```

### Step 3 – Install required packages

```powershell
pip install -r requirements.txt
```

### Step 4 – Run the dashboard

```powershell
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 📤 How to Upload to GitHub

1. Create a free account at [github.com](https://github.com)
2. Click **New Repository** → name it `SafeWork_Analytics` → click **Create**
3. In PowerShell (inside the project folder, with venv active):

```powershell
git init
git add .
git commit -m "Initial commit – SafeWork Analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/SafeWork_Analytics.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 📋 Dataset Fields

| Column | Description | Example |
|---|---|---|
| `report_id` | Unique report identifier | RPT-001 |
| `month` | Month of the report | January |
| `issue_category` | Type of safety concern | Inadequate Lighting |
| `workplace_area` | Location of the incident | Parking Lot |
| `severity` | Severity level (Low/Medium/High) | High |
| `resolution_status` | Whether it was resolved | Unresolved |
| `description` | Brief fictional description | The parking area... |

---

## 🔒 Privacy & Ethics

- All 20 records are **entirely fictional**
- No real names, phone numbers, or identifiable details are stored
- The app does not collect or transmit any user data
- The optional AI feature runs entirely on your local machine

---

## 📄 Licence

This project is for educational purposes only.
