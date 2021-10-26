from django.core.management.base import BaseCommand

from catalog.models import (
    Categorie, Course, Module, Section, Lesson, Feature,
    Study, Filling, TargetAudience, GetToKnow, ExchangeRate
)
from skill.models import HomeData, Client, Leader, Switch

# Models from which to delete all data
MODELS = [
    Lesson,
    Section,
    Module,
    Leader,
    Course,
    Categorie,
    Client,
    Switch,
    HomeData,
    Feature,
    Study,
    Filling,
    TargetAudience,
    GetToKnow,
    ExchangeRate,
]


class Command(BaseCommand):
    """Defines custom management command, see details in docs:
    https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
    """

    def handle(self, *args, **options):
        names = []
        for model in MODELS:
            model.objects.all().delete()
            names.append(model.__name__)
        self.stdout.write(f'Deleted all data from {", ".join(names)}')
