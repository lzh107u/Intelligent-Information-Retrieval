from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.template.loader import render_to_string
from crawler.models import Keyword, TweetPost, RelWordInPost

from crawler.stweet_test import json_parser
from crawler.crawler import crawler_pipeline

# Create your views here.
TITLE_LIST = [ 'World', 'U.S.', 'Technology', 'Design', 'Culture', 'Business', 'Politics', 'Opinion', 'Science', 'Health', 'Style', 'Travel' ]
def render_index( request ): 
    print( 'views, render_index: called.' )
    html_string = render_to_string( "crawler/blog/index.html" )
    return HttpResponse( html_string )

def render_test( request ):
    print( 'views, render_test: called.' )
    count = 4
    
    posts_list = json_parser( keyword = 'midjourney', tweet_count = 20 ) # get twitter post.
    car_list = []
    art_list = []
    
    for index in range( count ):
        if index == 0:
            act = True
        else:
            act = False
        car_list.append( { 'act' : act, 'post' : posts_list[ index + 3 ] } )
    
    content = {
        'car_list' : car_list,
        'car_range': range( count ),
        }
    # print( type( posts_list ) )
    # print( posts_list[ 6 ] )
    html_string = render_to_string( "crawler/test/index.html", context = content )
    return HttpResponse( html_string )

def render_template( request ):
    count = 4
    content = {
        'car_range' : range( count ),
        }
    
    html_string = render_to_string( "crawler/test/test_tag.html", context = content )
    return HttpResponse( html_string )

def crawler_test( request ):
    article_list = crawler_pipeline( page_count = 1 )
    
    article = article_list[ 0 ]
    for name in article:
        print( name )
        
    for name in article[ 'nltk_dict' ][ 'basic_feature' ]:
        print( name )
    return HttpResponse( 'crawler_test called.' )

