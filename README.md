# Job Application Tracker

A command-line tool for tracking and managing job applications, backed by a local SQLite database. Built with a clean layered architecture: CLI → API → Data Utilities → Database.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.14 |
| CLI | [Typer](https://typer.tiangolo.com/) |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (local file) |
| Display | Tabulate |
| Linting | Ruff + Black |
| Testing | pytest |

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd job_application_tracker
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

All commands are run via:

```bash
python -m src.cli [COMMAND] [OPTIONS]
```

---

## Commands

### Add a new entry

```bash
python -m src.cli add "Google" "Software Engineer"
```

### List all entries

```bash
python -m src.cli list
```

### Search entries

Filter by any combination of fields:

```bash
python -m src.cli search-by --company "Google"
python -m src.cli search-by --id 1
python -m src.cli search-by --job-title "Engineer"
python -m src.cli search-by --status "Pending start"
python -m src.cli search-by --company "Google" --job-title "Engineer"
```

### Update an entry

Pass one or more fields to update by entry ID:

```bash
python -m src.cli update 1 --company "Amazon"
python -m src.cli update 1 --job-title "Senior Engineer" --status "Applied"
```

### Delete an entry

```bash
python -m src.cli delete 1
```

### Reset the database

Deletes all entries (prompts for confirmation):

```bash
python -m src.cli reset
```

---

## Data Model

Each job application entry stores:

| Field | Type | Required | Default |
|-------|------|----------|---------|
| `id` | Integer (auto) | — | — |
| `company` | String (max 30) | Yes | — |
| `job_title` | String (max 30) | Yes | — |
| `status` | String (max 30) | No | `"Pending start"` |

---

## Testing

Tests use `pytest` with CRUD markers for categorization.

```bash
# Run all tests
pytest

# Run by category
pytest -m create
pytest -m read
pytest -m update
pytest -m delete
```

Available markers (defined in `pytest.ini`): `create`, `read`, `update`, `delete`.

---

## License

This project is for learning and personal use.
