# job_application_tracker
Repository for a cli app to track the job applications I am submitting.

# Job Application Tracker

A simple command-line application to track and manage job applications using a local SQLite database.

---

## 🚀 Features

- Add new job applications  
- List all entries  
- Search using multiple filters (id, company, job title, status)  
- Update existing entries  
- Delete entries  
- Reset the database  
- Input cleaning and validation  

---

## 🛠️ Tech Stack

- Python  
- Typer (CLI framework)  
- SQLAlchemy (ORM)  
- SQLite (database)  

---

## 📦 Installation

1. Clone the repository:

```
git clone https://github.com/your-username/job_application_tracker.git
cd job_application_tracker
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the CLI:

```
python -m src.cli
```

---

## 📌 Commands

### Add a new entry

```
japp add "DELL" "Software Engineer"
```

### List all entries

```
japp list
```

### Search entries

```
japp search-by --company "DELL"
japp search-by --id 1
japp search-by --company "DELL" --job-title "Engineer"
```

### Update an entry

```
japp update 1 --company "AMAZON"
```

### Delete an entry

```
japp delete 1
```

### Reset database

```
japp reset
```

---

## 🧪 Testing

Tests are written using `pytest`.

Run tests with:

```
pytest
```

---

## 📁 Project Structure

```
src/
├── api.py           # Business logic (EntryDB)
├── cli.py           # CLI commands
├── cli_utils.py     # CLI helpers
├── data_utils.py    # Data cleaning utilities
├── db.py            # Database configuration
├── models.py        # ORM models
├── exceptions.py    # Custom exceptions
```

---

## 🧠 Design Overview

The application is structured in layers:

- **CLI layer** → Handles user input/output  
- **API layer** → Business logic and validation  
- **Data utilities** → Input cleaning and normalization  
- **Database layer** → Persistence via SQLAlchemy  

---

## 📌 Future Improvements

- Add full test coverage  
- Improve validation and typing  
- Add application status workflows  
- Export data (CSV/JSON)  
- Package as an installable CLI tool  

---

## 📄 License

This project is for learning and personal use.