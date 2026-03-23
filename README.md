# 传统课程死亡倒计时 - 后端部署指南

## 项目结构

```
course_death_backend/
├── config/                 # Django 项目配置
│   ├── settings.py        # 主配置文件
│   ├── urls.py            # 主路由
│   └── wsgi.py
├── courses/               # 核心应用
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── views.py           # 视图函数
│   ├── urls.py            # 应用路由
│   └── admin.py           # 后台管理
├── venv/                  # 虚拟环境
├── logs/                  # 日志目录
├── db.sqlite3             # SQLite 数据库
├── manage.py              # Django 管理脚本
├── requirements.txt       # 依赖列表
├── init_data.py           # 初始化数据脚本
├── API.md                 # API 接口文档
└── README.md              # 本文件
```

## 本地开发环境搭建

### 1. 环境要求

- Python 3.9+
- pip
- virtualenv（可选）

### 2. 安装步骤

```bash
# 进入项目目录
cd /Users/vv/代码/微信小程序/course_death_backend

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（已完成）
pip install -r requirements.txt

# 数据库迁移（已完成）
python manage.py makemigrations
python manage.py migrate

# 初始化数据（已完成）
python manage.py shell < init_data.py
```

### 3. 创建管理员账号

```bash
python manage.py createsuperuser
# 按提示输入用户名、邮箱、密码
```

### 4. 启动开发服务器

```bash
python manage.py runserver
# 或指定端口
python manage.py runserver 0.0.0.0:8000
```

访问：
- 前端 API：http://127.0.0.1:8000/api/v1/
- 后台管理：http://127.0.0.1:8000/admin/

## 生产环境部署

### 方案一：使用 Gunicorn + Nginx

#### 1. 安装 Gunicorn

```bash
pip install gunicorn
```

#### 2. 启动 Gunicorn

```bash
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --daemon
```

#### 3. Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /static/ {
        alias /path/to/course_death_backend/static/;
    }
}
```

### 方案二：Docker 部署（推荐）

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

#### 2. 构建并运行

```bash
docker build -t course-death-backend .
docker run -d -p 8000:8000 --name course-backend course-death-backend
```

## 生产环境配置调整

### 1. 修改 settings.py

```python
# 关闭调试模式
DEBUG = False

# 设置允许的主机
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# 配置 CORS（生产环境建议使用白名单）
CORS_ALLOWED_ORIGINS = [
    "https://your-miniprogram-domain.com",
]

# 使用环境变量管理敏感信息
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key')

# 配置 MySQL（可选）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'course_death',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 2. 收集静态文件

```bash
python manage.py collectstatic
```

## 数据库迁移到 MySQL

### 1. 安装 MySQL 客户端

```bash
# macOS
brew install mysql

# Ubuntu
sudo apt-get install libmysqlclient-dev
```

### 2. 安装 Python MySQL 驱动

```bash
pip install mysqlclient
```

### 3. 创建数据库

```sql
CREATE DATABASE course_death CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'course_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON course_death.* TO 'course_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. 更新 settings.py 并迁移

```bash
python manage.py migrate
python manage.py shell < init_data.py
```

## 常见问题

### 1. CORS 跨域问题

确保 `django-cors-headers` 已安装并正确配置：
- 中间件顺序正确
- `CORS_ALLOW_ALL_ORIGINS = True`（开发环境）
- 生产环境使用 `CORS_ALLOWED_ORIGINS` 白名单

### 2. 静态文件 404

```bash
python manage.py collectstatic
```

### 3. 数据库连接失败

检查：
- 数据库服务是否启动
- 用户名密码是否正确
- 防火墙设置

### 4. 日志查看

```bash
# 开发服务器日志
tail -f logs/django.log

# Gunicorn 日志
tail -f logs/access.log
tail -f logs/error.log
```

## 性能优化建议

1. **数据库索引**：为常用查询字段添加索引
2. **缓存**：使用 Redis 缓存热点数据
3. **CDN**：静态文件使用 CDN 加速
4. **数据库连接池**：配置 `CONN_MAX_AGE`
5. **Gzip 压缩**：Nginx 开启 gzip

## 安全建议

1. 定期更新依赖包
2. 使用 HTTPS
3. 配置防火墙规则
4. 定期备份数据库
5. 限制 API 请求频率（可使用 django-ratelimit）

## 监控与维护

### 日志轮转

```bash
# 使用 logrotate
sudo nano /etc/logrotate.d/course-death

/path/to/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
}
```

### 定期备份

```bash
# SQLite 备份
cp db.sqlite3 backups/db_$(date +%Y%m%d).sqlite3

# MySQL 备份
mysqldump -u course_user -p course_death > backups/db_$(date +%Y%m%d).sql
```

## 联系与支持

- API 文档：查看 `API.md`
- 问题反馈：提交 Issue
- 技术栈：Django 4.2 + DRF + SQLite/MySQL

---

**祝部署顺利！** 🚀
