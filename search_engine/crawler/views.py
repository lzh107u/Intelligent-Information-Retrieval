from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.template.loader import render_to_string
from crawler.models import Keyword, TweetPost, RelWordInPost

# Create your views here.
TITLE_LIST = [ 'World', 'U.S.', 'Technology', 'Design', 'Culture', 'Business', 'Politics', 'Opinion', 'Science', 'Health', 'Style', 'Travel' ]
def render_index( request ): 
    print( 'views, render_index: called.' )
    html_string = render_to_string( "crawler/blog/index.html" )
    return HttpResponse( html_string )

def render_test( request ):
    print( 'views, render_test: called.' )
    
    global TITLE_LIST
    
    content = {
        'title_list' : TITLE_LIST,
        }
    
    html_string = render_to_string( "crawler/test/index.html", context = content )
    return HttpResponse( html_string )

