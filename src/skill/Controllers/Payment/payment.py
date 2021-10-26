# from django.contrib.gis.geoip2 import GeoIP2
import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .yandex import yandex
from .wallet import wallet
import logging
import json


def view(request):
    return render(request, 'payment/payment.html', {})


class Payment:

    def create(self, data):
        print('//////////', data)
        confirmation_url = None
        # ip = request.META.get('REMOTE_ADDR', None)
        # url = 'http://ip-api.com/json/' + ip
        # resp = requests.get(url=url)
        # country = resp.json().get('countryCode')
        country = 'Ua'
        if data is not None:

            if country != 'UKR':
                confirmation_url = yandex.createOrder()
            else:
                confirmation_url = wallet.createOrder()
        return confirmation_url
