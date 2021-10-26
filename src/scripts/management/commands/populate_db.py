from django.core.management.base import BaseCommand
import csv
import json

from catalog.models import (
    Categorie, Course, Module, Section, Lesson, Feature,
    Study, Filling, TargetAudience, GetToKnow, ExchangeRate
)
from skill.models import HomeData, Client, Leader, Switch

# Path to db data files
DATA_PATH = 'scripts/db_data/'


def read_file(path):
    """Read .csv or .json file
    :param path: str: path to the file to read
    :return:tuple: (headers, content):
        headers: list of file headers if file is csv; dict_keys if file is json
        content: list of tuples where each tuple is separate line of file if file is csv;
            list of dict_values if file is json.
    """
    format_ = path.split('.')[-1]

    with open(path, 'r') as f:
        if format_ == 'csv':
            reader = csv.reader(f)
            headers = next(reader)
            content = []
            for line in reader:
                content.append(tuple(line))
        elif format_ == 'json':
            data = json.load(f)
            headers = data.keys()
            content = [data.values()]
        else:
            raise TypeError(f'Unexpected format {format_}, excepted formats: csv, json')
    return headers, content


class Command(BaseCommand):
    """Defines custom management command, see details in docs:
    https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
    """
# UTILS

    def add_modules(self, instance, module_ids):
        """Add modules to many to many relation of 'instance' model
        :param instance: model to which to add modules;
        :param module_ids: string of ids of modules to add, separated by ':'
            module_ids='1:3:12';
        """
        if module_ids:
            module_ids = module_ids.split(':')
            modules = Module.objects.filter(pk__in=module_ids).all()
            instance.modules.add(*modules)

    def add_courses(self, instance, course_ids):
        """Add courses to many to many relation of 'instance' model
        :param instance: model to which to add courses;
        :param course_ids: string of ids of courses to add, separated by ':'
            course_ids='1:3:12';
        """
        if course_ids:
            course_ids = course_ids.split(':')
            courses = Course.objects.filter(pk__in=course_ids).all()
            instance.courses.add(*courses)

# CATALOG

    def populate_categories(self):
        self.stdout.write('Populating categories...')
        header, content = read_file(DATA_PATH + 'categories.csv')
        for id, title, name, mnemo, description, logo in content:
            Categorie.objects.create(id=id, title=title, name=name, mnemo=mnemo,
                                     description=description, logo=logo)

    def populate_courses(self):
        self.stdout.write('Populating courses...')
        header, content = read_file(DATA_PATH + 'courses.csv')
        for id, title, name, mnemo, logo, goal, descr, color, price, old_price, category_id in content:
            category = Categorie.objects.get(id=category_id)
            Course.objects.create(
                id=id, title=title, name=name, mnemo=mnemo, logo=logo, slogan_goal=goal, description=descr,
                color=color, price=price, old_price=old_price, category=category
            )

    def populate_modules(self):
        self.stdout.write('Populating modules...')
        header, content = read_file(DATA_PATH + 'modules.csv')
        for id, name, mnemo, logo, video, descr, full_descr, price, old_price, rating, course_id in content:
            course = Course.objects.get(id=course_id)
            Module.objects.create(
                id=id, name=name, mnemo=mnemo, logo=logo, video=video, description=descr,
                full_description=full_descr, price=price, old_price=old_price, course=course
            )

    def populate_sections(self):
        self.stdout.write('Populating sections...')
        header, content = read_file(DATA_PATH + 'sections.csv')
        for id, name, module_id in content:
            module = Module.objects.get(id=module_id)
            Section.objects.create(id=id, name=name, module=module)

    def populate_lessons(self):
        self.stdout.write('Populating lessons...')
        header, content = read_file(DATA_PATH + 'lessons.csv')
        for name, duration, section_id in content:
            section = Section.objects.get(id=section_id)
            Lesson.objects.create(name=name, duration=duration, section=section)

# COURSE / MODULE FILLING

    def populate_features(self):
        self.stdout.write('Populating features...')
        header, content = read_file(DATA_PATH + 'features.csv')
        for title, text, logo, course_ids, module_ids in content:
            feature = Feature.objects.create(title=title, text=text, logo=logo)
            self.add_courses(feature, course_ids)
            self.add_modules(feature, module_ids)

    def populate_study(self):
        self.stdout.write('Populating study...')
        header, content = read_file(DATA_PATH + 'study.csv')
        for topic, course_ids, module_ids in content:
            study = Study.objects.create(topic=topic)
            self.add_courses(study, course_ids)
            self.add_modules(study, module_ids)

    def populate_filling(self):
        self.stdout.write('Populating filling...')
        header, content = read_file(DATA_PATH + 'filling.csv')
        for title, logo, course_ids in content:
            filling = Filling.objects.create(title=title, logo=logo)
            self.add_courses(filling, course_ids)

    def populate_target_audience(self):
        self.stdout.write('Populating target audience...')
        header, content = read_file(DATA_PATH + 'target_audience.csv')
        for profession, logo, course_ids in content:
            audience = TargetAudience.objects.create(profession=profession, logo=logo)
            self.add_courses(audience, course_ids)

    def populate_get_to_know(self):
        self.stdout.write('Populating get to know...')
        header, content = read_file(DATA_PATH + 'get_to_know.csv')
        for text, course_ids in content:
            to_know = GetToKnow.objects.create(text=text)
            self.add_courses(to_know, course_ids)

    def populate_exchange_rate(self):
        self.stdout.write('Populating exchange rate...')
        header, content = read_file(DATA_PATH + 'exchange_rate.csv')
        for id, name, rate in content:
            ExchangeRate.objects.create(id=id, name=name, rate=rate)

# HOME PAGE

    def populate_home_data(self):
        self.stdout.write('Populating home data...')
        header, content = read_file(DATA_PATH + 'home_data.json')
        for id, font, opportunities, why_us in content:
            HomeData.objects.create(id=id, font=font, opportunities=opportunities, why_us=why_us)

    def populate_client(self):
        self.stdout.write('Populating client...')
        header, content = read_file(DATA_PATH + 'client.csv')
        for name, logo, country, home_id in content:
            home = HomeData.objects.get(id=home_id)
            Client.objects.create(name=name, logo=logo, country=country, home=home)

    def populate_switch(self):
        self.stdout.write('Populating switch...')
        header, content = read_file(DATA_PATH + 'switch.csv')
        for id, name, active in content:
            Switch.objects.create(id=id, name=name, active=active)

    def populate_leader(self):
        self.stdout.write('Populating lider...')
        header, content = read_file(DATA_PATH + 'lider.csv')
        for order, course_id, autoupdate_id, home_id in content:
            course = Course.objects.get(id=course_id)
            autoupdate = Switch.objects.get(id=autoupdate_id)
            home = HomeData.objects.get(id=home_id)
            Leader.objects.create(order=order, course=course, autoupdate=autoupdate, home=home)

    def handle(self, *args, **options):
        """Management command, can be accessed as follows:
        python manage.py populate_db
        """
        # catalog
        self.populate_categories()
        self.populate_courses()
        self.populate_modules()
        self.populate_sections()
        self.populate_lessons()
        # home page
        self.populate_home_data()
        self.populate_client()
        self.populate_switch()
        self.populate_leader()
        # course / module filling
        self.populate_features()
        self.populate_study()
        self.populate_filling()
        self.populate_target_audience()
        self.populate_get_to_know()
        self.populate_exchange_rate()
