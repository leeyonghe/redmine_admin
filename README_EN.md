# Redmine Admin

[한국어](README.md) | [English]

Redmine Admin is a Django-based web application for analyzing and managing data from the Redmine project management system. It visualizes data such as projects, issues, time entries, and provides performance analytics.

## 🚀 Key Features

### 📊 Dashboard
- Overall project and issue statistics
- Recent activity history
- Project-specific issue status

### 📈 Performance Analytics
- Individual work hours and issue processing status
- Project-specific performance statistics
- Average performance indicators

### 📋 Reporting System
- **Weekly Report**: Current week's issues and work status
- **Monthly Report**: Monthly performance and comparison with previous month
- **Yearly Report**: Comprehensive annual performance analysis

### 👥 User Management
- Redmine user information management
- Login and authentication system

## 🛠 Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL 8.0
- **Frontend**: HTML, CSS, JavaScript
- **Container**: Docker & Docker Compose
- **Environment**: django-environ

## 📦 Installation and Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd redmine_admin
```

### 2. Running with Docker (Recommended)

#### Run with Docker Compose
```bash
# Build and run containers
docker-compose up --build

# Run in background
docker-compose up -d
```

#### Run Individual Services
```bash
# Run MySQL database only
docker-compose up redmine_mysql

# Run Django application only
docker-compose up web
```

### 3. Running in Local Environment

#### Prerequisites
- Python 3.8+
- MySQL 8.0
- pip

#### Installation Steps
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file to configure database settings

# Database migration
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

## 🌐 Access Information

- **Web Application**: http://localhost:8000
- **MySQL Database**: localhost:3310
  - Database: redmine
  - User: root
  - Password: aqwsde123!

## 📁 Project Structure

```
redmine_admin/
├── redmine/                 # Main Django app
│   ├── models.py           # Data models (Project, Issue, TimeEntry, etc.)
│   ├── views.py            # View logic (dashboard, reports, etc.)
│   ├── urls.py             # URL routing
│   └── admin.py            # Django admin configuration
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── dashboard.html     # Dashboard page
│   ├── login.html         # Login page
│   └── *_report.html      # Report pages
├── static/                 # Static files (CSS, JS)
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image configuration
└── requirements.txt       # Python dependencies
```

## 📊 Data Models

### Main Models
- **Project**: Project information
- **Issue**: Issues and work items
- **TimeEntry**: Time records
- **RedmineUser**: User information
- **IssueStatus**: Issue status
- **Tracker**: Issue tracker

### Issue Status
- New (1)
- In Progress (2)
- Resolved (3)
- Feedback (4)
- Closed (5)
- Rejected (6)

### Priority
- Low (1)
- Normal (2)
- High (3)
- Urgent (4)
- Immediate (5)

## 🔧 Environment Variables

Set the following environment variables in the `.env` file:

```env
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=mysql://root:password@localhost:3310/redmine
```

## 📈 Usage

### 1. Access Dashboard
- Navigate to http://localhost:8000
- Check overall project status and recent activities

### 2. Performance Analytics
- Visit `/performance/` page to view individual and project-specific performance
- Provides work hours, processed issues count, and average performance indicators

### 3. View Reports
- **Weekly Report**: `/weekly-report/`
- **Monthly Report**: `/monthly-report/`
- **Yearly Report**: `/yearly-report/`

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check MySQL container status
   docker-compose ps
   
   # Check logs
   docker-compose logs redmine_mysql
   ```

2. **Django Migration Error**
   ```bash
   # Run migration inside container
   docker-compose exec web python manage.py migrate
   ```

3. **Static Files Issue**
   ```bash
   # Recollect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is distributed under the MIT License.

## 📞 Support

If you encounter any issues or have questions, please create an issue.

---

**Redmine Admin** - A tool for efficient project management and performance analysis