from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View, generic
from datetime import datetime
import json
import time
from django.views.decorators.http import require_http_methods

from .models import Clickbot


def get_colums(row):
    row = row.split(',')
    kw = row[0]
    volume = row[1]
    kw_difficulty = row[2]
    cpc = row[3]
    comp_density = row[4]
    no_of_results = row[5]
    intent = row[6]
    serp = row[7]
    trend = row[8]
    return (kw, volume, kw_difficulty, cpc, comp_density, no_of_results, intent, serp, trend)


def read_csv():
    try:
        with open("./clickad/dack_broad-match_se_2022-02-09.csv") as file:
            return file.readlines()
    except:
        print("Error opening csv file")
        return None


def read_data():
    data = read_csv()
    count = 0
    data_list = []
    for row in data[1:5]:
        row = row.strip()
        (kw, volume, kw_difficulty, cpc, comp_density,
         no_of_results, intent, serp, trend) = get_colums(row)
        geo = "Sweden"
        instance = "123456"
        niche = "Automotive"
        kw_list = "cars-se-kw.csv"
        clicks = "18231"
        est_amt = "$1289.07"
        details = "See logs"
        data_dict = {
            "geo": "%s" % geo,
            "instance": "%s" % instance,
            "niche": "%s" % niche,
            "kw_list": "%s" % kw_list,
            "clicks": "%s" % count,
            "est_amt": "%s" % est_amt,
            "details": "%s" % details
        }
        data_list.append(data_dict)
        count += 1
    data_list = """%s""" % data_list
    data_list = data_list.replace('\'', '"')
    return data_list


def get_filters():
    data = read_csv()
    count = 0
    data_list = []
    for row in data[1:5]:
        row = row.strip()
        (kw, volume, kw_difficulty, cpc, comp_density,
         no_of_results, intent, serp, trend) = get_colums(row)
        geo = "Sweden"
        niche = "Automotive"
        instance = count
        data_dict = {
            "geo": "%s" % geo,
            "niche": "%s" % niche,
            "instance": "%s" % instance
        }
        data_list.append(data_dict)
        count += 1
    data_list = """%s""" % data_list
    data_list = data_list.replace('\'', '"')
    return data_list


def get_categories():
    cat_list = ["Sweden", "Finland", "Germany"]
    data_list = []
    for index, cat in enumerate(cat_list):
        data_dict = {
            "id": "%s" % index,
            "title": "%s" % cat
        }
        data_list.append(data_dict)
    data_list = """%s""" % data_list
    data_list = data_list.replace('\'', '"')
    return data_list


@require_http_methods(["GET", "POST"])
def index(request):
    data2 = get_categories()
    subjects = json.loads(data2)
    print("KUCH TO PRINT HO")
    return JsonResponse({"subjects": subjects})


@require_http_methods(["GET", "POST"])
def get_topics_ajax(request):
    data2 = get_categories()
    subjects = json.loads(data2)
    print("KUCH TO PRINT HO get_topics_ajax")
    return JsonResponse({"subjects": subjects})


class IndexView(generic.ListView):
    template_name = 'clickad/index.html'

    def get_queryset(self):
        items, item_ids = [], []
        for item in Clickbot.objects.all():
            if item.geo_location not in item_ids:
                items.append(item)
                item_ids.append(item.geo_location)
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Clickbot.objects.all().values_list('geo_location', flat=True).distinct()
        return context


class GeoView(generic.ListView):
    # template_name = 'clickad/index.html'
    #
    # def get_queryset(self):
    #     return "clickad/index.html"

    def get_topics_ajax(self, request):
        # if request.is_ajax() and request.method == "GET":
        #     geo = request.GET.get('geo')
        #     colour = request.GET.get('niche')
        #     print("Request is Get")
        #
        # if self.request.is_ajax() and self.request.method == "GET":
        #     geo = request.GET.get('geo')
        #     colour = request.GET.get('niche')
        #     print ("Request is Post")

        data2 = get_categories()
        subjects = json.loads(data2)
        print("Subjects are:", subjects)
        return render(self.request, 'clickad/index.html', {"subjects": subjects})

    def post(self, request, *args, **kwargs):
        str = """{"friends":
                [{"count":"1","nick_name":"val1","first_name":"val2","last_name":"val3"},
                {"count":"2","nick_name":"val1","first_name":"val2","last_name":"val3"}
                ]}"""
        headers = json.loads(str)
        print("headers:", headers)
        return render(self.request, 'clickad/index.html', {"headers": headers})


class DataFilterView(View):
    def get(self, request, *args, **kwargs):
        queryset = Clickbot.objects.all()
        geo = request.GET.get('geo')
        niche = request.GET.get('niche')
        instance = request.GET.get('instance')
        start = request.GET.get('start')
        end = request.GET.get('end')

        if geo:
            queryset = queryset.filter(geo_location=geo)
        if niche:
            queryset = queryset.filter(niche=niche)
        if instance:
            queryset = queryset.filter(instance_id=instance)
        if  start:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            queryset = queryset.filter(date_time__gte=start_date)
        if  end:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            queryset = queryset.filter(date_time__lte=end_date)
            
        items, item_ids = [], []
        for item in queryset:
            if item.geo_location not in item_ids:
                items.append(item)
                item_ids.append(item.geo_location)
        html_string = render_to_string(
            'clickad/_table.html', {"adstats": items})
        return JsonResponse({"html": html_string})


class DataDetailsView(View):
    def get(self, request, *args, **kwargs):
        data = get_object_or_404(Clickbot, id=kwargs.get('id'))
        data_list = Clickbot.objects.filter(geo_location=data.geo_location)
        html_string = render_to_string(
            'clickad/_detail.html', {"data_list": data_list})
        return JsonResponse({"html": html_string})