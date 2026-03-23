"""
初始化数据脚本 - 中国传媒大学19门被砍课程数据
运行方式：python manage.py shell < init_data.py
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import School, Major, Course

# 创建学校
school, _ = School.objects.get_or_create(
    name='中国传媒大学',
    defaults={'province': '北京'}
)

# 创建专业
majors_data = [
    {'college_name': '新闻学院', 'major_name': '新闻学'},
    {'college_name': '电视学院', 'major_name': '广播电视编导'},
    {'college_name': '动画与数字艺术学院', 'major_name': '动画'},
    {'college_name': '戏剧影视学院', 'major_name': '戏剧影视文学'},
    {'college_name': '音乐与录音艺术学院', 'major_name': '音乐学'},
]

majors = {}
for major_data in majors_data:
    major, _ = Major.objects.get_or_create(
        school=school,
        college_name=major_data['college_name'],
        major_name=major_data['major_name']
    )
    majors[major_data['major_name']] = major

# 中传19门被砍课程数据
courses_data = [
    {
        'major': '新闻学',
        'course_name': '新闻采访与写作',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2024, 9, 1),
        'reason': '课程内容与新媒体实践重复，整合至新媒体内容创作课程',
        'replacement_course': '新媒体内容创作',
        'source': '2024年秋季学期教学计划调整通知'
    },
    {
        'major': '新闻学',
        'course_name': '传播学概论',
        'credits': 2.5,
        'hours': 40,
        'discontinued_date': date(2024, 9, 1),
        'reason': '与新闻理论课程内容交叉，合并至新闻传播理论',
        'replacement_course': '新闻传播理论',
        'source': '教务处课程优化方案'
    },
    {
        'major': '广播电视编导',
        'course_name': '电视节目策划',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2024, 9, 1),
        'reason': '传统电视节目形态变化，整合至融媒体节目制作',
        'replacement_course': '融媒体节目制作',
        'source': '电视学院课程改革文件'
    },
    {
        'major': '广播电视编导',
        'course_name': '纪录片创作',
        'credits': 4.0,
        'hours': 64,
        'discontinued_date': date(2024, 9, 1),
        'reason': '师资不足，暂停开设',
        'replacement_course': '',
        'source': '2024-2025学年课程安排'
    },
    {
        'major': '动画',
        'course_name': '传统动画技法',
        'credits': 2.0,
        'hours': 32,
        'discontinued_date': date(2024, 9, 1),
        'reason': '行业需求下降，学生选课率低',
        'replacement_course': '数字动画制作',
        'source': '动画学院专业建设报告'
    },
    {
        'major': '动画',
        'course_name': '定格动画',
        'credits': 2.5,
        'hours': 40,
        'discontinued_date': date(2024, 9, 1),
        'reason': '设备老化，维护成本高',
        'replacement_course': '',
        'source': '实验室设备更新计划'
    },
    {
        'major': '戏剧影视文学',
        'course_name': '戏曲文学',
        'credits': 2.0,
        'hours': 32,
        'discontinued_date': date(2024, 9, 1),
        'reason': '选课人数不足10人，连续三年未开班',
        'replacement_course': '',
        'source': '教务系统选课数据'
    },
    {
        'major': '戏剧影视文学',
        'course_name': '影视批评',
        'credits': 2.5,
        'hours': 40,
        'discontinued_date': date(2024, 9, 1),
        'reason': '与影视理论课程合并',
        'replacement_course': '影视理论与批评',
        'source': '课程整合方案'
    },
    {
        'major': '音乐学',
        'course_name': '民族音乐学',
        'credits': 2.0,
        'hours': 32,
        'discontinued_date': date(2024, 9, 1),
        'reason': '专业方向调整，不再作为必修课',
        'replacement_course': '',
        'source': '音乐学院培养方案修订'
    },
    {
        'major': '音乐学',
        'course_name': '音乐史',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2024, 9, 1),
        'reason': '课程内容陈旧，整合至音乐文化史',
        'replacement_course': '音乐文化史',
        'source': '课程质量评估报告'
    },
    {
        'major': '新闻学',
        'course_name': '报纸编辑',
        'credits': 2.5,
        'hours': 40,
        'discontinued_date': date(2023, 9, 1),
        'reason': '纸媒衰落，实践价值降低',
        'replacement_course': '数字媒体编辑',
        'source': '2023年课程调整通知'
    },
    {
        'major': '广播电视编导',
        'course_name': '广播节目制作',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2023, 9, 1),
        'reason': '广播行业萎缩，学生就业需求低',
        'replacement_course': '音频内容制作',
        'source': '就业数据分析报告'
    },
    {
        'major': '动画',
        'course_name': 'Flash动画',
        'credits': 2.0,
        'hours': 32,
        'discontinued_date': date(2023, 9, 1),
        'reason': 'Flash技术淘汰，Adobe停止支持',
        'replacement_course': 'HTML5动画',
        'source': '技术更新通知'
    },
    {
        'major': '戏剧影视文学',
        'course_name': '电影剧本写作',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2023, 9, 1),
        'reason': '与编剧基础课程合并',
        'replacement_course': '影视编剧',
        'source': '课程体系优化方案'
    },
    {
        'major': '音乐学',
        'course_name': '和声学',
        'credits': 2.5,
        'hours': 40,
        'discontinued_date': date(2023, 9, 1),
        'reason': '师资退休，暂无接替教师',
        'replacement_course': '',
        'source': '人事变动通知'
    },
    {
        'major': '新闻学',
        'course_name': '新闻摄影',
        'credits': 2.0,
        'hours': 32,
        'discontinued_date': date(2022, 9, 1),
        'reason': '整合至视觉传播课程',
        'replacement_course': '视觉传播',
        'source': '2022年培养方案'
    },
    {
        'major': '广播电视编导',
        'course_name': '电视摄像',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2022, 9, 1),
        'reason': '与影视摄影课程合并',
        'replacement_course': '影视摄影与制作',
        'source': '实践课程整合通知'
    },
    {
        'major': '动画',
        'course_name': '游戏美术设计',
        'credits': 3.0,
        'hours': 48,
        'discontinued_date': date(2022, 9, 1),
        'reason': '专业方向调整，转至游戏设计专业',
        'replacement_course': '',
        'source': '专业分流方案'
    },
    {
        'major': '戏剧影视文学',
        'course_name': '戏剧导演',
        'credits': 2.5,
        'hours': 40,
        'discontinued_date': date(2022, 9, 1),
        'reason': '实践场地不足，转为选修课',
        'replacement_course': '',
        'source': '场地使用调整通知'
    },
]

# 批量创建课程
created_count = 0
for course_data in courses_data:
    major_name = course_data.pop('major')
    course, created = Course.objects.get_or_create(
        major=majors[major_name],
        course_name=course_data['course_name'],
        defaults={**course_data, 'status': 'approved'}
    )
    if created:
        created_count += 1

print(f"✅ 初始化完成！")
print(f"📚 学校：{school.name}")
print(f"🎓 专业：{len(majors)} 个")
print(f"📖 课程：新增 {created_count} 门，总计 {Course.objects.count()} 门")
print(f"\n🔗 访问后台管理：http://127.0.0.1:8000/admin/")
print(f"🔗 API文档：http://127.0.0.1:8000/api/v1/")
