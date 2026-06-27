# Creative Spark – AI Startup Incubation Platform

A full-stack Django web application for startup incubation with AI-powered evaluation, market analysis, mentorship, and reporting.

## Features

- **Authentication**: Registration, Login, Logout, Password Reset, User Roles (Student, Mentor, Admin)
- **Home Page**: Hero section, animated cards, features, statistics, testimonials, contact form
- **Dashboard**: Personalized welcome, charts, stats, activity tracking
- **Startup Ideas**: Submit, edit, view startup ideas with full details
- **AI Evaluation**: Automatic scoring on innovation, feasibility, market potential, scalability, risk analysis, SWOT
- **Market Analysis**: Industry trends, competitor overview, market size, charts
- **Mentor Module**: Profiles, booking, feedback system
- **Reports**: PDF and Excel report generation
- **Admin Panel**: Manage users, ideas, categories, analytics
- **Search & Filter**: Search by keyword, filter by category/status/rating
- **Dark/Light Mode**: Toggle theme support
- **Responsive Design**: Bootstrap 5 with glassmorphism UI

## Tech Stack

- **Backend**: Python, Django 5
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Charts**: Chart.js
- **Icons**: Bootstrap Icons
- **Reports**: ReportLab (PDF), OpenPyXL (Excel)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CreativeSpark
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Load sample data:
```bash
python manage.py load_sample_data
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
CreativeSpark/
├── CreativeSpark/        # Project settings
├── apps/
│   ├── core/            # Home, About, Contact, FAQ
│   ├── authentication/  # Auth, profiles, roles
│   ├── dashboard/       # User dashboards
│   ├── ideas/           # Startup idea management
│   ├── evaluation/      # AI evaluation engine
│   ├── market/          # Market analysis
│   ├── mentors/         # Mentor profiles & booking
│   └── reports/         # PDF/Excel report generation
├── templates/           # HTML templates
├── static/              # CSS, JS, images
└── media/               # User uploads
```

## User Roles

- **Student**: Submit startup ideas, view evaluations, book mentors
- **Mentor**: Provide feedback, manage sessions
- **Admin**: Full system access, manage users and ideas
