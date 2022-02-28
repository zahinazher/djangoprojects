from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime


class Clickbot(models.Model):
    geo_location = models.CharField(max_length=200)
    niche = models.CharField(max_length=200)
    instance_id = models.CharField(max_length=200)
    date_time = models.DateField()
    keyword_list = models.CharField(max_length=100, blank=True)
    keyword = models.CharField(max_length=200)
    volume = models.CharField(max_length=200)
    kw_difficulty = models.CharField(max_length=200)
    cpc = models.CharField(max_length=200)
    comp_density = models.CharField(max_length=200)
    number_of_results = models.CharField(max_length=200)
    intent = models.CharField(max_length=200)
    serp_features = models.CharField(max_length=200)
    trend = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0)
    ip = models.CharField(max_length=100, blank=True)