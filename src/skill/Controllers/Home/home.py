from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.utils import translation
import logging
from django.views.decorators.cache import cache_page

from skill.utils import get_country


logger = logging.getLogger(__name__)


def index(request):
    logger.error('Houston, we have a problem!..')
    lang = get_country(request).lower()
    # activate(lang)
    name = _("Welcome to my site.")
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return render(request, 'home/index.html', {"name": name})


def locale(request):
    if request.POST:
        user_lang = request.POST.get('locale')
        activate(user_lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_lang
        return redirect('/')



