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
    accpetTerms=forms.BooleanField( error_messages={'required': 'Accepter brugervilkår og fortrolighedspolitik for at udføre registrering'},
    label="Terms")
    
    class Meta:
        model=Car
        exclude=('slug','start_time','end_time')
    def clean_steNum(self):
        stel=self.cleaned_data['stelNum']
        try:
            Car.objects.get(stelNum=stel)
        except Car.DoesNotExist:
            return stel
        raise forms.ValidationError('Der er allerede en bil regiteret med dette stelnummer.')
        
    def clean_picture(self):
        picture=self.cleaned_data['picture']
        if picture is not None:
            if imghdr.what(picture):
                if  picture.size> settings.MAX_PIC_SIZE:
                    raise forms.ValidationError('Billedet er for stort. Max størrelse på billedet er  '+str(settings.MAX_PIC_SIZE)+"bit")
                else:
                    return picture
            else:
                    raise forms.ValidationError('Denne fil er ikke et billede')
        else:
            return None
        
class BidForm(forms.Form):
    car=forms.CharField(widget = forms.HiddenInput())
    price=forms.IntegerField()
    def clean_price(self):
        price= self.cleaned_data['price']
        car=self.cleaned_data['car']
        p=Bid.objects.filter(car=car).aggregate(Max('price'))['price__max']
        if p is not None:
            max_price=int(p)+50
            if price<max_price:
                raise forms.ValidationError(' Du skal byde minimum 50 kroner højere end det højeste bud.')
            else:
                return price
        else:
            return price
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=200)                                 
    body = forms.CharField(max_length= 1000,widget=forms.Textarea)
    

class InactiveForm(forms.Form):
    name = forms.CharField(max_length=100)                              
    body = forms.CharField(max_length= 1000,widget=forms.Textarea)                                     

            
        
    
        