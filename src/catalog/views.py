from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

from .models import Module, Course, Categorie, Lesson
from .serializers import (ModuleInfoSerializer, CourseInfoSerializer, CategorySerializer, LessonSerializer)
from skill.utils import get_country


class URetrieveAPIView(RetrieveAPIView):
    """
    RetrieveAPIView with modified serializer context that includes User object
    """
    def get_user(self):
        """Return user object if request contains valid credentials"""
        jwt_auth = JWTAuthentication()
        user_token = jwt_auth.authenticate(self.request)
        if user_token is not None:
            user = user_token[0]
            return user
        else:
            return None

    def get_serializer_context(self):
        """Add user object and current user's country to serializer context"""
        country = get_country(self.request)
        context = super().get_serializer_context()
        context['country'] = country
        context['user'] = self.get_user()
        context['mnemo'] = self.kwargs['mnemo']
        return context


class ModuleDetailViewSet(URetrieveAPIView, RetrieveModelMixin, GenericViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleInfoSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'mnemo'


class CourseInfoViewSet(URetrieveAPIView, RetrieveModelMixin, GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseInfoSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'mnemo'


class CategoriesListAPIView(ListAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ModuleLessonsViewSet(URetrieveAPIView, RetrieveModelMixin, GenericViewSet):
    """
    Return all Lessons related to Module and check user for payment.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        return super().get_queryset().filter(section__module=get_object_or_404(Module, mnemo=self.kwargs['module_mnemo']))

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.profile.purchased_modules.filter(mnemo=self.kwargs['module_mnemo']):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

