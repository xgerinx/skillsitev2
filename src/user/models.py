import math
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Count
from secrets import token_urlsafe

from catalog.models import Module, Lesson


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, null=True, blank=True)
    purchased_modules = models.ManyToManyField(Module, related_name='users_bought',
                                               through='ModuleTradeInfo')
    lessons = models.ManyToManyField(Lesson, related_name='users_used', through='LessonStatistic')

    def get_next_lesson(self, module):
        """
        Return next lesson after last completed,
        if there is no completed lessons, return first lesson in 'module'
        """
        l_last = self.lessons.filter(
            users_stat__completed=True,
            section__module=module,
        ).last()

        if l_last is None:
            l_first = Lesson.objects.filter(section__module=module).first()
            return l_first
        else:
            l_next = Lesson.objects.filter(section__module=module, id__gt=l_last.id).first()
            return l_next

    def get_index_last(self, module):
        """Return serial number (in current module) of the last completed lesson"""
        l_last = self.lessons.filter(
            users_stat__completed=True,
            section__module=module,
        ).last()

        if l_last is not None:
            return Lesson.objects.filter(
                section__module=module, id__lte=l_last.id).aggregate(Count('id'))['id__count']
        return 0

    def get_progress(self, module):
        """Return percentage of completed lessons (progress),
        serial_number of last completed lesson ()"""
        completed = self.lessons.filter(
            users_stat__completed=True,
            section__module=module,
        ).aggregate(Count('id'))['id__count']

        total = Lesson.objects.filter(section__module=module).aggregate(Count('id'))['id__count']
        progress = math.floor(completed * 100 / total)
        index_last = self.get_index_last(module)
        return progress, index_last, total

    def get_course_progress(self, course):
        """Return percentage of course's completed lessons"""
        completed = len(self.lessons.filter(
            users_stat__completed=True,
            section__module__course=course,
        ))
        total = len(Lesson.objects.filter(section__module__course=course))
        progress = math.floor(completed * 100 / total)
        return progress

    def get_last_visit(self, module):
        """Return date when user last time completed lesson in given module"""
        try:
            last_visit = self.lessons_stat.filter(
                lesson__section__module=module).latest('last_visit').last_visit
            return last_visit.strftime("%d.%m.%Y")
        except LessonStatistic.DoesNotExist:
            return None

    def get_course_last_visit(self, course):
        """Return date when user last time completed lesson in given course"""
        try:
            last_visit = self.lessons_stat.filter(
                lesson__section__module__course=course).latest('last_visit').last_visit
            return last_visit.strftime("%d.%m.%Y")
        except LessonStatistic.DoesNotExist:
            return None

    def __str__(self):
        return self.user.username


class LessonStatistic(models.Model):
    """Information about lessons that users interacted with, bought or completed (demo lessons)"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='lessons_stat')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='users_stat')
    completed = models.BooleanField(default=False)
    bought = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.lesson.name} lesson statistics for {self.profile}'


class ModuleTradeInfo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='modules_stat')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='users_stat')
    express = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Module trade info'

    def __str__(self):
        return f'{self.module.course.name} - {self.module.name} | {self.profile}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance,
                                         verification_token=token_urlsafe(settings.TOKEN_NBYTES))
        # Give every new user Basic Excel module
        # This is done for convenience while testing
        if settings.DEBUG:
            mnemo = 'excelbas'
            excel_bas = Module.objects.get(mnemo=mnemo)
            ModuleTradeInfo.objects.create(profile=profile, module=excel_bas)


post_save.connect(create_profile, sender=User)
