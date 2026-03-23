from django.contrib import admin
from .models import School, Major, Course, Clue


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'created_at']
    search_fields = ['name', 'province']
    list_filter = ['province']


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['major_name', 'college_name', 'school', 'id']
    search_fields = ['major_name', 'college_name', 'school__name']
    list_filter = ['school']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'major', 'credits', 'discontinued_date', 'status', 'created_at']
    search_fields = ['course_name', 'major__major_name', 'major__school__name']
    list_filter = ['status', 'discontinued_date']
    actions = ['approve_courses', 'reject_courses']

    def approve_courses(self, request, queryset):
        queryset.update(status='approved')
    approve_courses.short_description = '批准选中的课程'

    def reject_courses(self, request, queryset):
        queryset.update(status='rejected')
    reject_courses.short_description = '拒绝选中的课程'


@admin.register(Clue)
class ClueAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'school_name', 'status', 'created_at']
    search_fields = ['course_name', 'school_name', 'major_name']
    list_filter = ['status', 'created_at']
    actions = ['approve_clues', 'reject_clues']

    def approve_clues(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', reviewed_at=timezone.now())
    approve_clues.short_description = '批准选中的线索'

    def reject_clues(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='rejected', reviewed_at=timezone.now())
    reject_clues.short_description = '拒绝选中的线索'
