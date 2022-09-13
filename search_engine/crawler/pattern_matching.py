# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 17:01:56 2022

@author: Hank
"""

import re

pattern = re.compile( "<[A-Za-z0-9\"\'\/\- \=]+>" )
# html tag in regular expression format.
# e.g. :
#   <p></p>
#   <strong class="sub-title"></strong>
#   ...

def content_concat( content ):
    global pattern
    
    text = ''
    for index, line in enumerate( content ):
        if pattern.match( line ) is None:
            # if current line was not a html tag, it should be concatenated to text.
            text = text + ' ' + line
    
    # print( 'concate result:', text )
    return text
    