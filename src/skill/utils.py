import random
import string
from django.utils.text import slugify
from django.contrib.gis.geoip2 import GeoIP2
# from django.contrib.gis.geoip2 import GeoIP2Exception
from django.conf import settings
from geoip2.errors import AddressNotFoundError


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """Source:
    https://www.codingforentrepreneurs.com/blog/random-string-generator-in-python/"""
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    Source:
    https://www.codingforentrepreneurs.com/blog/a-unique-slug-generator-for-django/
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_client_ip(request):
    ip = request.META.get('HTTP_X_REAL_IP')
    if ip:
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_country(request):
    g = GeoIP2()
    ip = get_client_ip(request)
    country = settings.DEFAULT_LANGUAGE
    if ip:
        try:
            country_code = g.country(ip)['country_code']
        except AddressNotFoundError:
            return settings.DEFAULT_LANGUAGE

        if country_code in settings.SUPPORTED_LANGUAGES:
            country = country_code
        else:
            country = settings.DEFAULT_LANGUAGE
    return country
