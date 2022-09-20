# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:23:42 2022

@author: Hank
"""

from crawler.models import Keyword, TweetPost, RelWordInPost
from crawler.stweet_test import search_tweets
from crawler.pubmed_nltk_analysis import nltk_pipeline

def tweet_find_keyword( keyword ):
    
    
    
    return 

def store_tweets( list_posts, keyword ):
    
    for index, post in enumerate( list_posts ):
        ret = nltk_pipeline( post[ 'text' ] )
        # create a new Tweet post.
        
        post_query = TweetPost.objects.filter( post_id = post[ 'ID' ] )
        if post_query.count() == 0:
            # current post-ID doesn't exist, create it.
            new_post = TweetPost( 
                content_text = post[ 'text' ],
                post_id = post[ 'ID' ],
                img_url = post[ 'media_url' ],
                num_word = ret[ 'basic_feature' ][ 'num_word' ],
                num_char = ret[ 'basic_feature' ][ 'num_char' ],
                num_sentence = ret[ 'basic_feature' ][ 'num_sentence' ] )
            new_post.save()
            post_obj = TweetPost.objects.filter( post_id = post[ 'ID' ] )
            for word in ret[ 'freq_dict' ]:
                if Keyword.objects.filter( word = word ).count() == 0:
                    # if keyword doesn't exist in database, then add it into database.
                    new_word = Keyword( word = word )
                    new_word.save()
                else:
                    word_obj = Keyword.objects.filter( word = word )
                    # keyword exists, adding count.
                    word_obj = word_obj[ 0 ]
                    count = word_obj.count
                    
                    count += 1
                    word_obj.count = count
                    word_obj.save()
                    
                new_rel = RelWordInPost(
                        word = Keyword.objects.filter( word = word )[ 0 ],
                        post = post_obj[ 0 ] )    
                new_rel.save()
        
            new_rel = RelWordInPost(
                        word = Keyword.objects.get( word = keyword ),
                        post = post_obj[ 0 ] )
            new_rel.save()
        else:
            post_obj = post_query[ 0 ]
            print( 'ID:', post_obj.post_id, 'exist.' )
        
    return 

def get_tweet( keyword = 'ukraine' ):
    
    db_keyword = Keyword.objects.filter( word = keyword )
    if ( db_keyword.count() == 0 ):
        # the given keyword didn't exist in database, try to search on twitter.
        print( 'get_tweet: no tweet with keyword:', keyword )
        new_word = Keyword( word = keyword ) # current keyword doesn't exist, add it into database.
        new_word.save()
        for word in Keyword.objects.all():
            # print( word.word )
            pass
        
        ret = search_tweets( keyword, tweet_count = 300 )
        store_tweets( ret, keyword )
    else:
        db_rel_res = RelWordInPost.objects.filter( word = db_keyword[ 0 ] )
        if db_rel_res.count() == 0:
            print( 'get_tweet: keyword exists, but no rel is constructed.' )
            ret = search_tweets( keyword, tweet_count = 300 )
            store_tweets( ret, keyword )
        else:
            print( 'get_tweet: keyword exists, and posts are found by rels.')
            
            # ret = search_tweets( keyword, tweet_count = 300 )
            # store_tweets( ret, keyword )
    return 