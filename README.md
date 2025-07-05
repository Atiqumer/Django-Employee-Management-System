# 🧑‍💼 Django Employee Management System

A full-featured web-based Employee & Project Management System built using **Django**. This system allows admins and employees to manage employee data, projects, salary slips, leaves, and dashboards with role-based access control.

🔗 **Live Demo**: Coming Soon  
📂 **Repository**: [GitHub - Atiqumer/Django-Employee-Management-System](https://github.com/Atiqumer/Django-Employee-Management-System)

---

## 🚀 Key Features

### 🧑‍💼 Employee Management
- Add, update, delete employees
- View personal and role-based employee profiles

### 📂 Project Management
- Assign projects to employees
- Track project details and assigned members

### 💵 Salary Management
- Generate and download salary slips (PDF)
- Auto-generate salary periods based on join dates

### 📊 Admin Dashboard
- View employee and project statistics
- Track project assignments and monthly overviews

### 🔐 Authentication & Permissions
- Admin vs Normal User roles:
  - **Admins** manage all data
  - **Normal Users** can only view/manage their own profile, salary, and projects

### ✉️ Email & PDF Integration
- PDF generation using ReportLab
- Email configuration (SMTP)

---

## 🛠 Tech Stack

| Component     | Technology                     |
|---------------|--------------------------------|
| Backend       | Django 4.x                     |
| Frontend      | HTML5, Bootstrap (or Tailwind) |
| PDF Engine    | ReportLab                      |
| Database      | SQLite (default), easily switchable to PostgreSQL |
| Email         | SMTP (configured for production) |
| Deployment    | Render.com or Hostinger        |

---

## 📁 Project Structure

django-employee-management/
├── core/ # Main app logic (views, models, urls)
│ ├── templates/ # HTML templates
│ ├── static/ # Static files (CSS, JS, images)
│ ├── models.py # Database models
│ ├── views.py # Business logic
│ └── urls.py # Route definitions
├── employee_system/ # Project settings and WSGI config
├── db.sqlite3 # Default SQLite database
├── manage.py # Django CLI entry point
└── requirements.txt # Python dependencies


---

---

## ⚙️ Installation Guide

### 📥 Clone the Repository

```bash
git clone https://github.com/Atiqumer/Django-Employee-Management-System.git
cd Django-Employee-Management-System

📦 Set Up Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt