# Task Manager

A simple task management project built with **Django**. This project allows users to create tasks, sub-tasks, and categorize them. All data can be managed via the Django admin panel or loaded from a JSON fixture.

## Features

* Create **Tasks** with title, description, status, categories, and deadlines.
* Create **SubTasks** linked to parent tasks.
* Categorize tasks with **Category** model (many-to-many relation).
* Admin panel support for easy management.
* Load initial data from a **JSON fixture**.
* Follows **PEP8** coding standards and includes English comments.

## Models

### Task

* title (unique per date)
* description
* categories (many-to-many)
* status: New, In progress, Pending, Blocked, Done
* deadline
* created_at

### SubTask

* title
* description
* task (foreign key to Task)
* status
* deadline
* created_at

### Category

* name (unique)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mierkulova-tech/Task-Manager.git
cd Task-Manager
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Load initial data (optional):

```bash
python manage.py loaddata tasks_fixture.json
```

7. Run the server:

```bash
python manage.py runserver
```

Access the admin panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## Screenshots

*(Add screenshots showing Tasks, SubTasks, and Categories in the admin panel here)*

## License

This project is for educational purposes.
