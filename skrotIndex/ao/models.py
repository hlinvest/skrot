from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class AO(User):
    company=models.CharField(max_length=40)
    slug=models.SlugField(unique=True)
    cvr=models.IntegerField()
    street=models.CharField(max_length=40)
    postcode=models.IntegerField()
    city=models.CharField(max_length=20)
    area=models.ForeignKey('Area', null=True,on_delete=models.SET_NULL)  
    tlf=models.IntegerField()
    web=models.URLField(null=True)
    description=models.TextField()
    picture=models.FileField(upload_to="media/aos", blank=True)
    

    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.username)                                   #method slugify() Converts to lowercase, removes non-word characters (alphanumerics and underscores) and converts spaces to hyphens. Also strips leading and trailing whitespace.
        super(AO,self).save(*args, **kwargs)     
    
    
    def __unicode__(self):
        return self.username
        
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    car=models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    ao=models.ForeignKey(AO, on_delete=models.CASCADE)
    price=models.IntegerField()
    class meta:
        ordering=['ao']
    
class Area(models.Model):
    area=models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.area
    

    
    
    
    

