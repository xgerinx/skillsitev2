from .utils import get_formatted_hour
from .models import ExchangeRate


class ModuleStatusMixin:
    """Define module purchase status"""
    def get_bought_status(self, module):
        user = self.context.get('user')
        if user is not None:
            trade_info = user.profile.modules_stat.filter(module=module).first()
            if trade_info is not None:
                return 'express' if trade_info.express else 'full'
        return None


class FeatureMixin:
    """Define method for dynamic generation of feature title
    for 'duration' and 'lessons' titles.
    """

    def get_features(self, instance):
        """If feature title is 'duration' or 'lessons',
        replace 'duration' with total course duration in hours,
        replace 'lessons' with number of lessons in course.
        """
        instance_name = type(instance).__name__
        if instance_name == 'Course':
            features = instance.course_features.all()
        elif instance_name == 'Module':
            features = instance.module_features.all()
        else:
            raise ValueError(f'Course or Module instance expected, got {instance_name}')

        res = []
        for f in features:
            if f.title == 'duration':
                duration = instance.get_duration()
                time_name = get_formatted_hour(duration)
                res.append({'title': f'{duration} {time_name}', 'text': f.text, 'logo': f.logo})
            elif f.title == 'lessons':
                res.append({'title': instance.get_lessons_count(), 'text': f.text, 'logo': f.logo})
            else:
                res.append({'title': f.title, 'text': f.text, 'logo': f.logo})
        return res


class CurrencyMixin:

    def get_price(self, cls):
        """Return 'price' converted to UAH if request is made from Ukraine"""
        country = self.context['country']
        if country == "UA":
            rate = ExchangeRate.objects.get(name='RUB-UAH').rate
            return int(round(cls.price * rate, -1))
        return cls.price

    def get_old_price(self, cls):
        """Return 'old_price' converted to UAH if request is made from Ukraine"""
        country = self.context['country']
        if country == "UA":
            rate = ExchangeRate.objects.get(name='RUB-UAH').rate
            return int(round(cls.old_price * rate, -1))
        return cls.old_price

    def get_currency(self, *args):
        """Return currency: 'грн' for Ukraine and '₽' otherwise"""
        return 'грн.' if self.context['country'] == 'UA' else '₽'
