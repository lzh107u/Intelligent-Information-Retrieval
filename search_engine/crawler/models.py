from django.db import models
import crawler
# Create your models here.

class Keyword( models.Model ):
    ID = models.AutoField( primary_key = True )
    word = models.CharField( max_length = 50 )
    count = models.IntegerField( default = 1 )
    
class TweetPost( models.Model ):
    ID = models.AutoField( primary_key = True )
    content_text = models.CharField( max_length = 500 )
    post_id = models.IntegerField( default = -1 )
    img_url = models.CharField( max_length = 200 )
    num_word = models.IntegerField( default = 0 )
    num_char = models.IntegerField( default = 0 )
    num_sentence = models.IntegerField( default = 0 )
    
    
class RelWordInPost( models.Model ):
    word = models.ForeignKey( to = Keyword, on_delete = models.CASCADE )
    post = models.ForeignKey( to = TweetPost, on_delete = models.CASCADE )
    hashtag = models.BooleanField( default = False )
    