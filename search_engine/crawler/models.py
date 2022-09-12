from django.db import models
import crawler
# Create your models here.

class Keyword( models.Model ):
    ID = models.AutoField( primary_key = True )
    word = models.CharField( max_length = 50 )
    count = models.IntegerField()
    
class TweetPost( models.Model ):
    ID = models.AutoField( primary_key = True )
    content_text = models.CharField( max_length = 500 )
    img_url = models.CharField( max_length = 200 )
    
class RelWordInPost( models.Model ):
    word = models.ForeignKey( to = Keyword, on_delete = models.CASCADE )
    post = models.ForeignKey( to = TweetPost, on_delete = models.CASCADE )
    
    