#!/usr/bin/python
# encoding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from skool.search import search as esearch


def index(request):
    context = RequestContext(request)
    return render_to_response('skool/index.html', None, context)


def search(request):
    context = RequestContext(request)
    q = request.GET['q']
    (hits, results) = esearch(request.GET['q'], 'btext', fuzzy=False, recommend=True, highlight=['<mark>', '</mark>'])
    return render_to_response('skool/search.html', {'pages': results, 'searchquery': q, 'itemsfound': hits}, context)


def monitor(request, url):
    context = RequestContext(request)
    (hits, results) = esearch(url, 'url')
    print results
    return render_to_response('skool/search.html', {'pages': results, 'searchquery': url, 'itemsfound': hits}, context)


def add_site(request):
    from skool.crawler import crawl, crawl_page
    context = RequestContext(request)
    if 'site' in request.POST:
        crawl(request.POST['site'])
        # Injection protection here!
        url = '../monitor/%s' % request.POST['site']
        res = "Pozadavek bude zpracovan. Prubeh muzete sledovat <a href=\"%s\">zde</a>" % url
    elif 'page' in request.POST:
        crawl_page(request.POST['page'])
        # Injection protection here!
        url = '../monitor/%s' % request.POST['page']
        res = "Pozadavek bude zpracovan. Prubeh muzete sledovat <a href=\"%s\">zde</a>" % url
    else:
        res = "Zadejte text"
    return render_to_response('skool/add_site.html', {'result': res}, context)
