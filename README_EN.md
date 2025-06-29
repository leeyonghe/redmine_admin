# Redmine Admin

[한국어](README.md) | [English]

Redmine Admin is a Django-based web application for analyzing and managing data from the Redmine project management system. It visualizes data such as projects, issues, time entries, and provides comprehensive performance analytics with advanced reporting capabilities.

## 🚀 Key Features

### 📊 Advanced Dashboard
- **Real-time Statistics**: Overall project and issue statistics with live updates
- **Activity Timeline**: Recent activity history with detailed tracking
- **Project Overview**: Project-specific issue status and progress visualization
- **Performance Metrics**: Key performance indicators (KPIs) at a glance

### 📈 Comprehensive Performance Analytics
- **Individual Performance**: Detailed work hours and issue processing status per user
- **Project Performance**: Project-specific performance statistics and trends
- **Team Analytics**: Team performance comparison and benchmarking
- **Advanced Metrics**: Average performance indicators with historical data

### 📋 Advanced Reporting System
- **Weekly Report**: Current week's issues and work status with trend analysis
- **Monthly Report**: Monthly performance and comparison with previous month
- **Yearly Report**: Comprehensive annual performance analysis with forecasting
- **Custom Date Ranges**: Flexible reporting with custom date selection
- **Export Capabilities**: Report export in multiple formats

### 👥 Enhanced User Management
- **Redmine Integration**: Seamless Redmine user information management
- **Secure Authentication**: Advanced login and authentication system
- **User Profiles**: Detailed user profiles with performance history
- **Avatar Support**: User avatar display and management

### 🔍 Advanced Search & Filtering
- **Smart Search**: Advanced search capabilities across all data
- **Dynamic Filtering**: Real-time filtering by status, priority, assignee
- **Date Range Filters**: Flexible date-based filtering options

## 🛠 Technology Stack

- **Backend**: Django 4.2.7 (LTS)
- **Database**: MySQL 8.0.42
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Container**: Docker 20.10+ & Docker Compose 2.0+
- **Environment**: django-environ 0.11.2
- **Image Processing**: Pillow 10.1.0
- **Database Driver**: mysqlclient 2.2.0

## 📦 Installation and Setup

### Prerequisites
- Docker 20.10+ and Docker Compose 2.0+
- Git
- 4GB+ RAM available
- 10GB+ disk space

### 1. Quick Start with Docker (Recommended)

#### Clone and Run
```bash
# Clone the repository
git clone <repository-url>
cd redmine_admin

# Start all services
docker-compose up --build -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f web
```

#### Service Management
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Update and rebuild
docker-compose up --build -d
```

### 2. Individual Service Management

#### Database Only
```bash
# Start MySQL database
docker-compose up redmine_mysql -d

# Access MySQL directly
docker-compose exec redmine_mysql mysql -u root -p
```

#### Application Only
```bash
# Start Django application
docker-compose up web -d

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

### 3. Development Environment Setup

#### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip
- virtualenv

#### Installation Steps
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your database settings

# Database setup
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver 0.0.0.0:8000
```

## 🌐 Access Information

- **Web Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin/
- **MySQL Database**: localhost:3310
  - Database: redmine
  - User: root
  - Password: aqwsde123!
  - Character Set: utf8

## 📁 Project Structure

```
redmine_admin/
├── redmine/                 # Main Django application
│   ├── models.py           # Data models (Project, Issue, TimeEntry, etc.)
│   ├── views.py            # View logic (dashboard, reports, analytics)
│   ├── urls.py             # URL routing configuration
│   ├── admin.py            # Django admin interface configuration
│   ├── backends.py         # Custom authentication backend
│   └── apps.py             # App configuration
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── dashboard.html     # Main dashboard page
│   ├── login.html         # Authentication page
│   ├── performance.html   # Performance analytics page
│   └── *_report.html      # Report templates
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Image assets
├── media/                  # User uploaded files
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## 📊 Data Models

### Core Models
- **Project**: Project information and metadata
- **Issue**: Issues and work items with full lifecycle tracking
- **TimeEntry**: Time tracking and work logging
- **RedmineUser**: User information and profiles
- **IssueStatus**: Issue status definitions
- **Tracker**: Issue tracking categories
- **RedmineUserAvatar**: User avatar management

### Issue Status Workflow
- **New (1)**: Initial issue state
- **In Progress (2)**: Active development
- **Resolved (3)**: Issue resolution completed
- **Feedback (4)**: Awaiting feedback/review
- **Closed (5)**: Issue fully completed
- **Rejected (6)**: Issue rejected/cancelled

### Priority Levels
- **Low (1)**: Low priority issues
- **Normal (2)**: Standard priority
- **High (3)**: High priority issues
- **Urgent (4)**: Urgent issues
- **Immediate (5)**: Critical issues

## 🔧 Environment Configuration

### Required Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=mysql://root:aqwsde123!@localhost:3310/redmine

# Optional Settings
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

### Docker Environment Variables
The following are automatically set in Docker:

```env
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=mysql://root:aqwsde123!@redmine_mysql:3306/redmine
```

## 📈 Usage Guide

### 1. Dashboard Overview
- Navigate to http://localhost:8000
- View real-time project statistics
- Monitor recent activities and trends
- Access quick navigation to all features

### 2. Performance Analytics
- Visit `/performance/` for detailed analytics
- View individual and team performance metrics
- Analyze project-specific statistics
- Track performance trends over time

### 3. Report Generation
- **Weekly Reports**: `/weekly-report/` or `/weekly-report/<year>/<week>/`
- **Monthly Reports**: `/monthly-report/` or `/monthly-report/<year>/<month>/`
- **Yearly Reports**: `/yearly-report/` or `/yearly-report/<year>/`

### 4. User Management
- Access user profiles and performance data
- View user avatars and contact information
- Track user activity and contributions

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Issues
```bash
# Check MySQL container status
docker-compose ps redmine_mysql

# View MySQL logs
docker-compose logs redmine_mysql

# Test database connection
docker-compose exec web python manage.py dbshell
```

#### 2. Django Migration Problems
```bash
# Reset migrations
docker-compose exec web python manage.py migrate --fake-initial

# Create new migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate
```

#### 3. Static Files Issues
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Check static files location
docker-compose exec web python manage.py findstatic admin/css/base.css
```

#### 4. Performance Issues
```bash
# Check container resources
docker stats

# View application logs
docker-compose logs -f web

# Restart services
docker-compose restart
```

### Performance Optimization
- Enable database query caching
- Optimize static file serving
- Use database connection pooling
- Implement proper indexing

## 🔒 Security Considerations

### Authentication
- Custom authentication backend for Redmine integration
- Session management with configurable expiry
- Password hashing and security

### Data Protection
- Database connection encryption
- Input validation and sanitization
- SQL injection prevention
- XSS protection

### Access Control
- Role-based access control
- User permission management
- Audit logging capabilities

## 🚀 Deployment

### Production Deployment
```bash
# Set production environment
export DJANGO_SETTINGS_MODULE=redmine_admin.settings.production

# Build production image
docker build -t redmine-admin:production .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

### Scaling Considerations
- Database replication for high availability
- Load balancing for multiple application instances
- Caching layer implementation
- Monitoring and logging setup

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Project**
2. **Create Feature Branch**: `git checkout -b feature/AmazingFeature`
3. **Commit Changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to Branch**: `git push origin feature/AmazingFeature`
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 coding standards
- Write comprehensive tests
- Update documentation
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support and Community

### Getting Help
- **Documentation**: Check this README and inline code comments
- **Issues**: Create an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

### Version History
- **v2.0.0**: Enhanced performance analytics and reporting
- **v1.5.0**: Added user avatar support and improved UI
- **v1.0.0**: Initial release with basic dashboard and reports

## 🔮 Roadmap

### Upcoming Features
- [ ] Real-time notifications
- [ ] Advanced charting and visualization
- [ ] API endpoints for external integrations
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Advanced export options (PDF, Excel)

### Planned Improvements
- [ ] Performance optimization
- [ ] Enhanced security features
- [ ] Better error handling
- [ ] Comprehensive testing suite

---

**Redmine Admin v2.0.0** - Advanced project management and performance analysis tool

*Built with ❤️ using Django and modern web technologies*