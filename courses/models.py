from django.db import models
from django.utils import timezone


class School(models.Model):
    """学校表"""
    name = models.CharField(max_length=100, verbose_name='学校名称')
    province = models.CharField(max_length=50, verbose_name='省份')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        db_table = 'school'
        verbose_name = '学校'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Major(models.Model):
    """专业表"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='majors', verbose_name='所属学校')
    college_name = models.CharField(max_length=100, verbose_name='学院名称')
    major_name = models.CharField(max_length=100, verbose_name='专业名称')

    class Meta:
        db_table = 'major'
        verbose_name = '专业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.school.name} - {self.college_name} - {self.major_name}"


class Course(models.Model):
    """课程表"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]

    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='courses', verbose_name='所属专业')
    course_name = models.CharField(max_length=100, verbose_name='课程名称')
    credits = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='学分')
    hours = models.IntegerField(verbose_name='课时', null=True, blank=True)
    discontinued_date = models.DateField(verbose_name='停开时间', null=True, blank=True)
    reason = models.TextField(verbose_name='停开原因', blank=True)
    replacement_course = models.CharField(max_length=100, verbose_name='替代课程', blank=True)
    source = models.CharField(max_length=200, verbose_name='信息来源', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审核状态')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        db_table = 'course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course_name} ({self.major.major_name})"


class Clue(models.Model):
    """用户提交线索表"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]

    school_name = models.CharField(max_length=100, verbose_name='学校名称')
    college_name = models.CharField(max_length=100, verbose_name='学院名称', blank=True)
    major_name = models.CharField(max_length=100, verbose_name='专业名称', blank=True)
    course_name = models.CharField(max_length=100, verbose_name='课程名称')
    credits = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='学分', null=True, blank=True)
    discontinued_date = models.DateField(verbose_name='停开时间', null=True, blank=True)
    reason = models.TextField(verbose_name='停开原因', blank=True)
    screenshot_url = models.URLField(verbose_name='截图链接', blank=True)
    announcement_url = models.URLField(verbose_name='公告链接', blank=True)
    submitter_contact = models.CharField(max_length=100, verbose_name='提交者联系方式', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审核状态')
    admin_note = models.TextField(verbose_name='管理员备注', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='提交时间')
    reviewed_at = models.DateTimeField(verbose_name='审核时间', null=True, blank=True)

    class Meta:
        db_table = 'clue'
        verbose_name = '用户线索'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.school_name} - {self.course_name}"
