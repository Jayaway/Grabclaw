# 快速启动指南

## 启动开发服务器

```bash
cd /Users/vv/代码/微信小程序/course_death_backend
source venv/bin/activate
python manage.py runserver
```

访问：
- API: http://127.0.0.1:8000/api/v1/
- 后台: http://127.0.0.1:8000/admin/

## 创建管理员

```bash
python manage.py createsuperuser
```

## 测试 API

```bash
# 安装 requests
pip install requests

# 运行测试
python test_api.py
```

## 常用命令

```bash
# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 重新初始化数据
python manage.py shell < init_data.py

# 收集静态文件（生产环境）
python manage.py collectstatic
```

## 项目文档

- `API.md` - 完整的 API 接口文档
- `README.md` - 详细的部署指南
- `test_api.py` - API 测试脚本
