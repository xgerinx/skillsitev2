from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from .utils import unique_slug_generator
from catalog.models import Course
from tasks.exchange_rates import ExchangeRatesController


class Partition(models.Model):
    name = models.TextField()
    mnemo = models.TextField()


class Post(models.Model):
    objects = None
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-timestamp", "-updated"]


# new models
class Order(models.Model):
    resource_id = models.IntegerField()
    customer_id = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    status = models.PositiveSmallIntegerField()
    check_no = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

#
# class Resource(models.Model):
#     type = models.PositiveSmallIntegerField()


class Supplement(models.Model):
    name = models.CharField(max_length=120)
    course_id = models.IntegerField()
    type = models.PositiveSmallIntegerField()
    time = models.PositiveIntegerField()  # for seconds
    description = models.TextField()


class HomeData(models.Model):

    font = models.CharField(max_length=200, default='Montserrat')
    opportunities = JSONField(help_text='Возможности')
    why_us = JSONField(help_text='Почему наши курсы')

    class Meta:
        verbose_name_plural = "Home Data"


class Client(models.Model):
    COUNTRIES = [
        ('UA', 'Ukraine'),
        ('RU', 'Russia')
    ]

    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    country = models.CharField(max_length=2, choices=COUNTRIES, default='UA')
    home = models.ForeignKey(HomeData, on_delete=models.DO_NOTHING, related_name='clients')
    purchased_courses = models.ManyToManyField(Course, blank=True, related_name='client_bought')

    def __str__(self):
        return self.name


class Switch(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Switches"


class Leader(models.Model):
    order = models.CharField(max_length=120, default=None)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='most_sold')
    autoupdate = models.ForeignKey(Switch, on_delete=models.DO_NOTHING, related_name='leaders')
    home = models.ForeignKey(HomeData, on_delete=models.DO_NOTHING, related_name='leaders')

    def __str__(self):
        return self.course.name


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='course')
    message = models.CharField(max_length=120)
    parent_id = models.IntegerField(default=None)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


class Main_review(models.Model):
    order = models.CharField(max_length=120, default=None)
    comment_id = models.ForeignKey(Review, on_delete=models.DO_NOTHING, related_name='courses')


class Bundle(models.Model):
    name = models.CharField(max_length=120)
    discount = models.PositiveSmallIntegerField()


class BundleItem(models.Model):
    bundle_id = models.IntegerField()
    resource_id = models.IntegerField()
    type = models.PositiveSmallIntegerField()


class Purchased_bundle(models.Model):
    user_id = models.PositiveIntegerField()
    bundle_id = models.PositiveIntegerField()


class Companie(models.Model):
    name = models.CharField(max_length=120)
    logo = models.CharField(max_length=120, default='default.png')
    backg = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


class CompaniesCourse(models.Model):
    company_id = models.PositiveIntegerField()
    course_id = models.PositiveIntegerField()

    # если посмотреть таблицу то  везде где поле count =  Null
    # там анлим лицензий, можно юзать Null этого поля
    # как флаг для анлим, для пустых будет 0
    count_license = models.PositiveIntegerField()
    license_left = models.PositiveIntegerField()


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)

rates_controller = ExchangeRatesController()
post_save.connect(rates_controller.toggle_autoconversion, sender=Switch)
