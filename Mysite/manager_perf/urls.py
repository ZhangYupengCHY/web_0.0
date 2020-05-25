# -*- coding: utf-8 -*-
"""
Proj: web_0.0
Created on:   2020/5/19 14:24
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
    path('', views.manager_perf,name='manager_perf'),
    path('<manager_name>/', views.manager_station_data),
    path('<manager_name>/<init_every_page_num>/<current_page>/', views.manager_station_data),
    path('<manager_name>/<init_every_page_num>/<current_page>/<add_page>/', views.manager_station_data),
    # path('<int:choose_day>/<station_name>/', views.overview_station_day),
]