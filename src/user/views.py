import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .serializers import (LessonStatisticSerializer, UserInfoSerializer,
                          CabinetSerializer, ChangePasswordSerializer, ChangeUserNameSerializer)
from .models import LessonStatistic, Profile
from catalog.models import Lesson


class UserAPIView(generics.RetrieveAPIView):

    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class LessonStatisticAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonStatisticSerializer
    permission_classes = (AllowAny,)
    # lookup_field = 'user_id'
    #
    # def get_queryset(self):
    #     queryset = LessonStatistic.objects.all()
    #     username = self.request.query_params.get('username', None)
    #     if username is not None:
    #         queryset = queryset.filter(purchaser__username=username)
    #     return queryset

    def put(self, request, pk, format=None):
        lesson = LessonStatistic.objects.filter(user_id=pk).get()
        serializer = LessonStatisticSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        # request.data.pop('email')
        serializer = LessonStatisticSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lesson = LessonStatistic.objects.filter(user_id=pk).get()
        lesson.delete()


class UserLessonsList(generics.ListAPIView):
    serializer_class = LessonStatisticSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        # user = self.request.user
        return LessonStatistic.objects.filter(user_id=pk)


class LessonCompletedAPIView(APIView):
    """Mark given lesson as completed"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return HttpResponse(json.dumps({'message': 'Lesson does not exist!'}), status=404)

        try:
            lesson_stat = LessonStatistic.objects.get(
                profile=request.user.profile,
                lesson=lesson
            )
            lesson_stat.completed = True
            lesson_stat.save()

        except LessonStatistic.DoesNotExist:
            LessonStatistic.objects.create(
                profile=request.user.profile,
                lesson=lesson,
                completed=True
            )

        return HttpResponse(json.dumps({'message': 'Lesson marked as completed!'}), status=201)


class CabinetAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = CabinetSerializer

    def get_object(self):
        user = self.request.user
        return self.queryset.get(id=user.id)


class ChangePasswordApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'massage': "Wrong old password."
                }, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserNameApiView(generics.UpdateAPIView):
    serializer_class = ChangeUserNameSerializer
    model = User

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.first_name = serializer.data.get("first_name")
            user.save()

            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Username updated successfully',
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
