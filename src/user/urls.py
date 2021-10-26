from django.urls import path

from .views import (
    LessonStatisticAPIView, UserLessonsList, UserAPIView, LessonCompletedAPIView,
    CabinetAPIView, ChangePasswordApiView, ChangeUserNameApiView
)

urlpatterns = [
    path('password/', ChangePasswordApiView.as_view()),
    path('name/', ChangeUserNameApiView.as_view()),
    path('cabinet/', CabinetAPIView.as_view()),
    path('lesson/<int:pk>/', LessonStatisticAPIView.as_view()),
    path('lessons/<int:pk>/', UserLessonsList.as_view()),
    path('lesson/completed/<int:pk>/', LessonCompletedAPIView.as_view(), name='lesson-viewed'),
    path('', UserAPIView.as_view(), name='get_user'),
]
