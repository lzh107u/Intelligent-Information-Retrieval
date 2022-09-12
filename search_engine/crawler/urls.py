# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 13:12:53 2022

@author: hankr
"""

from django.urls import path
from crawler import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path( 'index', views.render_index, name = 'render_index' ),
    path( 'test', views.render_test, name = 'render_test' ),
    ] + static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )