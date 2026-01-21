# Task Dependency Management System

## 📌 Project Description
This project is a **Task Dependency Management System** developed using **Django** and **Django REST Framework**.

The system allows tasks to depend on other tasks, automatically updates task statuses based on dependency completion, prevents circular dependencies, and provides both REST APIs and a simple visual graph for dependencies.

This project focuses on **backend logic correctness**, **data integrity**, and **clean architecture**, with a lightweight UI for visualization.

---

## 🚀 Features Implemented

### ✅ Task Management
- Create, update, delete tasks
- Supported statuses:
  - `pending`
  - `in_progress`
  - `completed`
  - `blocked`

---

### ✅ Dependency Management
- Tasks can depend on multiple other tasks
- Dependencies stored as a **directed graph**
- Dependencies manageable via:
  - Django Admin
  - REST APIs

---

# Automatic Status Update
- If **all dependencies are completed** → task becomes `in_progress`
- If **any dependency is incomplete** → task remains `pending`
- Implemented using **Django signals**

---

# Circular Dependency Prevention
- Prevents:
  - Self-dependency (Task → same Task)
  - Multi-level cycles (A → B → C → A)
- Implemented using **Depth-First Search (DFS)**
- Validation enforced at **model level**
- Works in:
  - Admin UI
  - REST APIs

---

 # Graph Visualization (UI)
- Visual display of task dependencies
- Status-based color coding
- Lightweight HTML-based graph (no external libraries)

 Graph Page (Local):
 (http://127.0.0.1:8000/graph/)
 
---

## 🌐 REST API Endpoints

### 🔹 Tasks API
- List & create tasks
http://127.0.0.1:8000/api/tasks/

### 🔹 Dependencies API
- List & create task dependencies
http://127.0.0.1:8000/api/dependencies/


All APIs return **JSON responses** and enforce validation rules.

---

## 🛠 Technology Stack
- Python 3.11
- Django 5.x
- Django REST Framework
- SQLite (default database)

---

## 📁 Project Structure

taskmanager/
│
├── manage.py
├── db.sqlite3
├── README.md
│
├── myapp/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── signals.py
│ ├── admin.py
│ ├── templates/
│ │ ├── task_list.html
│ │ └── graph.html
│ └── migrations/
│
└── taskmanager/
├── settings.py
├── urls.py
└── wsgi.py


---

## ⚙️ How to Run the Project (Step-by-Step)

### 1️⃣ Clone the repository
```bash
git clone <PASTE_GITHUB_REPO_LINK_HERE>
cd taskmanager

2️⃣ Install dependencies
pip install django djangorestframework

3️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

4️⃣ Start the server
python manage.py runserver

🔗 Access URLs (Local Development)

⚠️ These URLs work after running the server locally




Dependencies API

http://127.0.0.1:8000/api/dependencies/

