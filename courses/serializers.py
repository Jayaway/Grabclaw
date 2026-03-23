from rest_framework import serializers
from .models import School, Major, Course, Clue


class SchoolSerializer(serializers.ModelSerializer):
    """学校序列化器"""
    class Meta:
        model = School
        fields = ['id', 'name', 'province', 'created_at']
        read_only_fields = ['id', 'created_at']


class MajorSerializer(serializers.ModelSerializer):
    """专业序列化器"""
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = Major
        fields = ['id', 'school', 'school_name', 'college_name', 'major_name']
        read_only_fields = ['id']


class CourseSerializer(serializers.ModelSerializer):
    """课程序列化器"""
    school_name = serializers.CharField(source='major.school.name', read_only=True)
    college_name = serializers.CharField(source='major.college_name', read_only=True)
    major_name = serializers.CharField(source='major.major_name', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'major', 'school_name', 'college_name', 'major_name',
            'course_name', 'credits', 'hours', 'discontinued_date',
            'reason', 'replacement_course', 'source', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ClueSerializer(serializers.ModelSerializer):
    """线索序列化器"""
    class Meta:
        model = Clue
        fields = [
            'id', 'school_name', 'college_name', 'major_name', 'course_name',
            'credits', 'discontinued_date', 'reason', 'screenshot_url',
            'announcement_url', 'submitter_contact', 'status', 'admin_note',
            'created_at', 'reviewed_at'
        ]
        read_only_fields = ['id', 'created_at', 'reviewed_at', 'status', 'admin_note']


class CourseStatSerializer(serializers.Serializer):
    """课程统计序列化器"""
    school_name = serializers.CharField()
    total_count = serializers.IntegerField()
    year = serializers.IntegerField(required=False)
