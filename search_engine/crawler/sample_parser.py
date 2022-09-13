# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:35:08 2022

@author: Hank
"""

def pubmed_parser( full_text ):
    
    return 
def tweet_parser( full_text ):
    
    return

def parser( filename = '' ):
    
    with open( filename, 'r' ) as f:
        full_text = f.readlines()
        name_split = filename.split( '.' )
        
        if name_split[ 1 ] == 'xml':
            pubmed_parser( full_text )
        elif name_split[ 1 ] == 'json':
            tweet_parser( full_text )
    return 

if __name__ == '__main__':
    parser( 'tweettest1.json' )