# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:37:09 2022

@author: Hank
"""

from crawler.models import Keyword, TweetPost, RelWordInPost, PubMedPost, MedAuthor, RelWordInMed
from crawler.crawler import crawler_pipeline

def check_pubmed_title_existence( title_str = '' ):
    # input a title and search if the database has a copy of the article or not.
    if ( len( title_str ) == 0 ):
        # No keyword is given, returning False.
        return False
    
    query_med = PubMedPost.objects.filter( title = title_str )
    
    return 

def find_pubmed_keyword( keyword_str = '' ):
    # input a keyword and find every post containing this keyword.
    
    query_keyword = Keyword.objects.filter( word = keyword_str )
    if ( query_keyword.count()  == 0 ):
        print( 'find_pubmed_keyword: no such keyword exists in every PubMed article.' )
        return False
    
    keyword_obj = query_keyword[ 0 ] # turn query obj. into Keyword obj.
    query_pubmed_keyword = RelWordInMed.objects.filter( word = keyword_obj )
    # get every PubMed article with given keyword.
    for index, rel_obj in enumerate( query_pubmed_keyword ):
        article_obj = rel_obj.post
        # get article object through relation object.
        title = article_obj.title
        print( 'title:', title )
        
    return True

def store_pubmed_article( article_list ):
    print( 'store, len:', len( article_list ) )
    for index, article in enumerate( article_list ):
        print( index, 'ready to create:', article[ 'code' ], article[ 'title' ] )
        
        if PubMedPost.objects.filter( title = article[ 'code' ] ).count() == 0:
            print( 'stored, title:', article[ 'title' ] )
            
            # if the article doesn't exist, create it.
            new_article = PubMedPost(
                        title = article[ 'title' ],
                        abstract = article[ 'text' ],
                        url = article[ 'url' ],
                        code = article[ 'code' ]
            )
            if article[ 'nltk_dict' ] is None:
                # no abstract is provided.
                new_article.empty = True
            else:
                # abstract properties:
                new_article.num_word = article[ 'nltk_dict' ][ 'basic_feature' ][ 'num_word' ]
                new_article.num_sentence = article[ 'nltk_dict' ][ 'basic_feature' ][ 'num_sentence' ]
                new_article.num_char = article[ 'nltk_dict' ][ 'basic_feature' ][ 'num_char' ]
                
            new_article.save() # don't forget to save it.
            new_article = PubMedPost.objects.filter( code = article[ 'code' ] )[ 0 ]
            
            for author in article[ 'authors' ]:
                # create every author object.
                new_author = MedAuthor( 
                        name = author,
                        article = new_article
                        )
                new_author.save()
                
            if new_article.empty == True:
                # no abstract means no frequncy words dictionary.
                pass
            else:
                for word in article[ 'nltk_dict' ][ 'freq_dict' ]: # words in abstract text.
                    # link every keyword.
                    query_word = Keyword.objects.filter( word = word ) # find keyword obj. first
                    if query_word.count() == 0:
                        # create it if it doesn't exist.
                        new_word = Keyword( 
                                word = word,
                                count = 1 )
                        new_word.save()
                    word_obj = Keyword.objects.filter( word = word )[ 0 ]
                    # link the relation.
                    new_rel = RelWordInMed(
                        word = word_obj,
                        post = new_article,
                        istitle = False )
                    new_rel.save()
            
                for word in article[ 'nltk_dict' ][ 'freq_title' ]: # words in title.
                    # link every keyword.
                    query_word = Keyword.objects.filter( word = word ) # find keyword obj. first
                    if query_word.count() == 0:
                        # create it if it doesn't exist.
                        new_word = Keyword( 
                                word = word,
                                count = 1 )
                        new_word.save()
                    
                    word_obj = Keyword.objects.filter( word = word )[ 0 ]
                    # link the relation.
                    new_rel = RelWordInMed(
                        word = word_obj,
                        post = new_article,
                        istitle = True )
                    new_rel.save()
            
    return

def set_single_article( article_obj ):
    article_dict = {
        'title' : article_obj.title,
        'url' : article_obj.url,
        'text' : article_obj.abstract,
        }
    
    return 

def check_dup_article( result_list, new_code ):
    if len( result_list ) == 0:
        # must be no duplicated if the list is empty.
        return True
    for article_dict in result_list:
        article_obj = article_dict[ 'article' ]
        if new_code == article_obj.code:
            # the input title had existed in list.
            return False
    
    # not in list, returning True.
    return True

def find_articles( keyword_str = '', article_type = 'PubMed' ):
    if len( keyword_str ) == 0:
        print( 'find_articles: no keyword is given.' )
        return None
    result_list = []
    author_list = []
    keyword_list = keyword_str.lower().strip().split()
    for word in keyword_list:
        query_keyword = Keyword.objects.filter( word = word )
        # find keyword.
        if query_keyword.count() > 0:
            # keyword exist.
            keyword_obj = query_keyword[ 0 ]
            query_rel = RelWordInMed.objects.filter( word = keyword_obj )
            # find relations with given keyword.
            for rel_obj in query_rel:
                # find articles with given keyword.
                article_obj = rel_obj.post
                print( 'find:', article_obj.title )
                if check_dup_article( result_list, article_obj.code ):
                    # not duplicated in list, adding now.
                    
                    query_author = MedAuthor.objects.filter( article = article_obj )
                    # find authors.
                    for author_obj in query_author:
                        author_list.append( author_obj.name )
                        print( 'appending:', author_obj.name )
                    article_dict = {
                        'article' : article_obj,
                        'authors' : author_list }
                    result_list.append( article_dict )
                    
    return result_list

def find_keyword_handler( keyword_str = '', article_type = 'PubMed' ):
    
    if len( keyword_str ) == 0:
        print( 'find_keyword_handler: no keyword is given.' )
        return 
    if ( article_type == 'PubMed' ):
        ret = find_pubmed_keyword( keyword_str )
        if ret == False:
            return 
            # search pubmed with given keyword and store in database.
            # article_list = crawler_pipeline( page_count = 3, default_keyword_str = 'Myotonic Dystrophy' )
            # store_pubmed_article( article_list )
    elif ( article_type == 'Tweet' ):
        pass
    else:
        pass
    
    pass

def search_article_handler( keyword_str = '', article_type = 'PubMed', page_count = 2 ):
    # input a keyword and find articles with a title containing the keyword.
    
    # for developing purpose, please remember to remove this line.
    try:
        # PubMedPost.objects.all().delete()
        pass
    except:
        print( 'no pubmedpost to delete.')
        pass
    
    print( 'handler called, keyword:', keyword_str )
    if len( keyword_str ) == 0:
        print( 'search_article_handler: no keyword is given.' )
        return False
    
    ret = find_articles( keyword_str, article_type = 'PubMed' )
    if ret == None or ( PubMedPost.objects.all().count() < page_count * 10 ):
        print('no article, sending crawler now...')
        # if no article is found with given keyword, 
        # the crawler should be sent and store result back to database.
        
        # also, if total amount of article in database is less than crawler result,
        # part of result must be new in database.
        article_list = crawler_pipeline( page_count = page_count, default_keyword_str = keyword_str )
        store_pubmed_article( article_list )
        return search_article_handler( keyword_str, article_type, page_count,  )
    else:
        print('handler: search database sequence starts.')
        return ret