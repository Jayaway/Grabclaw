# 微信云托管部署清单

## 前置准备 ✅

- [ ] 确保项目代码已清理（已删除 venv、logs 等不需要的文件）
- [ ] 确认 Git 仓库已初始化并提交所有更改
- [ ] 准备好 GitHub 仓库地址

## 第一步：推送代码到 GitHub

```bash
cd /Users/vv/代码/微信小程序/course_death_backend

# 如果还没有提交更改
git add .
git commit -m "Ready for WeChat cloud hosting deployment"

# 如果还没有推送远程仓库
git remote add origin YOUR_GITHUB_REPO_URL  # 替换为你的仓库地址
git branch -M main
git push -u origin main
```

## 第二步：创建微信云托管服务

1. 登录 [微信云托管控制台](https://cloud.weixin.qq.com/cloudrun)
2. 选择"新建服务"
3. 选择"从代码仓库"
4. 授权 GitHub 账号并选择仓库
5. 选择 `main` 分支
6. 点击"部署"

## 第三步：配置环境变量

在微信云托管控制台的"环境变量"页面配置以下变量：

### 必填项
| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DJANGO_SECRET_KEY` | `your-very-long-random-secret-key` | Django 密钥（**务必改为随机字符串**） |
| `MYSQL_ADDRESS` | `your-mysql-address.mysql.tencentcdb.com` | 数据库地址 |
| `MYSQL_USERNAME` | `root` | 数据库用户名 |
| `MYSQL_PASSWORD` | `your-database-password` | 数据库密码 |

### 可选项
| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DJANGO_DEBUG` | `False` | 关闭调试模式（生产环境） |
| `ALLOWED_HOSTS` | `.sh.run.tcloudbase.com` | 允许的主机域名 |
| `MYSQL_DB_NAME` | `course_death` | 数据库名称 |

## 第四步：执行数据库迁移

### 方式一：通过控制台执行（推荐）

1. 进入微信云托管控制台
2. 点击"运行日志"
3. 点击"终端"（如果有）
4. 执行以下命令：
   ```bash
   python manage.py migrate
   ```

### 方式二：重启服务时自动执行

在 `config/urls.py` 或应用启动时添加迁移代码（需要开发）。

## 第五步：验证部署

1. **检查服务状态**
   - 确认服务状态为"服务正常"（绿色圆点）
   - 查看运行日志，确认没有错误信息

2. **测试 API**
   - 获取服务公网域名
   - 访问 `https://your-domain.sh.run.tcloudbase.com/api/v1/schools/`
   - 应该返回 JSON 格式的响应

3. **常见测试接口**
   ```bash
   # 获取学校列表
   curl https://your-domain/api/v1/schools/

   # 获取课程列表
   curl https://your-domain/api/v1/courses/

   # 提交线索（测试）
   curl -X POST https://your-domain/api/v1/clues/ \
     -H "Content-Type: application/json" \
     -d '{
       "school_name": "测试学校",
       "course_name": "测试课程"
     }'
   ```

## 常见问题排查

### 1. 服务启动失败
- 检查"运行日志"，查看具体错误信息
- 确认所有必填环境变量已配置
- 检查 `requirements.txt` 中的依赖是否兼容

### 2. 数据库连接失败
- 检查 `MYSQL_ADDRESS`、`MYSQL_USERNAME`、`MYSQL_PASSWORD` 是否正确
- 确认数据库已创建且密码正确
- 检查数据库是否允许云托管 IP 访问

### 3. API 返回 400/404 错误
- 检查 `ALLOWED_HOSTS` 环境变量是否包含服务域名
- 确认请求路径正确（基础路径为 `/api/v1/`）

### 4. 静态文件加载失败
- 检查 WhiteNoise 中间件是否已启用
- 查看日志中是否有 `collectstatic` 执行信息

## 更新代码后的部署

当你修改代码后：

1. **本地提交并推送**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

2. **在微信云托管控制台重新部署**
   - 进入服务详情页
   - 点击"重新部署"
   - 选择最新提交
   - 等待部署完成

3. **如果有数据库结构变更**
   - 在"运行日志"中执行 `python manage.py migrate`
   - 或重启服务自动执行迁移

## 性能优化建议

1. **数据库优化**
   - 为常用查询字段添加索引
   - 使用 `select_related` 和 `prefetch_related` 减少查询次数

2. **缓存配置**
   - 考虑添加 Redis 缓存
   - 对静态数据和统计结果进行缓存

3. **CDN 加速**
   - 将静态文件上传到 COS 或 CDN
   - 修改 `STATIC_URL` 指向 CDN 地址

## 监控和维护

1. **定期检查**
   - 查看"运行日志"监控服务健康状态
   - 关注资源使用情况（CPU、内存、磁盘）

2. **备份数据**
   - 定期备份数据库
   - 保存环境变量配置

3. **更新依赖**
   - 定期检查 `requirements.txt` 中的依赖更新
   - 测试兼容性后更新部署
