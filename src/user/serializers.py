from django.contrib.auth.models import User
from rest_framework import serializers

from catalog.models import Module, Course
from .models import LessonStatistic, Profile


class LessonStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStatistic
        fields = ['profile', 'lesson', 'completed', 'bought']


class UserInfoSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    def get_courses(self, *args):
        """Return purchased modules embedded in courses"""
        courses = []
        user = self.context['user']
        modules = user.profile.purchased_modules.all()
        for module in modules:
            course_id = self.course_in_courses(module.course.mnemo, courses)
            if course_id:
                courses[course_id[0]]['modules'].append({'mnemo': module.mnemo})
            else:
                courses.append({
                    'mnemo': module.course.mnemo,
                    'modules': [{'mnemo': module.mnemo}]
                })
        return courses

    def course_in_courses(self, mnemo, courses):
        """Check whether corresponding to 'mnemo' course is in 'courses'.
        Return tuple (course_id,) if course mnemo found in courses,
        return False otherwise.
        """
        for course_id, course in enumerate(courses):
            if mnemo in course.values():
                # tuple is returned here, so that converting to bool with id = 0 result was True
                return course_id,
        return False

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'courses',
        ]


class CabinetModuleSerializer(serializers.ModelSerializer):
    """Serializer used in CabinetCourseSerializer"""
    progress = serializers.SerializerMethodField()
    bought = serializers.SerializerMethodField()
    last_visit = serializers.SerializerMethodField()
    exam_status = serializers.SerializerMethodField()

    def get_progress(self, module):
        user = self.context['request'].user
        progress = user.profile.get_progress(module)
        return progress[0]

    def get_bought(self, module):
        user = self.context['request'].user
        return user.profile.purchased_modules.filter(id=module.id).exists()

    def get_last_visit(self, module):
        user = self.context['request'].user
        return user.profile.get_last_visit(module)

    def get_exam_status(self, module):
        """Placeholder for exams_status, place real data later"""
        return {'completed': False, 'exist': True, 'progress': 53}

    class Meta:
        model = Module
        fields = [
            'id',
            'mnemo',
            'name',
            'progress',
            'last_visit',
            'exam_status',
            'bought',
        ]


class CabinetCourseSerializer(serializers.ModelSerializer):
    """Serializer used in CabinetSerializer"""
    modules = CabinetModuleSerializer(many=True)
    progress = serializers.SerializerMethodField()
    last_visit = serializers.SerializerMethodField()
    modules_status = serializers.SerializerMethodField()
    exam_status = serializers.SerializerMethodField()

    def get_progress(self, course):
        user = self.context['request'].user
        return user.profile.get_course_progress(course)

    def get_last_visit(self, course):
        user = self.context['request'].user
        return user.profile.get_course_last_visit(course)

    def get_modules_status(self, course):
        user = self.context['request'].user
        bought = len(user.profile.purchased_modules.filter(course=course))
        completed = 0
        total = len(Module.objects.filter(course=course))
        for module in Module.objects.filter(course=course):
            if user.profile.get_progress(module)[0] == 100:
                completed += 1
        return {'bought': bought, 'completed': completed, 'total': total}

    def get_exam_status(self, course):
        """Placeholder for exams_status, place real data later"""
        return {'completed': False, 'exist': False, 'progress': 53}

    class Meta:
        model = Course
        fields = [
            'id',
            'mnemo',
            'title',
            'name',
            'progress',
            'last_visit',
            'exam_status',
            'modules_status',
            'modules',
        ]


class CabinetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    def get_user(self, profile):
        user = self.context['request'].user
        return {'first_name': user.first_name, 'email': user.email, 'avatar': 'work in progress'}

    def get_courses(self, profile):
        course_list = []
        for module in profile.purchased_modules.all():
            course_list.append(module.course)
        return CabinetCourseSerializer(set(course_list), context=self.context, many=True).data

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'courses',
        ]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUserNameSerializer(serializers.Serializer):
    model = User

    first_name = serializers.CharField(required=True)
