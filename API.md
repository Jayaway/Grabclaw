# 传统课程死亡倒计时 - 后端 API 文档

## 基础信息

- **Base URL**: `http://127.0.0.1:8000/api/v1/`
- **响应格式**: JSON
- **统一响应结构**:
```json
{
  "code": 0,           // 0=成功, -1=失败
  "message": "提示信息",
  "data": {}           // 实际数据
}
```

---

## 1. 学校接口

### 1.1 获取学校列表

**请求**
```
GET /api/v1/schools/
```

**响应示例**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "name": "中国传媒大学",
      "province": "北京",
      "created_at": "2024-03-18T10:00:00Z"
    }
  ]
}
```

---

## 2. 专业接口

### 2.1 获取专业列表

**请求**
```
GET /api/v1/majors/
GET /api/v1/majors/?school_id=1  # 按学校筛选
```

**响应示例**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "school": 1,
      "school_name": "中国传媒大学",
      "college_name": "新闻学院",
      "major_name": "新闻学"
    }
  ]
}
```

---

## 3. 课程接口

### 3.1 获取课程列表（支持搜索）

**请求**
```
GET /api/v1/courses/
GET /api/v1/courses/?keyword=新闻        # 模糊搜索
GET /api/v1/courses/?school_id=1        # 按学校筛选
GET /api/v1/courses/?major_id=1         # 按专业筛选
```

**响应示例**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "major": 1,
      "school_name": "中国传媒大学",
      "college_name": "新闻学院",
      "major_name": "新闻学",
      "course_name": "新闻采访与写作",
      "credits": 3.0,
      "hours": 48,
      "discontinued_date": "2024-09-01",
      "reason": "课程内容与新媒体实践重复，整合至新媒体内容创作课程",
      "replacement_course": "新媒体内容创作",
      "source": "2024年秋季学期教学计划调整通知",
      "status": "approved",
      "created_at": "2024-03-18T10:00:00Z"
    }
  ]
}
```

### 3.2 课程统计接口

**请求**
```
GET /api/v1/courses/statistics/
GET /api/v1/courses/statistics/?school_id=1     # 按学校统计
GET /api/v1/courses/statistics/?year=2024       # 按年份统计
```

**响应示例**
```json
{
  "code": 0,
  "message": "统计成功",
  "data": [
    {
      "school_name": "中国传媒大学",
      "total_count": 19,
      "year": 2024
    }
  ]
}
```

---

## 4. 用户线索接口

### 4.1 提交线索

**请求**
```
POST /api/v1/clues/
Content-Type: application/json

{
  "school_name": "中国传媒大学",
  "college_name": "新闻学院",
  "major_name": "新闻学",
  "course_name": "新闻评论",
  "credits": 2.5,
  "discontinued_date": "2024-09-01",
  "reason": "与新闻写作课程合并",
  "screenshot_url": "https://example.com/screenshot.jpg",
  "announcement_url": "https://example.com/notice",
  "submitter_contact": "微信: abc123"
}
```

**响应示例**
```json
{
  "code": 0,
  "message": "提交成功，等待审核",
  "data": {
    "id": 1,
    "school_name": "中国传媒大学",
    "course_name": "新闻评论",
    "status": "pending",
    "created_at": "2024-03-18T10:00:00Z"
  }
}
```

### 4.2 获取线索列表（管理员用）

**请求**
```
GET /api/v1/clues/
GET /api/v1/clues/?status=pending  # 筛选待审核
```

**响应示例**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "school_name": "中国传媒大学",
      "course_name": "新闻评论",
      "status": "pending",
      "created_at": "2024-03-18T10:00:00Z"
    }
  ]
}
```

---

## 错误码说明

| code | 说明 |
|------|------|
| 0    | 成功 |
| -1   | 失败（具体原因见 message） |

---

## 微信小程序请求示例

```javascript
// 获取课程列表
wx.request({
  url: 'http://your-domain.com/api/v1/courses/',
  method: 'GET',
  data: {
    keyword: '新闻',
    school_id: 1
  },
  success(res) {
    if (res.data.code === 0) {
      console.log('课程列表:', res.data.data);
    } else {
      wx.showToast({ title: res.data.message, icon: 'none' });
    }
  }
});

// 提交线索
wx.request({
  url: 'http://your-domain.com/api/v1/clues/',
  method: 'POST',
  header: {
    'content-type': 'application/json'
  },
  data: {
    school_name: '中国传媒大学',
    course_name: '新闻评论',
    reason: '课程合并'
  },
  success(res) {
    if (res.data.code === 0) {
      wx.showToast({ title: '提交成功', icon: 'success' });
    }
  }
});
```

---

## 后台管理

访问 `http://127.0.0.1:8000/admin/` 进行数据管理和线索审核。

需要先创建管理员账号：
```bash
python manage.py createsuperuser
```
