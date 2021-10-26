from django.urls import path, include
from rest_framework_nested import routers

from .views import (ModuleDetailViewSet, CourseInfoViewSet, CategoriesListAPIView, ModuleLessonsViewSet)

router = routers.SimpleRouter()
router.register('course', CourseInfoViewSet, base_name='course-info')
router.register('module', ModuleDetailViewSet, base_name='module-detail')

lessons_router = routers.NestedSimpleRouter(router, 'module', lookup='module')
lessons_router.register('lessons', ModuleLessonsViewSet, base_name='module-lessons')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(lessons_router.urls)),
    path('categories/', CategoriesListAPIView.as_view(), name='categories-list'),
]
