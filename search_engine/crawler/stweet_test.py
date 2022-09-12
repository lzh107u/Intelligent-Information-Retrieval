# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 10:59:50 2022

@author: Hank
"""

import stweet as st
import json

def try_search( keyword = '' ):
    search_tweet_task = st.SearchTweetsTask( all_words = '#' + keyword )
    output_jl_tweets = st.JsonLineFileRawOutput( keyword + '_raw_search_tweets.jl' )
    output_jl_users = st.JsonLineFileRawOutput( keyword + '_raw_search_users.jl' )
    output_print = st.PrintRawOutput()
    
    st.TweetSearchRunner( search_tweets_task = search_tweet_task, 
                         tweet_raw_data_outputs = [ output_print, output_jl_tweets ], 
                         user_raw_data_outputs = [ output_print, output_jl_users ] ).run()
    
def try_user_scrap():
    user_task = st.GetUsersTask( ['iga_swiatek' ] )
    output_json = st.JsonLineFileRawOutput( 'output_raw_user.jl' )
    output_print = st.PrintRawOutput()


    st.GetUsersRunner( get_user_task = user_task, raw_data_outputs = [ output_print, output_json ] ).run()

def try_tweet_by_id_scrap():
    id_task = st.TweetsByIdTask( '1447348840164564994' )
    output_json = st.JsonLineFileRawOutput( 'output_raw_id.jl' )
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

def parser_single_tweet( line ):
    layer1_dict = json.loads( line )
    raw_value = layer1_dict[ 'raw_value' ]
    # print( 'json_parser: type of raw_value:', type( raw_value ) )
    post_timestamp = raw_value[ 'created_at' ]
    post_id = raw_value[ 'id' ]
    post_text = raw_value[ 'full_text' ]
    post_media_dict = raw_value[ 'entities' ][ 'media' ][ 0 ]
    media_url = post_media_dict[ 'media_url_https' ]
    post_url = post_media_dict[ 'url' ]
    
    post_dict = {
        'timestamp' : post_timestamp,
        'ID' : post_id,
        'text' : post_text,
        'media_url' : media_url,
        'url' : post_url,
        }
    
    return post_dict
    
def json_parser( keyword = 'midjourney', tweet_count = 20 ):
    filename = 'crawler/' + keyword + '_raw_search_tweets.jl'
    with open( filename, 'r' ) as f:
        posts_list = []
        for count in range( tweet_count ):
            line = f.readline()
            posts_list.append( parser_single_tweet( line ) )
        
        
        return posts_list

if __name__ == '__main__':
    keyword = 'midjourney'
    # try_search( keyword )
    json_parser( keyword )
    # try_user_scrap()
    # try_tweet_by_id_scrap()    
    