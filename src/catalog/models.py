from django.db import models
from django.db.models import Sum


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    user_id = models.PositiveIntegerField()
    course_id = models.PositiveIntegerField()


# Django will add 's'
class Categorie(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    mnemo = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    logo = models.CharField(max_length=120, default='default.png')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    # type = models.CharField(max_length=120, default=None, null=True)
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    mnemo = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, default='00FF00', help_text='Hex background color of a course')
    description = models.TextField()
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField()
    video = models.URLField(default=None, blank=True, null=True)
    # test_id = models.IntegerField()
    category = models.ForeignKey(Categorie, on_delete=models.DO_NOTHING, related_name='courses')
    logo = models.CharField(max_length=120, default='default.png')
    slogan_goal = models.CharField(max_length=600, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_duration(self):
        """Return total duration of all lessons in the course in hours"""
        lessons = Lesson.objects.filter(section__module__course__mnemo=self.mnemo).all()
        time_total = lessons.aggregate(Sum('duration'))['duration__sum']
        if time_total is None or time_total == 0:
            return 0
        time_hours = round(time_total.seconds / 3600)
        return time_hours if time_hours else 1

    def get_lessons_count(self):
        """Return number of lessons in course"""
        return Lesson.objects.filter(section__module__course__mnemo=self.mnemo).count()

    def get_modules_count(self):
        """Return number of modules in course"""
        return Module.objects.filter(course__mnemo=self.mnemo).count()

    def __str__(self):
        return self.name


class ModuleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('course')


class Module(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    old_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    time = models.PositiveIntegerField(default=0, blank=True)  # update for duration and make default 0
    description = models.TextField()
    full_description = models.TextField()
    logo = models.CharField(max_length=120, default='default.png')
    cover = models.CharField(max_length=120, default='', blank=True)
    video = models.URLField(default=None, blank=True, null=True)
    mnemo = models.CharField(max_length=120, unique=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING,
                               related_name='modules')
    rating = models.ForeignKey(Rating, on_delete=models.DO_NOTHING,
                               default=None, blank=True, null=True,
                               related_name='module_rating')
    order = models.CharField(max_length=120, default='', blank=True)
    seo_title = models.CharField(max_length=120, default='', blank=True)
    # something for seo TODO
    dev = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    storyline = models.CharField(max_length=255)
    demo_storyline = models.CharField(max_length=255)

    objects = ModuleManager()

    def get_duration(self):
        """Return total duration of all lessons in the course in hours"""
        lessons = Lesson.objects.filter(section__module__mnemo=self.mnemo).all()
        time_total = lessons.aggregate(Sum('duration'))['duration__sum']
        if time_total is None or time_total == 0:
            return 0
        time_hours = round(time_total.seconds / 3600)
        return time_hours if time_hours else 1

    def get_lessons_count(self):
        """Return number of lessons in course"""
        return Lesson.objects.filter(section__module__mnemo=self.mnemo).count()

    def get_next(self):
        """Return next module in the 'course'"""
        return Module.objects.filter(course=self.course, id__gt=self.id).first()

    def __str__(self):
        return f'{self.course.name} - {self.name}'


class Section(models.Model):
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, related_name='sections')
    name = models.TextField()

    def __str__(self):
        return f'{self.name} of {self.module.name} module'


class Lesson(models.Model):
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, related_name='lessons')
    name = models.TextField()
    express = models.BooleanField(default=False)
    demo = models.BooleanField(default=False)
    duration = models.DurationField()
    video = models.FileField(default=None, upload_to='uploads/video/lessons/')

    def __str__(self):
        return f'{self.name} lesson in {self.section.name} section of {self.section.module.name} module'


class Feature(models.Model):
    """Site name: 'Почему наш курс лучший ?' """
    courses = models.ManyToManyField(Course, related_name='course_features', blank=True)
    modules = models.ManyToManyField(Module, related_name='module_features', blank=True)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title} {self.text}'


class Study(models.Model):
    """Site name: 'Чему вы научитесь ?' """
    courses = models.ManyToManyField(Course, related_name='study_in_course', blank=True)
    modules = models.ManyToManyField(Module, related_name='study_in_module', blank=True)
    topic = models.TextField()

    def __str__(self):
        return self.topic


class Filling(models.Model):
    """Site name: 'Наполнение' """
    courses = models.ManyToManyField(Course, related_name='filling')
    title = models.TextField()
    logo = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class TargetAudience(models.Model):
    """Site name: 'Для кого этот курс' """
    courses = models.ManyToManyField(Course, related_name='target_audience')
    # courses that always display current target audience objects
    perm_courses = models.ManyToManyField(Course, related_name='permanent_audience')
    profession = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)

    def __str__(self):
        return self.profession


class GetToKnow(models.Model):
    """Site name: 'В этом курсе вы узнаете' """
    courses = models.ManyToManyField(Course, related_name='get_to_know')
    text = models.TextField()

    def __str__(self):
        return self.text


class ExchangeRate(models.Model):
    name = models.CharField(max_length=7)
    rate = models.FloatField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
