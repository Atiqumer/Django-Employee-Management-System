# Django Employee Management System

A scalable and secure web-based solution built with **Django**, **Bootstrap**, and **SQLite** for efficiently managing employees, projects, and salary slips. Designed to streamline HR operations with role-based access, intuitive dashboards, and modern UI.

---

## 🚀 Key Features

- 🔐 **User Authentication** (Login / Logout)
- 🎯 **Role-Based Access Control** (Admin & Normal User)
- 👥 **Employee Management** (Create, Read, Update, Delete)
- 📁 **Project Assignment** per Employee
- 💵 **Salary Slip Generation** with Export & Print support
- 📊 **Admin Dashboard** Overview
- 📅 **Monthly Salary Filtering**
- 🌐 **Responsive UI** with Bootstrap
- 🔒 **Environment Variable Handling** via `.env` file

---

## 👥 User Roles & Permissions

### 🔒 Admin
- Full control over all records
- Access to all employees, projects, and salary data
- Dashboard with real-time insights

### 👤 Normal User
- View personal profile
- Access assigned projects
- View individual salary records
- Submit leave requests

---

## 🛠️ Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Backend     | Django 5.x (Python 3) |
| Frontend    | HTML, Bootstrap 5   |
| Database    | SQLite (can be migrated to PostgreSQL/MySQL) |
| Authentication | Django's Built-in Auth |
| Email       | SMTP Support (Optional) |

---

## 📦 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Atiqumer/Django-Employee-Management-System.git
cd Django-Employee-Management-System
