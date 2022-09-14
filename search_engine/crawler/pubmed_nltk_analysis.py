# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:32:36 2022

@author: Hank
"""
import re
import nltk
from nltk.corpus import stopwords
nltk.download( 'stopwords' )
nltk.download( 'punkt' )

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;\?\-\'<>\*\:\`\.\"\=]')
NUM_SYMBOL = re.compile('[0-9]*[\.]?[0-9]+')

REPLACE_RULES = [ REPLACE_BY_SPACE_RE, NUM_SYMBOL ]
CachedStopwords = stopwords.words( "english" )

def text_token( text ):
    global CachedStopwords
    token_text = nltk.tokenize.word_tokenize( text )
    token_without_sw = []
    
    for index, seg in enumerate( token_text ):
        if seg not in CachedStopwords:
            token_without_sw.append( seg )
    
    return token_without_sw

def text_preprocess( text ):
    global REPLACE_RULES
    
    text = text.lower()
    
    for index, re_rule in enumerate( REPLACE_RULES ):
        text = re_rule.sub( '', text )
        
    token_without_sw = text_token( text )
    text = ' '.join( token_without_sw )
    
    return text, token_without_sw

def basic_feature( text ):
    global REPLACE_RULES
    
    sentences = nltk.sent_tokenize( text )
    num_sentence = len( sentences )
    
    for index, re_rule in enumerate( REPLACE_RULES ):
        text = re_rule.sub( '', text )
    
    token = nltk.tokenize.word_tokenize( text )
    num_word = len( token )
    
    num_char = 0
    for index, word in enumerate( token ):
        num_char += len( word )
    
    # print( 'num_sentence:', num_sentence )
    # print( 'num_word:', num_word )
    # print( 'num_char:', num_char )
    
    basic_feat_dict = {
        "num_sentence": num_sentence,
        "num_word": num_word,
        "num_char": num_char,
        }
    
    return basic_feat_dict

def nltk_pipeline( text ):
    basic_feat_dict = basic_feature( text )
    text, token = text_preprocess( text )
    # print( 'nltk_pipeline, processed text:' )
    # print( text )
    freq_dist_nltk = nltk.FreqDist( token )
    # print( token )
    for keyword, value in freq_dist_nltk.items():
        # print( str( keyword ) + ':' + str( value ) )
        pass
    
    nltk_dict = {
        'basic_feature' : basic_feat_dict,
        'freq_dict' : freq_dist_nltk,
        }
    return nltk_dict