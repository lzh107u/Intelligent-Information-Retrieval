from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django import forms
from django.template.loader import render_to_string
from crawler.models import Keyword, TweetPost, RelWordInPost

from crawler.stweet_test import json_parser
from crawler.crawler import crawler_pipeline
from crawler.tweet_ops import get_tweet
from crawler.request_handler import find_keyword_handler, search_article_handler, flush_database, sample_handler

from crawler.forms import UploadFileForm
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
    search_flag = False
    compare_str = ''
    if request.method == "POST":
        form_type = request.POST.get( 'FormType' )
        if form_type == 'keyword':
            keyword_str = request.POST.get( 'Keyword' )
            article_list = search_article_handler( keyword_str = keyword_str )
        elif form_type == 'FindKeyword':
            find_str = request.POST.get( 'FindKeyword' )
            file = request.FILES.get( 'myfile' )
            if file is not None:
                # a file is uploaded.
                article_upload = sample_handler( filename = file.name, content = file.read().decode('utf-8') )
                
                if find_str is not None and len( find_str ) > 0:
                    search_flag = True
                    compare_str = find_str
                    article_upload[ 'article' ][ 'abstract' ] = article_upload[ 'article' ][ 'abstract' ].split()
                article_list = [ article_upload ]
            else:
                if find_str is None:
                    # no find_str is provided.
                    article_list = find_keyword_handler( keyword_str = 'myotonic', article_type = 'PubMed' )
                elif find_str is not None and len( find_str ) == 0:
                    # find_str is provided, but no content.
                    # set to default page.
                    article_list = search_article_handler( keyword_str = keyword_str )
            
                else:
                    # find_str is provided.
                    print( 'views, render_test: I want to find', find_str, len( find_str ) )
                    article_list = find_keyword_handler( keyword_str = find_str, article_type = 'PubMed' )
        else:
            # undefined POST method.
            # turn to default page.
            article_list = search_article_handler( keyword_str = keyword_str )
    else:
        # GET method called.
        # set to default page.
        article_list = search_article_handler( keyword_str = keyword_str )
    
    keyword_str = sub( PLUS, ' ', keyword_str )
    count = 4 # how many twitter posts are needed for Carousel display.
    posts_list = json_parser( keyword = 'midjourney', tweet_count = 20 ) # get twitter post.
    car_list = [] # store carousel posts.
    art_list = [] # store pubmed posts.
    
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
        'search_flag' : search_flag,
        'compare_str' : compare_str,
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
    
    # flush_database()
    if request.method == "POST":
        form_type = request.POST.get( 'FormType' )
        if form_type == 'upload':
            form = UploadFileForm( request.POST, request.FILES )
            if form.is_valid():
                print( 'upload successfully.' )
            else:
                print( 'something wrong with form' )
            file = request.FILES.get( 'myfile' )
            print( 'type of file:', type( file ) )
            print( file )
            res = file.read().decode('utf-8')
            print( type( res ) )
            print( res )
            
            
    
    # return HttpResponse( 'db_test called.' )
    return render( request = request, template_name = "crawler/upload.html" )