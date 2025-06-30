# Redmine Admin

[한국어](README.md) | [English](README_EN.md) | [Japanese](README_JP.md) | [Chinese]

Redmine Admin是一个基于Django的Web应用程序，用于分析和管理Redmine项目管理系统中的数据。它可视化项目、问题、工时记录等数据，并提供具有高级报告功能的全面性能分析。

## 🚀 主要功能

### 📊 高级仪表板
- **实时统计**: 整体项目和问题统计，支持实时更新
- **活动时间线**: 具有详细跟踪的最近活动历史
- **项目概览**: 项目特定问题状态和进度可视化
- **性能指标**: 一目了然的关键性能指标（KPI）

### 📈 全面性能分析
- **个人性能**: 每个用户的详细工作时间和问题处理状态
- **项目性能**: 项目特定的性能统计和趋势
- **团队分析**: 团队性能比较和基准测试
- **高级指标**: 包含历史数据的平均性能指标

### 📋 高级报告系统
- **周报**: 本周问题和工作状态的趋势分析
- **月报**: 月度性能与上月的比较
- **年报**: 包含预测的全面年度性能分析
- **自定义日期范围**: 具有自定义日期选择的灵活报告
- **导出功能**: 多种格式的报告导出

### 👥 增强用户管理
- **Redmine集成**: 无缝的Redmine用户信息管理
- **安全认证**: 高级登录和认证系统
- **用户档案**: 包含性能历史的详细用户档案
- **头像支持**: 用户头像显示和管理

### 🔍 高级搜索和过滤
- **智能搜索**: 跨所有数据的高级搜索功能
- **动态过滤**: 按状态、优先级、分配人进行实时过滤
- **日期范围过滤器**: 灵活的基于日期的过滤选项

## 🛠 技术栈

- **后端**: Django 4.2.7 (LTS)
- **数据库**: MySQL 8.0.42
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **容器**: Docker 20.10+ & Docker Compose 2.0+
- **环境**: django-environ 0.11.2
- **图像处理**: Pillow 10.1.0
- **数据库驱动**: mysqlclient 2.2.0

## 📦 安装和设置

### 前提条件
- Docker 20.10+ 和 Docker Compose 2.0+
- Git
- 4GB+ 可用内存
- 10GB+ 磁盘空间

### 1. Docker快速开始（推荐）

#### 克隆和运行
```bash
# 克隆仓库
git clone <repository-url>
cd redmine_admin

# 启动所有服务
docker-compose up --build -d

# 检查服务状态
docker-compose ps

# 查看日志
docker-compose logs -f web
```

#### 服务管理
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 更新和重建
docker-compose up --build -d
```

### 2. 单独服务管理

#### 仅数据库
```bash
# 启动MySQL数据库
docker-compose up redmine_mysql -d

# 直接访问MySQL
docker-compose exec redmine_mysql mysql -u root -p
```

#### 仅应用程序
```bash
# 启动Django应用程序
docker-compose up web -d

# 运行Django命令
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

### 3. 开发环境设置

#### 前提条件
- Python 3.8+
- MySQL 8.0+
- pip
- virtualenv

#### 安装步骤
```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 使用数据库设置编辑.env文件

# 数据库设置
python manage.py migrate
python manage.py collectstatic --noinput

# 创建超级用户（可选）
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver 0.0.0.0:8000
```

## 🌐 访问信息

- **Web应用程序**: http://localhost:8000
- **管理界面**: http://localhost:8000/admin/
- **MySQL数据库**: localhost:3310
  - 数据库: redmine
  - 用户: root
  - 密码: aqwsde123!
  - 字符集: utf8

## 📁 项目结构

```
redmine_admin/
├── redmine/                 # 主Django应用程序
│   ├── models.py           # 数据模型（Project, Issue, TimeEntry等）
│   ├── views.py            # 视图逻辑（仪表板、报告、分析）
│   ├── urls.py             # URL路由配置
│   ├── admin.py            # Django管理界面配置
│   ├── backends.py         # 自定义认证后端
│   └── apps.py             # 应用程序配置
├── templates/              # HTML模板
│   ├── base.html          # 带导航的基础模板
│   ├── dashboard.html     # 主仪表板页面
│   ├── login.html         # 认证页面
│   ├── performance.html   # 性能分析页面
│   └── *_report.html      # 报告模板
├── static/                 # 静态资源
│   ├── css/               # 样式表
│   ├── js/                # JavaScript文件
│   └── images/            # 图像资源
├── media/                  # 用户上传文件
├── docker-compose.yml     # Docker Compose配置
├── Dockerfile             # Docker镜像定义
├── requirements.txt       # Python依赖
└── manage.py             # Django管理脚本
```

## 📊 数据模型

### 核心模型
- **Project**: 项目信息和元数据
- **Issue**: 具有完整生命周期跟踪的问题和工作项
- **TimeEntry**: 时间跟踪和工作日志
- **RedmineUser**: 用户信息和档案
- **IssueStatus**: 问题状态定义
- **Tracker**: 问题跟踪类别
- **RedmineUserAvatar**: 用户头像管理

### 问题状态工作流
- **新建 (1)**: 初始问题状态
- **进行中 (2)**: 积极开发
- **已解决 (3)**: 问题解决完成
- **反馈 (4)**: 等待反馈/审查
- **已关闭 (5)**: 问题完全完成
- **已拒绝 (6)**: 问题被拒绝/取消

### 优先级级别
- **低 (1)**: 低优先级问题
- **普通 (2)**: 标准优先级
- **高 (3)**: 高优先级问题
- **紧急 (4)**: 紧急问题
- **立即 (5)**: 关键问题

## 🔧 环境配置

### 必需环境变量
在项目根目录创建`.env`文件：

```env
# Django设置
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=mysql://root:aqwsde123!@localhost:3310/redmine

# 可选设置
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

### Docker环境变量
以下在Docker中自动设置：

```env
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=mysql://root:aqwsde123!@redmine_mysql:3306/redmine
```

## 📈 使用指南

### 1. 仪表板概览
- 导航到 http://localhost:8000
- 查看实时项目统计
- 监控最近的活动和趋势
- 访问所有功能的快速导航

### 2. 性能分析
- 访问 `/performance/` 获取详细分析
- 查看个人和团队性能指标
- 分析项目特定统计
- 跟踪随时间变化的性能趋势

### 3. 报告生成
- **周报**: `/weekly-report/` 或 `/weekly-report/<year>/<week>/`
- **月报**: `/monthly-report/` 或 `/monthly-report/<year>/<month>/`
- **年报**: `/yearly-report/` 或 `/yearly-report/<year>/`

### 4. 用户管理
- 访问用户档案和性能数据
- 查看用户头像和联系信息
- 跟踪用户活动和贡献

## 🐛 故障排除

### 常见问题和解决方案

#### 1. 数据库连接问题
```bash
# 检查MySQL容器状态
docker-compose ps redmine_mysql

# 查看MySQL日志
docker-compose logs redmine_mysql

# 测试数据库连接
docker-compose exec web python manage.py dbshell
```

#### 2. Django迁移问题
```bash
# 重置迁移
docker-compose exec web python manage.py migrate --fake-initial

# 创建新迁移
docker-compose exec web python manage.py makemigrations

# 应用迁移
docker-compose exec web python manage.py migrate
```

#### 3. 静态文件问题
```bash
# 重新收集静态文件
docker-compose exec web python manage.py collectstatic --noinput --clear

# 检查静态文件位置
docker-compose exec web python manage.py findstatic admin/css/base.css
```

#### 4. 性能问题
```bash
# 检查容器资源
docker stats

# 查看应用程序日志
docker-compose logs -f web

# 重启服务
docker-compose restart
```

### 性能优化
- 启用数据库查询缓存
- 优化静态文件服务
- 使用数据库连接池
- 实现适当的索引

## 🔒 安全考虑

### 认证
- Redmine集成的自定义认证后端
- 具有可配置过期时间的会话管理
- 密码哈希和安全

### 数据保护
- 数据库连接加密
- 输入验证和清理
- SQL注入防护
- XSS防护

### 访问控制
- 基于角色的访问控制
- 用户权限管理
- 审计日志功能

## 🚀 部署

### 生产部署
```bash
# 设置生产环境
export DJANGO_SETTINGS_MODULE=redmine_admin.settings.production

# 构建生产镜像
docker build -t redmine-admin:production .

# 使用生产设置运行
docker-compose -f docker-compose.prod.yml up -d
```

### 扩展考虑
- 高可用性的数据库复制
- 多应用程序实例的负载均衡
- 缓存层实现
- 监控和日志设置

## 🤝 贡献

我们欢迎贡献！请按照以下步骤：

1. **分叉项目**
2. **创建功能分支**: `git checkout -b feature/AmazingFeature`
3. **提交更改**: `git commit -m 'Add some AmazingFeature'`
4. **推送到分支**: `git push origin feature/AmazingFeature`
5. **打开拉取请求**

### 开发指南
- 遵循PEP 8编码标准
- 编写全面的测试
- 更新文档
- 确保向后兼容性

## 📄 许可证

本项目在MIT许可证下授权 - 详情请参阅[LICENSE](LICENSE)文件。

## 📞 支持和社区

### 获取帮助
- **文档**: 查看此README和内联代码注释
- **问题**: 在GitHub上为错误或功能请求创建issue
- **讨论**: 使用GitHub Discussions进行问题和想法讨论

### 版本历史
- **v2.0.0**: 增强的性能分析和报告
- **v1.5.0**: 添加用户头像支持和改进UI
- **v1.0.0**: 包含基本仪表板和报告的初始版本

## 🔮 路线图

### 即将推出的功能
- [ ] 实时通知
- [ ] 高级图表和可视化
- [ ] 外部集成的API端点
- [ ] 移动响应式设计改进
- [ ] 多语言支持
- [ ] 高级导出选项（PDF、Excel）

### 计划改进
- [ ] 性能优化
- [ ] 增强安全功能
- [ ] 更好的错误处理
- [ ] 全面的测试套件

---

**Redmine Admin v2.0.0** - 高级项目管理和性能分析工具

*使用Django和现代Web技术❤️构建*