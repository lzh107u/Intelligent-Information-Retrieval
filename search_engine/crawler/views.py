from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.template.loader import render_to_string
from crawler.models import Keyword, TweetPost, RelWordInPost

from crawler.stweet_test import json_parser

# Create your views here.
TITLE_LIST = [ 'World', 'U.S.', 'Technology', 'Design', 'Culture', 'Business', 'Politics', 'Opinion', 'Science', 'Health', 'Style', 'Travel' ]
def render_index( request ): 
    print( 'views, render_index: called.' )
    html_string = render_to_string( "crawler/blog/index.html" )
    return HttpResponse( html_string )

def render_test( request ):
    print( 'views, render_test: called.' )
    count = 3
    
    posts_list = json_parser( keyword = 'midjourney', tweet_count = 20 )
    act_list = [ True, False, False ]
    car_list = []
    for index in range( 3 ):
        car_list.append( { 'act' : act_list[ index ], 'post' : posts_list[ index + 4 ] } )
    content = {
        'car_list' : car_list,
        }
    # print( type( posts_list ) )
    # print( posts_list[ 6 ] )
    html_string = render_to_string( "crawler/test/index.html", context = content )
    return HttpResponse( html_string )

