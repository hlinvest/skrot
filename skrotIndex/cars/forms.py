# -*- coding: utf-8 -*-   
from django.forms.models import ModelForm
from cars.models import Car
from django import forms
import imghdr
from skrotIndex import settings
from ao.models import Bid
from django.db.models.aggregates import Max
date_choice= [(i,i) for i in range(1,7)]

class CarForm(ModelForm):
    duration=forms.ChoiceField(choices=date_choice)
    picture=forms.FileField(required=False)
    address=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
    
    class Meta:
        model=Car
        exclude=('slug','start_time','end_time')
        
    def clean_picture(self):
        picture=self.cleaned_data['picture']
        if picture is not None:
            if imghdr.what(picture):
                if  picture.size> settings.MAX_PIC_SIZE:
                    raise forms.ValidationError('Billedet er for stor, max størrelse på billede er  '+str(settings.MAX_PIC_SIZE)+"bit")
                else:
                    return picture
            else:
                    raise forms.ValidationError(' det er ikke et billede file')
        else:
            return None
        
class BidForm(forms.Form):
    car=forms.CharField()
    price=forms.IntegerField()
    def clean_price(self):
        price= self.cleaned_data['price']
        carID= self.cleaned_data['car']
        max_price=Bid.objects.filter(car=carID).aggregate(Max('price'))+50
    
        if price<max_price:
            raise forms.ValidationError('der er allerede en der byder højere end dig, eller du skal byde minimum 50 kroner højere end hjøst byd.')
        else:
            return price
            
    
    
        
#class BidForm(ModelForm):
#    car=forms.CharField()
#    class Meta:
#        model=Bid
#        exclude=('ao')
#    def cleaned_car(self):
#        return self.cleaned_data['car']
#    def cleaned_price(self):
#        price= self.cleaned_data['price']
#        carID= self.cleaned_data['car']
#        max_price=Bid.objects.filter(car=carID).aggregate(Max('price'))
#        if price< max_price:
#            raise forms.ValidationError('der er allerede en der byder højere end dig')
#        else:
#            return price
            
        
    
        