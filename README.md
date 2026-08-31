# Task Dependency Management System

A Django and Django REST Framework backend for managing tasks and their dependencies. The system validates dependency relationships, prevents circular dependencies, updates task states based on dependency completion, and exposes REST APIs alongside a lightweight dependency graph view.

## Project Summary

The project focuses on backend correctness and data integrity. Tasks are represented as a directed dependency graph, while model-level validation prevents invalid relationships such as self-dependencies and multi-level cycles.

## Main Features

- Create, update, and delete tasks
- Task states: `pending`, `in_progress`, `completed`, and `blocked`
- Multiple dependencies per task
- Dependency management through Django Admin and REST APIs
- Automatic status updates using Django signals
- Circular-dependency prevention using depth-first search (DFS)
- Lightweight dependency graph visualization
- JSON REST API responses

## Automatic Status Logic

- When all dependencies are completed, a dependent task can move to `in_progress`.
- When one or more dependencies are incomplete, the dependent task remains `pending`.

## Circular Dependency Prevention

The model validation checks for:

- Self-dependencies such as `A → A`
- Multi-level cycles such as `A → B → C → A`

DFS is used to detect whether adding a dependency would create a cycle. The validation applies to the model layer, so it protects both the admin interface and API workflows.

## REST API

### Tasks

```text
/api/tasks/
```

### Dependencies

```text
/api/dependencies/
```

Both endpoints are intended for local development and return JSON responses.

## Technology Stack

- Python 3.11
- Django 5.x
- Django REST Framework
- SQLite

## Project Structure

```text
.
├── manage.py
├── db.sqlite3
├── README.md
├── myapp/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── signals.py
│   ├── admin.py
│   ├── templates/
│   │   ├── task_list.html
│   │   └── graph.html
│   └── migrations/
└── taskmanager/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd task-dependency-management-system
```

### 2. Install dependencies

```bash
pip install django djangorestframework
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the development server

```bash
python manage.py runserver
```

### 5. Open the application

Use the local server address and the API routes documented above. The graph view is available at `/graph/` when enabled by the project's URL configuration.

## Key Learning Outcomes

- Django model design
- REST API development
- Graph-based dependency management
- DFS cycle detection
- Model-level validation
- Signals and state-management logic
- Backend data integrity
