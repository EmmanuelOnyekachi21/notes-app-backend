# 📝 Notes App Backend (Django + DRF)

This is the **backend API** for the Notes App, built with **Django** and **Django REST Framework (DRF)**.  
It provides CRUD endpoints for managing notes, with authentication and future support for AI-powered features.

---

## 🚀 Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite (development), PostgreSQL (production)
- **Auth:** Django authentication / JWT (future)
- **Future AI Features:** Text summarization, keyword extraction, semantic search

---

## 🛠️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/notes-app-backend.git
cd notes-app-backend
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver
```

## Linting Script

This project includes a helper script `check_style.sh` which scans Python files for style issues using `pycodestyle`.

### How it works
- The script searches the provided directory for `.py` files.
- Each file is checked with `pycodestyle`.
- If errors are found, the file is opened in VS Code for correction.
- You can choose to skip files interactively.

### Error log file
During the process, linter errors are written to a temporary file:

- **Default name**: `/tmp/pycodestyle_errors.txt`
- The file is automatically deleted when the script exits.
- If the script is interrupted, the file can be safely removed manually:
  ```bash
  rm -f py_errors.txt
  ```

