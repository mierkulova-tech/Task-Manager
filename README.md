# 📋 Task Manager — Educational Django Project

A clean, responsive task management and learning journal built with **Django**.  
This project combines **backend logic** (tasks, subtasks, categories) with a **modern frontend UI**, serving as a portfolio piece for backend development and full-stack learning.

> ✨ Live features:  
> - Task & subtask management  
> - Learning journal (blog-style posts)  
> - Styled UI with consistent layout  
> - Fully responsive design  

---

## 🌟 Features

### 📌 Task Management
- Create **Tasks** with title, description, status, categories, and deadlines  
- Add **Subtasks** linked to parent tasks  
- Organize tasks using **Categories** (many-to-many relation)  
- Manage all data via **Django Admin**

### 📝 Learning Journal
- Write and view **educational posts** (notes, reflections, code snippets)  
- Clean, readable layout with proper typography

### 🎨 Frontend
- Modern, responsive design with **flexbox layout**  
- Consistent styling across all pages (`/`, `/tasks/`, `/posts/`, `/about/`)  
- Sticky footer that **never jumps**  
- GitHub & LinkedIn links on the About page  
- Light, accessible color scheme

### 🛠️ Developer Experience
- Follows **PEP8** coding standards  
- English comments and clean structure  
- Load initial data via JSON fixture (optional)  
- Ready for deployment

---

## 📦 Models

### `Task`
- `title` (unique per deadline)
- `description`
- `categories` (many-to-many with `Category`)
- `status`: `New`, `In progress`, `Pending`, `Blocked`, `Done`
- `deadline`
- `created_at`

### `SubTask`
- `title`
- `description`
- `task` (foreign key to `Task`)
- `status`
- `deadline`
- `created_at`

### `Category`
- `name` (unique)

### `Post` (for learning journal)
- `title`
- `slug` (for clean URLs)
- `body`
- `date`

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mierkulova-tech/Task-Manager.git
   cd Task-Manager

2. **Create and activate virtual environment**
bash
1 python -m venv .venv
2 # Windows:
3 .\.venv\Scripts\activate
4 # macOS / Linux:
5 source .venv/bin/activate

**Install dependencies**
bash
1 pip install -r requirements.txt

**Apply migrations**
bash
1 python manage.py migrate

**Create superuser (optional but recommended)**
bash
1 python manage.py createsuperuser

**Load sample data (optional)**
bash
1 python manage.py loaddata tasks_fixture.json

**Run the server**
bash
1 python manage.py runserver

**Explore**
Visit: http://127.0.0.1:8000
Admin panel: http://127.0.0.1:8000/admin

💻 ***Screenshots***
(Consider adding 2–3 screenshots later: homepage, task list, post detail, about page)
Example caption:
"Clean UI with consistent layout and responsive design" 

📚 ***Purpose***
**This project is part of my backend development and full-stack learning journey, demonstrating:**

Django models, views, and templates
REST-like URL design
Semantic HTML & modern CSS (no frameworks)
Professional GitHub presentation

📄 **License**
This project is for educational purposes only.
Feel free to use the code as a reference or learning resource.
