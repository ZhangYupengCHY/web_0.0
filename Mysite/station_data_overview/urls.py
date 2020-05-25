# -*- coding: utf-8 -*-
"""
Proj: web_0.0
Created on:   2020/4/30 13:51
@Author: RAMSEY

Standard:  
    s: data start
    t: important  temp data
    r: result
    error1: error type1 do not have file
    error2: error type2 file empty
    error3: error type3 do not have needed data
"""

from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.overview_days,name='overview_days'),
    path('<int:choose_day>/', views.overview_stations),
    path('<int:choose_day>/<station_name>/', views.overview_station_day),
]
