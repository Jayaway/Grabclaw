#!/bin/bash
# 微信云托管 Django 服务诊断脚本

echo "========================================="
echo "微信云托管 Django 服务诊断"
echo "========================================="
echo ""

# 1. 检查代码文件
echo "📋 1. 检查代码文件..."
FILES=(
    "manage.py"
    "Procfile"
    "requirements.txt"
    "config/settings.py"
    "config/wsgi.py"
    "config/urls.py"
    "courses/urls.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (文件不存在)"
    fi
done
echo ""

# 2. 检查依赖
echo "📦 2. 检查依赖包..."
echo "  必需的 Python 包："
echo "  - Django"
echo "  - djangorestframework"
echo "  - django-cors-headers"
echo "  - gunicorn"
echo "  - whitenoise"
echo ""

# 3. 检查配置
echo "⚙️  3. 检查 Django 配置..."
echo "  ALLOWED_HOSTS: $(grep "^ALLOWED_HOSTS" config/settings.py)"
echo "  DEBUG: $(grep "^DEBUG" config/settings.py | head -1)"
echo "  CORS: $(grep "CORS_ALLOW_ALL_ORIGINS" config/settings.py)"
echo ""

# 4. 检查路由
echo "🔀 4. 检查 URL 路由..."
echo "  根路由："
grep -A 5 "^urlpatterns" config/urls.py | grep "path"
echo ""
echo "  API 路由："
grep -A 5 "^urlpatterns" courses/urls.py | grep "register"
echo ""

# 5. 测试本地服务
echo "🧪 5. 测试本地服务（如果虚拟环境已激活）..."
if command -v python &> /dev/null; then
    echo "  Python 已安装"
    echo "  运行 Django 检查："
    python manage.py check --deploy
else
    echo "  ⚠️  Python 未在 PATH 中"
fi
echo ""

# 6. API 测试建议
echo "🌐 6. API 测试建议..."
echo ""
echo "  测试根路径："
echo "  curl https://django-2yna-237212-7-1414659147.sh.run.tcloudbase.com/"
echo ""
echo "  测试课程 API："
echo "  curl https://django-2yna-237212-7-1414659147.sh.run.tcloudbase.com/api/v1/courses/"
echo ""
echo "  测试线索计数："
echo "  curl -X POST https://django-2yna-237212-7-1414659147.sh.run.tcloudbase.com/api/v1/clues/ \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"action\": \"inc\"}'"
echo ""

# 7. 部署检查
echo "🚀 7. 部署检查清单..."
echo "  [ ] 代码已推送到 GitHub"
echo "  [ ] 在微信云托管控制台触发部署"
echo "  [ ] 环境变量已配置（DJANGO_SECRET_KEY, DJANGO_DEBUG）"
echo "  [ ] 数据库配置已更新（MySQL）"
echo "  [ ] 服务启动成功（查看日志）"
echo "  [ ] API 可以正常访问"
echo ""

# 8. 常见问题
echo "❓ 8. 常见问题排查..."
echo ""
echo "  问题：返回微信云托管默认页面"
echo "  原因：Django 应用未正确启动"
echo "  解决："
echo "    1. 检查 Procfile 是否存在"
echo "    2. 查看云托管服务日志"
echo "    3. 确认 Gunicorn 启动成功"
echo ""

echo "  问题：API 返回 404"
echo "  原因：URL 路径配置错误"
echo "  解决："
echo "    1. 确认使用 /api/v1/ 前缀"
echo "    2. 检查 config/urls.py 路由配置"
echo "    3. 检查 courses/urls.py 视图注册"
echo ""

echo "  问题：CORS 跨域错误"
echo "  原因：小程序无法访问后端"
echo "  解决："
echo "    1. 检查 CORS 中间件配置"
echo "    2. 确认 CORS_ALLOW_ALL_ORIGINS=True"
echo "    3. 查看响应头是否包含 CORS 相关"
echo ""

echo "========================================="
echo "诊断完成！"
echo "========================================="
