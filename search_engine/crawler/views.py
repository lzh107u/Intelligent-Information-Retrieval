from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django import forms
from django.template.loader import render_to_string
from crawler.models import Keyword, TweetPost, RelWordInPost

from crawler.stweet_test import json_parser
from crawler.crawler import crawler_pipeline
from crawler.tweet_ops import get_tweet
from crawler.request_handler import find_keyword_handler, search_article_handler
from re import sub, compile

# Create your views here.

PLUS = compile( '[\+]' )
def render_index( request ): 
    print( 'views, render_index: called.' )
    html_string = render_to_string( "crawler/blog/index.html" )
    return HttpResponse( html_string )

def render_test( request, keyword_str = 'Myotonic Dystrophy' ):
    global PLUS
    print( 'views, render_test: called.' )
    
    if request.method == "POST":
        form_type = request.POST.get( 'FormType' )
        if form_type == 'keyword':
            keyword_str = request.POST.get( 'Keyword' )
        elif form_type == 'FindKeyword':
            find_str = request.POST.get( 'FindKeyword' )
            print( 'views, render_test: I want to find', find_str )
            find_keyword_handler( keyword_str = find_str, article_type = 'PubMed' )
    
    keyword_str = sub( PLUS, ' ', keyword_str )
    count = 4 # how many twitter posts are needed for Carousel display.
    posts_list = json_parser( keyword = 'midjourney', tweet_count = 20 ) # get twitter post.
    car_list = [] # store carousel posts.
    art_list = [] # store pubmed posts.
    
    article_list = search_article_handler( keyword_str = keyword_str )
    # article_list = crawler_pipeline() # for temporary demo purpose.
    # get PubMed articles
    
    for index in range( count ):
        if index == 0:
            act = True
        else:
            act = False
        car_list.append( { 'act' : act, 'post' : posts_list[ index + 3 ] } )
    
    content = {
        'car_list' : car_list,
        'car_range': range( count ),
        'pubmed_list': article_list,
        'pubmed_range': range( 10 ),
        }
    
    
    return render( request = request, template_name = "crawler/test/index.html", context = content )

def render_template( request ):
    count = 4
    content = {
        'car_range' : range( count ),
        }
    
    html_string = render_to_string( "crawler/test/test_tag.html", context = content )
    return HttpResponse( html_string )

def crawler_test( request ):
    article_list = crawler_pipeline( page_count = 1, default_keyword_str = 'Myotonic Dystrophy' )
    """
    the format of a single article dict:
    {
        title : str,
        authors : list,
        text : str, # raw text without style tags
        nltk_dict : dict,
        {
            basic_feature : dict,
            {
                num_sentence : int,
                num_word : int,
                num_char : int,
            }
            freq_dict : dict,
            {
                word 1 : int, # the number of word appears in article
                word 2 : int,
                ...
            }
            freq_title : dict,
            {
                word 1 : int, # the number of word appears in article
                word 2 : int,
                ...
            }
            
        }
        check_list : list, # 4 boolean vals, which indicates the existence of 4 vars above.
        # True: exist
        # False: not exist
    }
    """
    
    try:
        article = article_list[ 0 ]
        for name in article:
            print( name )
        
        for name in article[ 'nltk_dict' ][ 'basic_feature' ]:
            print( name )
    except IndexError:
        print( 'article_list error with index problem.' )
    
    return HttpResponse( 'crawler_test called.' )

def db_test( request, keyword = 'midjourney' ):
    get_tweet( keyword )
    
    return HttpResponse( 'db_test called.' )
