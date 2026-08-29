# 🎓 SchoBase — Comprehensive School Management System

[![Django](https://img.shields.io/badge/Django-5.x%20%2F%206.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-3.17.x-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Python](https://img.shields.io/badge/Python-3.11%20%2F%203.12%20%2F%203.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon%20DB-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**SchoBase** is a scalable, modular, full-featured web-based School Management System built on Django. It streamlines multi-stakeholder school administration, teacher-student workflows, daily attendance tracking, digital homework assignment and submissions, automated student credential provisioning, and in-app notifications with a modern dark-themed responsive UI and RESTful APIs for mobile/client integrations.

---

## 📑 Table of Contents

- [Overview & Architecture](#-overview--architecture)
- [Key Features by User Role](#-key-features-by-user-role)
- [Tech Stack & Dependencies](#-tech-stack--dependencies)
- [Project Directory Structure](#-project-directory-structure)
- [Database Models & Entity Relationships](#-database-models--entity-relationships)
- [Getting Started & Local Setup](#-getting-started--local-setup)
- [Environment Variables](#-environment-variables)
- [Database Migrations & Reset Scripts](#-database-migrations--reset-scripts)
- [API Reference (REST Endpoints)](#-api-reference-rest-endpoints)
- [Authentication & Role Decorators](#-authentication--role-decorators)
- [Developer Guide: Extending SchoBase](#-developer-guide-extending-schobase)
- [Deployment Guide (Render / Railway / Heroku / Neon)](#-deployment-guide)
- [Contributing & Code Style](#-contributing--code-style)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## 🏛 Overview & Architecture

SchoBase follows the classic Django **MVT (Model-View-Template)** architecture combined with **Django REST Framework (DRF)** for headless/API capabilities.

```
                    ┌──────────────────────────────────────────────┐
                    │             Client / Browser / API           │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │                 hello/urls.py                │
                    └──────┬───────────────┬────────────────┬──────┘
                           │               │                │
             ┌─────────────▼────┐  ┌───────▼────────┐  ┌────▼─────────────┐
             │  Web Views (MVT) │  │  DRF API Views │  │  Django Admin    │
             │ (Bootstrap Dark) │  │   (/api/...)   │  │   (/admin/...)   │
             └─────────────┬────┘  └───────┬────────┘  └────┬─────────────┘
                           │               │                │
                           └───────────────┼────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │          Django Apps & ORM Layer             │
                    │  (accounts, school, teacher, student, etc.)  │
                    └──────────────────────┬───────────────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
             [ Development SQLite ]                 [ Production PostgreSQL ]
                  (db.sqlite3)                         (Neon Serverless)
```

---

## 🌟 Key Features by User Role

### 👑 1. School Administrator (`school_admin`)
- **Institution Overview**: Real-time KPI cards for total enrolled students, faculty members, and active classes.
- **Academic Hierarchy Management**: Create and configure Classes, Sections, and Subjects.
- **Teacher & Student Management**: View full teacher directories and student rosters with multi-criteria filtering.
- **Access Control**: Supervise active teacher records linked to the specific institution.

### 👩‍🏫 2. Teacher (`teacher`)
- **Classroom Management**: Manage assigned sections and view class students.
- **Student Enrollment**: Create and update student records. Automatically creates user credentials and sends an onboarding notification.
- **Daily Attendance**: Mark daily attendance with rapid single-click toggles (`Present`, `Absent`, `Leave`, `Pending`). Attendance enforces a single record per student per day constraint.
- **Attendance History**: Inspect daily attendance statuses grouped by class.
- **Digital Homework**: Create assignments with attachments (`PDF/Doc/Images`), deadlines, and section-specific targeting.
- **Teacher Profile**: View personal profile, assigned classes, and contact details.

### 🎓 3. Student (`student`)
- **Student Portal**: Dedicated student dashboard and rich profile overview (admission number, roll number, class, section, date of birth, contact info).
- **Homework Feed**: View active and upcoming assignments assigned to their section, download files, and check deadlines.
- **Attendance Tracking**: View attendance records and status.
- **Notifications**: In-app notification center with mark-as-read and clear-all actions.

### ⚙️ 4. Super Administrator
- Full access to the Django Admin panel (`/admin/`) to manage all database tables, global platform settings, multi-school data, and custom user models.

---

## 🛠 Tech Stack & Dependencies

| Category | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Django 5.x / 6.x | Core web framework, ORM, authentication, and routing |
| **REST APIs** | Django REST Framework 3.17.x | RESTful API endpoints and serializers |
| **Database** | PostgreSQL (Neon) / SQLite | Relational database (PostgreSQL for prod, SQLite for dev) |
| **Database Adapter** | `psycopg2-binary`, `dj-database-url` | PostgreSQL database driver and 12-factor database URL parser |
| **Frontend Styling** | Bootstrap 5.3 (Dark Theme) | Responsive CSS framework, RTL support, modern UI |
| **Icons** | Font Awesome 7 | Comprehensive UI icons |
| **Static Files** | WhiteNoise 6.12.x | High-performance static files serving for production |
| **Image Processing** | Pillow 12.3.x | Processing and handling profile pictures & uploads |
| **WSGI Server** | Gunicorn 26.0.x | Production HTTP WSGI server |
| **Live Reloading** | `django-browser-reload` | Fast DX with automatic browser reload during frontend changes |
| **CORS Support** | `django-cors-headers` | Cross-Origin Resource Sharing for decoupled frontends/APIs |

---

## 📂 Project Directory Structure

```text
SchoBase Django web App/
├── .venv/                         # Python virtual environment
├── .gitignore                     # Git ignore rules (env, sqlite, media, pycache)
├── README.md                      # Project documentation (this file)
└── hello/                         # Main Django workspace root
    ├── manage.py                  # Django CLI entrypoint
    ├── requirements.txt           # Python package dependencies
    ├── Procfile                   # Process configuration for Heroku/Render/Railway
    ├── build.sh                   # Deployment build and superuser seed script
    ├── migrations_script.py       # Helper script to clean migrations and reset local DB
    ├── db.sqlite3                 # Local SQLite database (dev)
    │
    ├── hello/                     # Project configuration package
    │   ├── __init__.py
    │   ├── asgi.py                # ASGI configuration
    │   ├── settings.py            # Main Django settings (Apps, DB, Middleware, Auth)
    │   ├── urls.py                # Root URL dispatcher
    │   ├── views.py               # Root error views (custom 403, 404, CSRF handlers)
    │   └── wsgi.py                # WSGI entrypoint for Gunicorn
    │
    ├── accounts/                  # User authentication & role management
    │   ├── models.py              # CustomUser (extending AbstractUser with role choices)
    │   ├── views.py               # Custom login, logout, authentication views
    │   ├── forms.py               # Authentication forms
    │   ├── decorators.py          # @teacher_required, @teacher_or_admin_required, etc.
    │   ├── context_processors.py  # nav_items (role-based dynamic navbar items)
    │   └── urls.py                # /acc/login/, /acc/logout/
    │
    ├── school/                    # School entity and institutional information
    │   ├── models.py              # School model (name, board, contact, email, address)
    │   └── admin.py
    │
    ├── school_admin/              # School Administrator entity
    │   ├── models.py              # Adminstrators model (linked to CustomUser & School)
    │   └── admin.py
    │
    ├── teacher/                   # Faculty management
    │   ├── models.py              # Teacher model (user, school, class_teacher_of M2M)
    │   ├── views.py               # teacher_profile, list_teachers
    │   ├── forms.py               # Teacher profile and editing forms
    │   └── urls.py                # /teacher/, /teacher/list_teachers/
    │
    ├── student/                   # Student management & enrollment
    │   ├── models.py              # Student model + post_delete cascade signal
    │   ├── views.py               # CRUD views: create, list, update, delete student
    │   ├── forms.py               # StudentForm with dynamic section filtering
    │   └── urls.py                # /student/create_student/, /student/list_students/, etc.
    │
    ├── classes/                   # Grade / Class levels
    │   ├── models.py              # Class model (name, school FK)
    │   └── admin.py
    │
    ├── section/                   # Class sections
    │   ├── models.py              # Section model (name, class_name FK, class_teacher FK)
    │   └── admin.py
    │
    ├── subject/                   # Academic subjects
    │   ├── models.py              # Subject model (name, section FK)
    │   └── admin.py
    │
    ├── attendence/                # Student daily attendance system
    │   ├── models.py              # Attendance model (status: Present/Absent/Leave/Pending)
    │   ├── views.py               # take_attendance, view_att (daily attendance views)
    │   └── urls.py                # /attendance/take_attendance/, /attendance/view/
    │
    ├── homework/                  # Assignments and homework management
    │   ├── models.py              # Homework model (body, subject, deadlines, files)
    │   ├── views.py               # ViewHomework, sendHomework
    │   ├── forms.py               # HomeworkForm with section-subject filtering
    │   └── urls.py                # /homework/, /homework/send/
    │
    ├── notification/              # In-app notifications
    │   ├── models.py              # Notification model (user, message, created_at)
    │   ├── views.py               # notification_list, mrk_as_read, delete_notification
    │   └── urls.py                # /notification/, /notification/mrk_as_read/<id>
    │
    ├── dashboard/                 # Role-based dashboard dispatching
    │   ├── views.py               # dashboard view (routes school_admin, teacher, student)
    │   └── urls.py                # / (root home dashboard)
    │
    ├── api/                       # Django REST Framework APIs
    │   ├── serializers.py         # ModelSerializers for all core models
    │   ├── views.py               # ModelViewSets for CRUD via API
    │   └── urls.py                # /api/students/, /api/teachers/, /api/schools/, etc.
    │
    ├── marks/                     # [Extension Ready] Marks and examination module
    │   ├── models.py
    │   └── views.py
    │
    ├── templates/                 # Global base templates and error pages
    │   ├── base.html              # Core layout, navbar, loader, footer
    │   ├── 403.html               # 403 Forbidden page
    │   ├── 404.html               # 404 Not Found page
    │   └── 500.html               # 500 Server Error page
    │
    ├── static/                    # Static assets (CSS, JS, images, logos)
    ├── staticfiles/               # Collected static files (for WhiteNoise)
    └── media/                     # User uploads (profile pictures, homework documents)
```

---

## 📊 Database Models & Entity Relationships

Below is the entity-relationship diagram representing the core models in SchoBase:

```mermaid
erDiagram
    CustomUser ||--o| Adminstrators : "has profile"
    CustomUser ||--o| Teacher : "has profile"
    CustomUser ||--o| Student : "has profile"
    CustomUser ||--o{ Notification : "receives"

    School ||--o{ Adminstrators : "employs"
    School ||--o{ Teacher : "employs"
    School ||--o{ Class : "offers"
    School ||--o{ Student : "enrolls"
    School ||--o{ Section : "contains"

    Class ||--o{ Section : "divided into"
    Class ||--o{ Student : "belongs to"
    Teacher }o--o{ Class : "class_teacher_of"
    Teacher ||--o{ Section : "manages as class teacher"

    Section ||--o{ Subject : "has"
    Section ||--o{ Student : "contains"
    Section ||--o{ Homework : "assigned to"

    Subject ||--o{ Homework : "categorized by"
    Teacher ||--o{ Homework : "assigns"

    Student ||--o{ Attendance : "has daily record"
    Teacher ||--o{ Attendance : "marks"
```

---

## 🚀 Getting Started & Local Setup

Follow these step-by-step instructions to get a local development environment running.

### 1. Prerequisites
- **Python 3.11+** installed on your system.
- **Git** installed.
- **pip** and **virtualenv**.

### 2. Clone the Repository
```bash
git clone https://github.com/Code-Keshav-1947/SchoBase.git
cd SchoBase
```

### 3. Create and Activate Virtual Environment
- **On Windows (PowerShell / Command Prompt):**
  ```powershell
  python -m venv .venv
  .venv\Scriptsctivate
  ```
- **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependencies
Navigate into the Django workspace directory (`hello/`) and install requirements:
```bash
cd hello
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
Create an initial administrative account to access the Django admin portal:
```bash
python manage.py createsuperuser
```
*(Or use the credentials seeded if using `build.sh`: Username `boss`, Password `BossPass123`)*

### 7. Run the Development Server
```bash
python manage.py runserver
```
Open your browser and navigate to:
- **Application Web UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Login Screen:** [http://127.0.0.1:8000/acc/login/](http://127.0.0.1:8000/acc/login/)
- **Admin Dashboard:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Browsable REST API:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## ⚙️ Environment Variables

SchoBase can be configured using environment variables for seamless deployment across local, staging, and production environments:

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | Optional | `None` (uses SQLite `db.sqlite3`) | PostgreSQL connection string (e.g. Neon connection URL with connection pooling: `postgresql://user:pass@ep-pooler.region.neon.tech/dbname?sslmode=require`) |
| `SECRET_KEY` | Production | Insecure dev key | Django secret key for cryptographic signing |
| `DEBUG` | Optional | `True` | Set `False` in production |
| `ALLOWED_HOSTS` | Optional | `*` | Comma-separated list of host/domain names |

---

## 🔄 Database Migrations & Reset Scripts

### Managing Migrations
When adding new fields or models:
```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```

### Clean Database Reset (Development Helper)
The project includes a utility script `migrations_script.py` located in `hello/`. It deletes `db.sqlite3` and all intermediate migration files while preserving `__init__.py` files:

```bash
cd hello
python migrations_script.py
python manage.py makemigrations accounts school school_admin teacher classes section subject student attendence homework notification marks dashboard api
python manage.py migrate
python manage.py createsuperuser
```

---

## 📡 API Reference (REST Endpoints)

SchoBase exposes full RESTful endpoints via Django REST Framework. All endpoints are prefixed with `/api/`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` / `POST` | `/api/students/` | List all students or create a new student |
| `GET` / `POST` | `/api/teachers/` | List all teachers or register a new teacher |
| `GET` / `POST` | `/api/schools/` | List schools or register a new school |
| `GET` / `POST` | `/api/classes/` | List classes or create a new class |
| `GET` / `POST` | `/api/sections/` | List sections or create a new section |
| `GET` / `POST` | `/api/attendances/` | List attendance records or record attendance |
| `GET` / `POST` | `/api/notifications/` | List notifications or push a notification |

> **Note**: For detail views, update, and delete actions, append the object ID (e.g. `/api/students/1/`).

---

## 🔐 Authentication & Role Decorators

SchoBase employs custom decorators in `accounts/decorators.py` and `student/views.py` to enforce role-based access control:

- `@login_required`: Restricts view to authenticated users.
- `@teacher_required`: Restricts view strictly to users with `role == 'teacher'`.
- `@teacher_or_admin_required`: Allows access to users with `role in ['teacher', 'school_admin']`.
- `@school_admin_required`: Restricts view strictly to school administrators.

### Role Switching Flow
When a user visits `/`, the `dashboard` view inspects `request.user.role`:
- If `role == 'school_admin'`, renders `dashboard/school_admin.html` with institution statistics.
- If `role == 'teacher'`, renders `dashboard/teacher_dashboard.html` with class management cards.
- If `role == 'student'`, renders `dashboard/student_dashboard.html` with student-centric items.
- If unauthenticated, redirects to `/acc/login/`.

---

## 💡 Developer Guide: Extending SchoBase

Here are the recommended workflows and best practices when continuing development on SchoBase:

### 1. Implementing the Marks & Examination Module (`marks/`)
The `marks` app is scaffolded. To implement examination results:
1. Define models in `hello/marks/models.py`:
   ```python
   class Exam(models.Model):
       school = models.ForeignKey('school.School', on_delete=models.CASCADE)
       name = models.CharField(max_length=100) # e.g. Mid-Term 2026
       start_date = models.DateField()
       end_date = models.DateField()

   class Mark(models.Model):
       student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
       subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE)
       exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
       marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
       max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
       remarks = models.CharField(max_length=200, blank=True)
   ```
2. Create forms and views in `marks/forms.py` and `marks/views.py`.
3. Add URLs in `marks/urls.py` and include them in `hello/urls.py`.
4. Add serializers in `api/serializers.py` and register viewsets in `api/views.py`.

### 2. Adding Fee Management
- Add a `FeeCategory` and `StudentFeeRecord` in a new `fees` app.
- Link payment statuses (`Paid`, `Pending`, `Overdue`) to the teacher and admin dashboard fee cards.

### 3. Adding Signal Handlers & Automations
- Notice the `post_delete` signal in `student/models.py` that automatically deletes the associated `CustomUser` when a student is deleted. Follow this pattern for `Teacher` and `Adminstrators` to maintain database hygiene.

### 4. Query Optimization Tips
- Always use `.select_related('school', 'class_name', 'section')` for single foreign keys.
- Use `.prefetch_related('class_teacher_of')` for ManyToMany relationships to prevent `N+1` query bottlenecks.

---

## 🚢 Deployment Guide

SchoBase is pre-configured for instant deployment to cloud platforms like **Render**, **Railway**, or **Heroku** with **Neon PostgreSQL**.

### 1. Build Script (`build.sh`)
The included `build.sh` script automatically:
1. Installs Python dependencies.
2. Collects static assets (`collectstatic --noinput`).
3. Runs database migrations (`makemigrations` and `migrate`).
4. Idempotently creates a default superuser if one doesn't exist.

### 2. Procfile
The `Procfile` runs database migrations and binds Gunicorn:
```text
web: python manage.py migrate && gunicorn hello.wsgi
```

### 3. Deploying to Render.com
1. Create a new **Web Service** and connect your GitHub repository.
2. Set **Environment** to `Python 3`.
3. Set **Build Command**: `./build.sh` (or `cd hello && ./build.sh`)
4. Set **Start Command**: `cd hello && gunicorn hello.wsgi:application`
5. Add Environment Variables:
   - `DATABASE_URL`: `postgresql://<user>:<password>@<host>/<database>?sslmode=require`
   - `PYTHON_VERSION`: `3.12.0`
   - `SECRET_KEY`: `<your-random-secure-secret-key>`
   - `DEBUG`: `False`

---

## 🤝 Contributing & Code Style

We welcome contributions! To maintain a clean and reliable codebase:

1. **Fork the Repository** and create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
2. **Follow PEP 8 Guidelines** for Python code formatting.
3. **Commit your changes with descriptive commit messages:**
   ```bash
   git commit -m 'feat: add exam report card generator'
   ```
4. **Push to the Branch:**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**.

---

## ❓ Troubleshooting & FAQs

<details>
<summary><b>1. ModuleNotFoundError: No module named 'dj_database_url' or other packages</b></summary>

Ensure your virtual environment is activated before running commands:

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Install requirements
pip install -r hello/requirements.txt
```

</details>

<details>
<summary><b>2. Static files or CSS not loading</b></summary>

Ensure you have run `collectstatic`:

```bash
python manage.py collectstatic --noinput
```

WhiteNoise is configured in `settings.py` and `MIDDLEWARE` to serve static assets automatically.
</details>

<details>
<summary><b>3. Images or Media uploads returning 404</b></summary>

In local development, `MEDIA_URL` is served through `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` in `hello/urls.py`. Ensure uploaded files exist in `hello/media/`.
</details>


---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details.

---

<div align="center">
  <sub>Built with ❤️ by the SchoBase Team & Contributors.</sub>
</div>
