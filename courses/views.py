from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.db.models.functions import ExtractYear
from django.utils import timezone
import logging

from .models import School, Major, Course, Clue
from .serializers import (
    SchoolSerializer, MajorSerializer, CourseSerializer,
    ClueSerializer, CourseStatSerializer
)

logger = logging.getLogger(__name__)


class SchoolViewSet(viewsets.ModelViewSet):
    """学校管理视图集"""
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def list(self, request, *args, **kwargs):
        """获取学校列表"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 0,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"获取学校列表失败: {str(e)}")
            return Response({
                'code': -1,
                'message': f'获取失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MajorViewSet(viewsets.ModelViewSet):
    """专业管理视图集"""
    queryset = Major.objects.select_related('school').all()
    serializer_class = MajorSerializer

    def list(self, request, *args, **kwargs):
        """获取专业列表，支持按学校筛选"""
        try:
            queryset = self.get_queryset()
            school_id = request.query_params.get('school_id')
            if school_id:
                queryset = queryset.filter(school_id=school_id)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 0,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"获取专业列表失败: {str(e)}")
            return Response({
                'code': -1,
                'message': f'获取失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseViewSet(viewsets.ModelViewSet):
    """课程管理视图集"""
    queryset = Course.objects.select_related('major__school').filter(status='approved')
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        """获取课程列表，支持搜索和筛选"""
        try:
            queryset = self.get_queryset()
            
            # 搜索参数
            keyword = request.query_params.get('keyword', '').strip()
            if keyword:
                queryset = queryset.filter(
                    Q(course_name__icontains=keyword) |
                    Q(major__major_name__icontains=keyword) |
                    Q(major__school__name__icontains=keyword)
                )
            
            # 筛选参数
            school_id = request.query_params.get('school_id')
            major_id = request.query_params.get('major_id')
            
            if school_id:
                queryset = queryset.filter(major__school_id=school_id)
            if major_id:
                queryset = queryset.filter(major_id=major_id)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 0,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"获取课程列表失败: {str(e)}")
            return Response({
                'code': -1,
                'message': f'获取失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """课程统计接口 - 按学校/年份统计"""
        try:
            school_id = request.query_params.get('school_id')
            year = request.query_params.get('year')
            
            queryset = Course.objects.filter(status='approved')
            
            if school_id:
                queryset = queryset.filter(major__school_id=school_id)
            
            if year:
                queryset = queryset.filter(discontinued_date__year=year)
            
            # 按学校统计
            stats = queryset.values('major__school__name').annotate(
                total_count=Count('id')
            ).order_by('-total_count')
            
            result = []
            for item in stats:
                result.append({
                    'school_name': item['major__school__name'],
                    'total_count': item['total_count'],
                    'year': int(year) if year else None
                })
            
            return Response({
                'code': 0,
                'message': '统计成功',
                'data': result
            })
        except Exception as e:
            logger.error(f"课程统计失败: {str(e)}")
            return Response({
                'code': -1,
                'message': f'统计失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClueViewSet(viewsets.ModelViewSet):
    """用户线索管理视图集"""
    queryset = Clue.objects.all()
    serializer_class = ClueSerializer

    def create(self, request, *args, **kwargs):
        """提交线索"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            return Response({
                'code': 0,
                'message': '提交成功，等待审核',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"提交线索失败: {str(e)}")
            return Response({
                'code': -1,
                'message': f'提交失败: {str(e)}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """获取线索列表（管理员用）"""
        try:
            queryset = self.get_queryset()
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 0,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"获取线索列表失败: {str(e)}")
            return Response({
                'code': -1,
                'message': f'获取失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
