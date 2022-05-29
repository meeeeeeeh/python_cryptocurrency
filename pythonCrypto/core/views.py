from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from bs4 import BeautifulSoup as BS


def index(request):
    s = requests.Session()
    r = s.get("https://digital-money.info//")
    html = BS(r.content, 'html.parser')
    a = []
    for el in html.select(".article-list > .post"):
        title = el.select(".article-title > a")
        image = el.select(".post-image > a > img")
        description = el.select(".post-description-text > p")
        a.append({'title': title[0].text,
                  'href': title[0].get('href'),
                  'image': image[0].get('src'),
                  'description': description[0].text})
    return render(request, 'index.html', context={'a': a})


def current_price(request):
    apidata = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return render(request, 'current_crypto_price.html', {'apidata': apidata})
