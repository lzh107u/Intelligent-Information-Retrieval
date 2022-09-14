from django.test import TestCase

# Create your tests here.

def subsub_func( a_list ):
    a_list.append( 'hello' )

def sub_func( a_list ):
    subsub_func( a_list )

def func():
    A_list = []
    for index in range( 10 ):
        sub_func( A_list )
        
    print( 'final result' )
    print( A_list )
    
func()