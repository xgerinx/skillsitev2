import requests
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

from catalog.models import ExchangeRate


URLs = [
    'http://api.currencylayer.com/live',
    'http://data.fixer.io/api/latest'
]

PARAMS = [
    {
        'access_key': settings.API_KEY_CURRENCYLAYER,
        'currencies': 'USD,RUB,UAH',
        'format': 1
    },
    {
        'access_key': settings.API_KEY_FIXER,
        'symbols': 'USD,RUB,UAH'
    }
]

SITES = [
    'currencylayer',
    'fixer'
]


def get_exchange_rates(url: str, params: dict, site: str):
    """
    Return RUB-UAH exchange rate
    :param url: url to make request for currency exchange rates
    :param params: parameters to access API by the 'url'
    :param site: name of the website that provides API
    """
    r = requests.get(url, params=params)
    json = r.json()
    if json is not None:
        if json['success']:
            if site == 'currencylayer':
                RUB = json['quotes']['USDRUB']
                UAH = json['quotes']['USDUAH']
            elif site == 'fixer':
                RUB = json['rates']['RUB']
                UAH = json['rates']['UAH']
            else:
                raise ValueError(f"'site' must be 'currencylayer' or 'fixer', received '{site}' !")
            return round(UAH / RUB, 5)


def refresh_exchange_rates():
    """Set new value for 'rate' field in 'ExchangeRate' model"""
    rates = []
    for args in zip(URLs, PARAMS, SITES):
        rate = get_exchange_rates(*args)
        if isinstance(rate, float):
            rates.append(rate)
    final_rate = round(sum(rates)/len(rates), 3)

    rub_uah = ExchangeRate.objects.get(name='RUB-UAH')
    rub_uah.rate = final_rate
    rub_uah.save()


class ExchangeRatesController:

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(refresh_exchange_rates, 'interval', hours=22, minutes=11, id='currency_rates')
        self.scheduler.start(paused=True)

    def toggle_autoconversion(self, sender, instance, **kwargs):
        """Pause or resume exchange rates auto-conversion."""
        if instance.name == 'currency autoconversion':
            if instance.active:
                self.scheduler.resume()
            else:
                self.scheduler.pause()
