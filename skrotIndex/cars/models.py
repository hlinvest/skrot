from django.db import models
from django.utils.text import slugify
import datetime

class Car(models.Model):
        id = models.AutoField(primary_key=True)
        slug=models.SlugField(unique=True)
        plate=models.CharField(max_length=20, null=True)
        stelNum=models.CharField(max_length=20)
        art=models.CharField(max_length=20)
        year=models.CharField(max_length=20)
        brand=models.CharField(max_length=40)
        address=models.CharField(max_length=40, null=True)
        city=models.CharField(max_length=40)
        pickup=models.BooleanField()
        email=models.EmailField(max_length=75)
        tlf=models.IntegerField(null=True)
        start_time=models.DateTimeField()
        picture=models.ImageField(upload_to='media/carPictures',null=True)
        end_time=models.DateTimeField(db_index=True)
        bid_area=models.ManyToManyField('ao.Area',through='BidArea')
        
        class Meta:
            ordering=['end_time']
        
        def save(self,*args,**kwargs):
            self.slug=slugify(self.brand+"-"+self.stelNum)                                                           #method slugify() Converts to lowercase, removes non-word characters (alphanumerics and underscores) and converts spaces to hyphens. Also strips leading and trailing whitespace.
            super(Car,self).save(*args, **kwargs) 
            
        def delete(self, *args, **kwargs):
            if not self.picture:
                super(Car, self).delete(*args, **kwargs)
            else:
                print "thie car has picture" +self.picture
                self.picture.delete(False)
                super(Car, self).delete(*args, **kwargs)
                super(Car, self).delete(*args, **kwargs)
            
        def __unicode__(self):
            return self.plate

            
            
class BidArea(models.Model):
        car=models.ForeignKey(Car, on_delete=models.CASCADE)
        area=models.ForeignKey('ao.Area',null=True,on_delete=models.SET_NULL)
        
class SoldCar(models.Model):
        id=models.IntegerField(primary_key=True)
        plate=models.CharField(max_length=20,null=True)
        stelNum=models.CharField(max_length=20)
        year=models.CharField(max_length=20)
        brand=models.CharField(max_length=40)
        address=models.CharField(max_length=40, null=True)
        city=models.CharField(max_length=40)
        pickup=models.BooleanField()
        email=models.CharField(max_length=50)
        tlf=models.IntegerField(null=True)
        start_time=models.DateTimeField()
        end_time=models.DateTimeField(db_index=True)
        picture=models.ImageField(upload_to='media/carPictures',null=True)
        
class highest_bid(models.Model):
        carID=models.ForeignKey(Car, on_delete=models.CASCADE)
        bider=models.ForeignKey('ao.AO',null=True, on_delete=models.SET_NULL)
        price=models.IntegerField()
            