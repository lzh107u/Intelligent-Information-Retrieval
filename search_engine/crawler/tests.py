from django.test import TestCase
import os.path as path
# Create your tests here.

from re import sub, compile

sample = 'Atrial+Fibrillation'
PLUS = compile( '[\+]' )
# print( sub( PLUS, ' ', sample ) )

title_pattern = compile( '<[\/]*Abstract>' )

line = '<Abstract>hello</Abstract>'

print( line, sub( title_pattern, '', line ) )