# Course Death Backend - Django API

基于 Django 4.2 和 REST Framework 的课程停开信息管理系统后端 API，已适配微信云托管。

## 项目结构

```
course_death_backend/
├── config/                 # Django 项目配置
│   ├── settings.py        # 主配置文件（支持环境变量）
│   ├── urls.py            # 主路由配置
│   └── wsgi.py            # WSGI 应用入口
├── courses/               # 课程管理应用
│   ├── models.py          # 数据模型
│   ├── serializers.py     # REST 序列化器
│   ├── views.py           # API 视图
│   └── urls.py            # 应用路由
├── Dockerfile             # Docker 容器配置
├── container.config.json  # 微信云托管配置
├── requirements.txt       # Python 依赖
└── manage.py             # Django 管理脚本
```

## API 接口

### 基础路径
`/api/v1/`

### 可用接口
- `GET /api/v1/schools/` - 获取学校列表
- `GET /api/v1/majors/` - 获取专业列表（支持按学校筛选）
- `GET /api/v1/courses/` - 获取课程列表（支持搜索和筛选）
- `GET /api/v1/courses/statistics/` - 课程统计
- `POST /api/v1/clues/` - 提交课程停开线索
- `GET /api/v1/clues/` - 获取线索列表

## 本地开发

### 1. 安装依赖
```bash
cd course_death_backend
pip install -r requirements.txt
```

### 2. 数据库迁移
```bash
python manage.py migrate
```

### 3. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 4. 启动开发服务器
```bash
python manage.py runserver
```

### 5. 测试 API
访问 `http://127.0.0.1:8000/api/v1/` 测试 API

## 微信云托管部署

### 方式一：使用官方模板部署

1. 在微信云托管控制台选择"从官方模板创建"
2. 选择"django"模板
3. 替换官方模板代码为本项目代码
4. 配置环境变量（见下方）
5. 点击部署

### 方式二：从代码仓库部署（推荐）

1. **推送代码到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Init Django backend for WeChat cloud hosting"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **创建微信云托管服务**
   - 登录 [微信云托管控制台](https://cloud.weixin.qq.com/cloudrun)
   - 选择"新建服务" → "从代码仓库"
   - 授权 GitHub 账号并选择仓库
   - 选择 `main` 分支

3. **配置环境变量**
   在微信云托管控制台配置以下环境变量：
   
   | 变量名 | 说明 | 必填 | 示例值 |
   |--------|------|------|--------|
   | `DJANGO_DEBUG` | 调试模式 | 否 | `False` |
   | `DJANGO_SECRET_KEY` | Django 密钥 | 是 | 随机生成的长字符串 |
   | `ALLOWED_HOSTS` | 允许的主机 | 否 | `.sh.run.tcloudbase.com` |
   | `MYSQL_ADDRESS` | 数据库地址 | 是 | `xxx.mysql.tencentcdb.com` |
   | `MYSQL_USERNAME` | 数据库用户名 | 是 | `root` |
   | `MYSQL_PASSWORD` | 数据库密码 | 是 | `your-password` |
   | `MYSQL_DB_NAME` | 数据库名称 | 否 | `course_death` |

4. **数据库初始化**
   部署完成后，在云托管控制台的"运行日志"中执行：
   ```bash
   python manage.py migrate
   ```

5. **访问服务**
   部署成功后，通过"公网域名访问"获取服务地址。

## 环境变量说明

### 本地开发（可选）
- 不设置任何数据库环境变量时，自动使用 SQLite（`db.sqlite3`）
- 设置 `DJANGO_DEBUG=True` 启用调试模式

### 云托管生产环境
- 必须设置 `MYSQL_ADDRESS`、`MYSQL_USERNAME`、`MYSQL_PASSWORD`
- 设置 `DJANGO_DEBUG=False` 关闭调试模式
- 设置 `DJANGO_SECRET_KEY` 为强随机字符串

## 数据库迁移

### 本地迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 云托管迁移
方式一：通过控制台"运行日志"执行
方式二：在代码中添加迁移脚本，重启服务时自动执行

## 静态文件

生产环境使用 WhiteNoise 中间件提供静态文件服务，部署时会自动收集到 `staticfiles/` 目录。

## 常见问题

### 1. 数据库连接失败
检查环境变量 `MYSQL_ADDRESS`、`MYSQL_USERNAME`、`MYSQL_PASSWORD` 是否正确配置。

### 2. API 返回 404
检查 `ALLOWED_HOSTS` 环境变量是否包含服务域名。

### 3. 部署后 API 无响应
查看"运行日志"，检查是否有错误信息，常见原因：
- 端口未正确监听（默认 8080）
- 环境变量未配置
- 数据库迁移未执行

## 技术栈

- **Web 框架**: Django 4.2
- **API 框架**: Django REST Framework 3.14
- **数据库**: SQLite（开发）/ MySQL（生产）
- **WSGI 服务器**: Gunicorn
- **静态文件**: WhiteNoise
- **跨域支持**: django-cors-headers

## 许可证

MIT License
