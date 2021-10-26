from itertools import chain
from django.db.models import Sum
from rest_framework import serializers

from .models import (Lesson, Section, Module, Categorie, Course, Rating,
                     Study, Filling, TargetAudience, GetToKnow)
from .mixins import ModuleStatusMixin, FeatureMixin, CurrencyMixin
from user.models import ModuleTradeInfo, LessonStatistic
from skill.models import Client


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, lesson):
        """Return lesson status, in format: [{'completed': bool, 'bought': bool}]"""
        user = self.context['user']
        if user is not None:
            module_stat = ModuleTradeInfo.objects.filter(profile=user.profile, module=lesson.section.module).first()
            lesson_stat = LessonStatistic.objects.filter(profile=user.profile, lesson=lesson).first()

            if module_stat or lesson_stat is not None:
                if lesson_stat is not None:
                    return [{'completed': lesson_stat.completed, 'bought': lesson_stat.bought}]

                return {'completed': False, 'bought': True}

        return {'completed': False, 'bought': False}

    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'video',
            'duration',
            'express',
            'demo',
            'status',
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating']


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    duration = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

    def get_duration(self, section):
        """Return total duration of all lessons in the section"""
        total_seconds = section.lessons.all().aggregate(Sum('duration'))['duration__sum'].seconds
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        else:
            return '{:02d}:{:02d}'.format(minutes, seconds)

    def get_lessons_count(self, section):
        """Return number of lessons in the section"""
        return section.lessons.count()

    class Meta:
        model = Section
        fields = [
            'id',
            'name',
            'duration',
            'lessons_count',
            'lessons'
        ]


class StudySerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = ['topic']


class FillingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filling
        fields = ['title', 'logo']


class TargetAudienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetAudience
        fields = ['profession', 'logo']


class GetToKnowSerializer(serializers.ModelSerializer):

    class Meta:
        model = GetToKnow
        fields = ['id', 'text']


class ModuleInfoSerializer(CurrencyMixin, FeatureMixin, ModuleStatusMixin, serializers.ModelSerializer):
    moduleFeatures = serializers.SerializerMethodField('get_features')
    studyInModule = StudySerializer(source='study_in_module', many=True, read_only=True)
    sections = SectionSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    oldPrice = serializers.SerializerMethodField('get_old_price')
    currency = serializers.SerializerMethodField()
    bought = serializers.SerializerMethodField('get_bought_status')  # get_bought_status defined in ModuleStatusMixin
    nextModule = serializers.SerializerMethodField('get_next_module')

    def get_next_module(self, module):
        """Return next module's name and mnemo."""
        next_module = module.get_next()
        if next_module is None:
            return None
        response_data = {
            'name': next_module.name,
            'mnemo': next_module.mnemo,
        }
        return response_data

    class Meta:
        model = Module
        fields = [
            'id',
            'name',
            'mnemo',
            'logo',
            'description',
            'bought',
            'price',
            'oldPrice',
            'currency',
            'video',
            'moduleFeatures',
            'studyInModule',
            'sections',
            'nextModule',
        ]


class SectionListSerializer(serializers.ModelSerializer):
    """Section list for ModuleSmallInfoSerializer"""
    class Meta:
        model = Section
        fields = [
            'name'
        ]


class ModuleSmallInfoSerializer(CurrencyMixin, ModuleStatusMixin, serializers.ModelSerializer):
    """Serializer class to use in CourseInfoSerializer for 'modules' field"""
    bought = serializers.SerializerMethodField('get_bought_status')  # get_bought_status defined in ModuleStatusMixin
    sections = SectionListSerializer(many=True, read_only=True)
    course = serializers.StringRelatedField()
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    nextLesson = serializers.SerializerMethodField(method_name='get_next_lesson')
    progress = serializers.SerializerMethodField()

    def get_next_lesson(self, module):
        user = self.context['user']
        if user is not None:
            lesson = user.profile.get_next_lesson(module)
            return {
                'id': lesson.id,
                'name': lesson.name,
                'section': lesson.section.name,
                'lastVisit': user.profile.get_last_visit(module)
            } if lesson is not None else None
        else:
            return None

    def get_progress(self, module):
        user = self.context['user']
        if user is not None:
            progress, index_last, total = user.profile.get_progress(module)
            last_visit = user.profile.get_last_visit(module)
            return {'progress': progress, 'indexNext': index_last + 1, 'total': total, 'lastVisit': last_visit}
        else:
            return None

    class Meta:
        model = Module
        fields = [
            'name',
            'mnemo',
            'course',
            'sections',
            'bought',
            'price',
            'currency',
            'nextLesson',
            'progress',
            'logo',
            'description',
        ]


class CourseInfoSerializer(CurrencyMixin, FeatureMixin, serializers.ModelSerializer):
    modules = ModuleSmallInfoSerializer(many=True, read_only=True)
    filling = FillingSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    courseFeatures = serializers.SerializerMethodField('get_features')
    # 'source' is used to modify default django fields to satisfy Frontend side style
    # targetAudience = TargetAudienceSerializer(source='target_audience', many=True, read_only=True)
    targetAudience = serializers.SerializerMethodField('get_target_audience')
    studyInCourse = StudySerializer(source='study_in_course', many=True, read_only=True)
    getToKnow = GetToKnowSerializer(source='get_to_know', many=True, read_only=True)
    price = serializers.SerializerMethodField()
    oldPrice = serializers.SerializerMethodField('get_old_price')
    currency = serializers.SerializerMethodField()
    sloganGoal = serializers.CharField(source='slogan_goal')
    clients = serializers.SerializerMethodField()

    def get_target_audience(self, course):
        """Return 5 'target_audience' objects. Objects from 'permanent_audience' relation
        returned all the time, other objects are selected randomly."""
        audience_num = 5
        # permanent -- audience that always displayed
        permanent = course.permanent_audience.all()[:audience_num]
        if len(permanent) == audience_num:
            return [TargetAudienceSerializer(a).data for a in permanent]

        places_left = audience_num - len(permanent)
        #  temporary -- audience selected randomly on each request
        temporary = course.target_audience.exclude(id__in=permanent).order_by("?")[:places_left]
        current_audience = list(chain(permanent, temporary))
        return [TargetAudienceSerializer(a).data for a in current_audience]

    def get_clients(self, *args):
        country = self.context['country']
        mnemo = self.context['mnemo']
        clients = Client.objects.filter(country=country)
        res_clients = []
        for client in clients:
            if client.purchased_courses.filter(mnemo=mnemo):
                res_clients.append({
                    'name': client.name,
                    'logo': client.logo
                })
        return res_clients

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'name',
            'mnemo',
            'logo',
            'description',
            'price',
            'oldPrice',
            'currency',
            'video',
            'sloganGoal',
            'category',
            'modules',
            'courseFeatures',
            'targetAudience',
            'filling',
            'studyInCourse',
            'getToKnow',
            'clients',
        ]


class ModuleMnemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['mnemo']


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='get_lessons_count')
    modules_count = serializers.IntegerField(source='get_modules_count')
    hours = serializers.IntegerField(source='get_duration')
    modules = ModuleMnemoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'mnemo',
            'title',
            'name',
            'logo',
            'hours',
            'lessons_count',
            'modules_count',
            'color',
            'modules',
        ]


class CourseForLiderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['mnemo', 'title', 'name', 'color']


class CategorySerializer(serializers.ModelSerializer):
    courses = CourseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Categorie
        fields = ['mnemo', 'title', 'name', 'logo', 'courses']
