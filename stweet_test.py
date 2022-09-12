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

def list_content( content_list, depth ):
    for index, element in enumerate( content_list ):
        if type( element ) is type( list() ):
            print( '---------- search further in list ----------' )
            list_content( element, depth + 1 )
            print( '---------- end ----------' )
        elif type( element ) is type( dict() ):
            print( '---------- search further in dict ----------' )
            content_analysis( element, depth + 1 )
            print( '---------- end ----------' )
        else:
            print( element )

def content_analysis( content_dict, depth ):
    for index, name in enumerate( content_dict ):
        print( name, '-', type( content_dict[ name ] ) )
        if type( content_dict[ name ] ) is type( dict() ):
            print( '---------- search further in dict', name, '----------' )
            content_analysis( content_dict[ name ], depth + 1 )
            print( '---------- end of', name, '----------' )
        elif type( content_dict[ name ] ) is type( list() ):
            print( '---------- search further in list', name, '----------' )
            list_content( content_dict[ name ], depth + 1 )
            print( '---------- end of', name, '----------' )
        else:
            print( content_dict[ name ] )
    return

def format_inspection( keyword = '', depth = 1 ):
    filename = keyword + '_raw_search_tweets.jl'
    with open( filename, 'r' ) as f:
        line = f.readline()
        parsed_json = json.loads( line )
        content_analysis( parsed_json, depth )
        
    return 


def json_parser( keyword = '' ):
    filename = keyword + '_raw_search_tweets.jl'
    with open( filename, 'r' ) as f:
        for count, line in enumerate( f.readline() ):
            print( 'count:', count )

if __name__ == '__main__':
    keyword = 'midjourney'
    # try_search( keyword )
    # json_parser( keyword )
    format_inspection( keyword )
    # try_user_scrap()
    # try_tweet_by_id_scrap()    
    