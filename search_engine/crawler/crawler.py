# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests # for internet protocol comm.
from bs4 import BeautifulSoup

import pubmed_nltk_analysis as pubmed
import pattern_matching as pm

SEARCH_URL_PREFIX = 'https://pubmed.ncbi.nlm.nih.gov'

ARTICLE_COUNT = 0
    
def send_crawler( filename = '', url = "https://pubmed.ncbi.nlm.nih.gov/?term=myotonic+dystrophy", write_file = True ):
    response = requests.get( url ) # send http request and get a response.
    soup = BeautifulSoup( response.text, "html.parser" )

    buf = soup.prettify() # turn response into string.
    
    if write_file == True and len( filename ) > 4:
        # write file
        with open( filename, 'w', encoding = 'UTF-8' ) as f:
            f.write( buf )
    else:
        return buf

def check_author_exist( new_name, authors ):
    for index, name in enumerate( authors ):
        if name == new_name:
            return False
        else:
            # print( 'new_name:', new_name, ', cur_name:', name )
            pass
    return True

def parser_abstract_page( filename = '', buf = None ):
    global ARTICLE_COUNT
    if len( filename ) > 4:
        # if given filename was too short, there might be no such file,
        # which resulted in an exception.
        with open( filename, 'r', encoding = 'UTF-8' ) as f:
            full_text = f.readlines()
            # split entire page into lines.
    elif buf is not None:
        full_text = buf.split( '\n' )
        # split entire page into lines.
    else:
        # print( 'parser_abstract_page: no given buffer or filename.' )
        return False
    
    flag_title = 0
    authors_list = []
    flag_abstract = 0
    abstract_content = []
    for index, line in enumerate( full_text ):
        if ( line.find( 'heading-title' ) > 0 ) and ( flag_title == 0 ):
            ARTICLE_COUNT += 1
            # extract article title.
            print( ARTICLE_COUNT, 'title:', full_text[ index + 1 ].strip() )
            flag_title = 1
        if ( line.find( 'authors-list-item' ) > 0 ):
            # extract authors.
            new_name = full_text[ index + 2 ].strip()
            # remove redundant whitespaces
            if check_author_exist( new_name, authors_list ):
                # check if current result had been found or not.
                # same info. appeared in html message serveral times,
                # which needed to be checked or it would result in an error.
                # print( 'author:', new_name )
                authors_list.append( new_name ) # add newly found author.
        if ( line.find( 'enc-abstract' ) > 0 ):
            # start extracting the abstract of article.
            flag_abstract = 1
            
        if ( flag_abstract == 1 and line.strip() != '</div>' ):
            abstract_content.append( line.strip() )
            # extract line-by-line.
        elif ( flag_abstract == 1 and line.strip() == '</div>' ):
            # stop extracting when encounter '</div>'
            abstract_text = pm.content_concat( abstract_content )
            # remove tags and concat every line together.
            pubmed.nltk_pipeline( abstract_text )
            # perform nltk analysis.
            return True
    
    # some article didn't have the abstract part.
    print( '--------------------' )
    print( '     no abstract    ' )
    print( '--------------------' )

def parser_search_page( buf = None, filename = '', read_file = True ):
    global SEARCH_URL_PREFIX
    if read_file == True:
        with open( filename, 'r', encoding = 'UTF-8' ) as f:
            full_text = f.readlines()
            # print( 'file open' )
    else:
        # buf from crawler was an entire html page
        # which could be divided into lines by '\n'
        full_text = buf.split( '\n' )
        # print( 'parser_search_page: length of buf:', len( full_text ) )        
    
    if len( full_text ) < 1:
        # with buf.split() or f.readlines(), full_text should be a list
        # which contained entire html page line-by-line.
        # if the len of list is less than 1, the page information can't be extracted.
        
        # print( 'parser_search_page: full_text length error.' )
        return False
    
    for index, line in enumerate( full_text ):
        ret = line.find( 'data-article-id=' )
        # the url of each article was contained in a line of html.
        if ( ret > -1 ):
            res = line.split()[ 7 ]
            # split entire line into serveral tag parts
            # and only extract element 7, which was 'href'.
            res = res.split( '=' )[ 1 ][ 1:-1 ]
            # remove the symbol '"' at the head and tail of 'href' tag.
            # the extracted result should be liked: /{article_code}/
            print( 'searching url:', SEARCH_URL_PREFIX + res )
            buf = send_crawler( url = SEARCH_URL_PREFIX + res )
            # send crawler with article url.
            parser_abstract_page( buf = buf )
            # extract every useful info. in html page from crawler.  
            
    return res

def parser_keyword( keyword_str ):
    # given a keyword string, returning a valid url keywords part.
    keyword_list = keyword_str.lower().strip().split()
    # lower: url only accepts lowercase.
    # strip: remove whitespaces at the head and tail of string.
    # split: extract each keyword from string.
    # print( keyword_list )
    res = '/?term='
    for word in keyword_list:
        res = res + '+' + word
        # each keyword is concatenated by '+'
        # it's proved that add a symbol '+' between '/?term=' and the first keyword was valid.
    return res

def crawler_pipeline( page_count = 1 ):
    global SEARCH_URL_PREFIX
    global ARTICLE_COUNT
    
    ARTICLE_COUNT = 0
    default_keyword_str = 'Myotonic Dystrophy'
    page_str = '&page='
    searching_str = parser_keyword( default_keyword_str )
    for index in range( page_count ):
        # example of an url:
        #   general form: https://pubmed.ncbi.nlm.nih.gov/?term=+{keyword_1}+{keyword_2}&page={page_num}
        #   e.g. : https://pubmed.ncbi.nlm.nih.gov/?term=+myotonic+dystrophy&page=2
        buf = send_crawler( write_file = False, url = SEARCH_URL_PREFIX + searching_str + page_str + str( index + 1 ) )
        # send a crawler with given url.
        parser_search_page( read_file = False, buf = buf )
        # parse the returned html page from crawler.

if __name__ == '__main__':
    filename = 'output_af.txt'
    keyword_str = ''
    crawler_pipeline( page_count = 3 )