# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 10:59:50 2022

@author: Hank
"""

import stweet as st
import json
import re
import os.path as path

from crawler.pubmed_nltk_analysis import nltk_pipeline

def try_search( keyword = '' ):
    search_tweet_task = st.SearchTweetsTask( all_words = keyword )
    output_jl_tweets = st.JsonLineFileRawOutput( 'crawler/Tweets/' + keyword + '_tweets.jl' )
    output_jl_users = st.JsonLineFileRawOutput( 'crawler/Tweets/' + keyword + '_users.jl' )
    # output_print = st.PrintRawOutput()
    
    st.TweetSearchRunner( search_tweets_task = search_tweet_task, 
                         tweet_raw_data_outputs = [ output_jl_tweets ], 
                         user_raw_data_outputs = [ output_jl_users ] ).run()
    
def try_user_scrap():
    user_task = st.GetUsersTask( ['iga_swiatek' ] )
    output_json = st.JsonLineFileRawOutput( 'output_user.jl' )
    output_print = st.PrintRawOutput()


    st.GetUsersRunner( get_user_task = user_task, raw_data_outputs = [ output_print, output_json ] ).run()

def try_tweet_by_id_scrap():
    id_task = st.TweetsByIdTask( '1447348840164564994' )
    output_json = st.JsonLineFileRawOutput( 'output_id.jl' )
    output_print = st.PrintRawOutput()
    st.TweetsByIdRunner( tweets_by_id_task = id_task, raw_data_outputs = [ output_print, output_json ] ).run()


def content_analysis( content_dict ):
    for index, name in enumerate( content_dict ):
        print( name, '-', type( content_dict[ name ] ) )
        if type( content_dict[ name ] ) is type( dict() ):
            print( '---------- search further in', name, '----------' )
            content_analysis( content_dict[ name ] )
            print( '---------- end of', name, '----------' )
    return

def display_post( post_dict ):
    for index, name in enumerate( post_dict ):
        print( name, post_dict[ name ] )

def remove_tags( text, hashtags ):
    # print( text )
    tags_text = ''
    for index, tag in enumerate( hashtags ):
        # print( 'tag', tag[ 'text' ] )
        text = re.sub( '#' + tag[ 'text' ], '', text )
        tags_text = tags_text + '#' + tag[ 'text' ] + ' '
    
    text = re.sub( 'https://t.co/[a-zA-Z0-9]+', '', text )
    text = text.strip()
    # print( text )
    return text, tags_text

def parser_single_tweet( line ):
    layer1_dict = json.loads( line )
    raw_value = layer1_dict[ 'raw_value' ]
    # print( 'json_parser: type of raw_value:', type( raw_value ) )
    post_timestamp = raw_value[ 'created_at' ]
    post_id = raw_value[ 'id' ]
    post_text = raw_value[ 'full_text' ]
    post_media_dict = raw_value[ 'entities' ][ 'media' ][ 0 ] # get only first media of the post.
    post_hashtags = raw_value[ 'entities' ][ 'hashtags' ]
    media_url = post_media_dict[ 'media_url_https' ]
    post_url = post_media_dict[ 'url' ]
    
    post_text, post_hashtags = remove_tags( post_text, post_hashtags )
    
    post_dict = {
        'timestamp' : post_timestamp,
        'ID' : post_id,
        'text' : post_text,
        'media_url' : media_url,
        'url' : post_url,
        'hashtags' : post_hashtags,
        }
    
    return post_dict

def parser_sample_file( filename, line ):
    parsed_dict = json.loads( line )[ 0 ] 
    # it will return a list, in case of a single string contain multiple dictionary.
    # print( parsed_dict )
    article = {
        'title' : filename
        }
    authors = []
    for name in parsed_dict:
        if name.lower() == 'text' or name.lower() == 'tweet_text':
            # tweet content.
            article[ 'abstract' ] = parsed_dict[ name ]
            nltk_dict = nltk_pipeline( text = parsed_dict[ name ] )
            article[ 'num_word' ] = nltk_dict[ 'basic_feature' ][ 'num_word' ]
            article[ 'num_char' ] = nltk_dict[ 'basic_feature' ][ 'num_char' ]
            article[ 'num_sentence' ] = nltk_dict[ 'basic_feature' ][ 'num_sentence' ]
            
        elif name.lower()  == 'username':
            user = parsed_dict[ name ]
            if len( user ) == 0:
                # no username is provided.
                user = '( not provided )'
            authors.append( user )
        elif name.lower() == 'urls' or name.lower() == 'twitter_url':
            urls = parsed_dict[ name ]
            if len( urls ) < 10:
                urls = '#'
            article[ 'url' ] = urls
    
    article_dict = {
        'article' : article,
        'authors' : authors
        }
    
    return article_dict

def json_parser( keyword = 'midjourney', tweet_count = 3 ):
    filename = 'crawler/Tweets/' + keyword + '_tweets.jl'
    with open( filename, 'r' ) as f:
        posts_list = []
        for count in range( tweet_count ):
            try:
                line = f.readline()
                posts_list.append( parser_single_tweet( line ) )
                # parser_single_tweet() returned the content of a single tweet post in dict format.
            except:
                print( 'stweet, json_parser: end file reading.' )
                break
        
        return posts_list # a list that contained the content of every post in dict format.

def search_tweets( keyword = 'midjourney', tweet_count = 3 ):
    if ( path.exists( "crawler/Tweets/" + keyword + '_tweets.jl' ) ):
        print( 'stweet, search_tweets: file exists.' )
        pass
    else:
        print( 'stweet, search_tweets: file does not exist.' )
        try_search( keyword )
        return search_tweets( keyword ) # receive a list from search_tweets() and return it to previous func.
    
    # json_parser() returned a list containing every post.
    return json_parser( keyword, tweet_count )

if __name__ == '__main__':
    keyword = 'midjourney'
    # try_search( keyword )
    json_parser( keyword )
    # try_user_scrap()
    # try_tweet_by_id_scrap()    
    