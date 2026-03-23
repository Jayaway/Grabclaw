from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, MajorViewSet, CourseViewSet, ClueViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'majors', MajorViewSet, basename='major')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'clues', ClueViewSet, basename='clue')

urlpatterns = [
    path('', include(router.urls)),
]
