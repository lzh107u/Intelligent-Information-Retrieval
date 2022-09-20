# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:03:42 2022

@author: hankr
"""

from django import forms

class UploadFileForm( forms.Form ):
    title = forms.CharField( max_length = 50 )
    file = forms.FileField()
    
    