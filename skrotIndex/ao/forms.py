# -*- coding: utf-8 -*-  
from django.forms.models import ModelForm
from django import forms
from ao.models import AO
import imghdr
from skrotIndex import settings

class RegiForm(ModelForm):
    password=forms.CharField(label=(u'password'), widget=forms.PasswordInput(render_value=False))
    password2=forms.CharField(label=(u'password2'), widget=forms.PasswordInput(render_value=False))
    web=forms.URLField(required=False)
    accpetTerms=forms.BooleanField( error_messages={'required': 'Accepterer brugervilkår og fortrolighedspolitik for at udføre registrering'},
    label="Terms")
    
    class Meta:
        model=AO
        exclude=('username','picture','last_login', 'bid','slug','date_joined')
        
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            AO.objects.get(username=username)
        except AO.DoesNotExist:
                return username      
        raise forms.ValidationError('Brugernavn er optaget.')
    
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            AO.objects.get(email=email)
        except AO.DoesNotExist:
            return email
        except AO.MultipleObjectsReturned:                   # it is for testing stage ,remeber change_profile form haas the same except
            raise forms.ValidationError("Denne email er allerede i brug.")
        raise forms.ValidationError("Denne email er allerede i brug.")
      
    def clean_password(self):
        password=self.cleaned_data.get('password',None)
        print password
        if len(password)<6:
            raise forms.ValidationError('Password skal minimun være på 6 tegn')
        return password
        
    def clean(self):
        password=self.cleaned_data.get('password',None)                                                       #instead of use cleaned_data, use get here to avoid exception when nothing is return, none is the default value
        password2=self.cleaned_data.get('password2',None)
        
        if password and password and (password2 == password):
            return self.cleaned_data                                                                             # this method has access too all the fields in the class, so it must return all the fields instead of one.        
        raise forms.ValidationError('De to indtastede passsword er ikke ens')

class LoginForm(forms.Form):  
                                                                                          
        username=forms.CharField(label=(u'username'))
        password=forms.CharField(max_length=10, label=(u'password'), widget=forms.PasswordInput(render_value=False))
        
        
class ChangeProfile(ModelForm):
    web=forms.URLField(required=False)
    def __init__(self, *args, **kwargs):                                       
        self.existed_email=kwargs.pop('existed_email')                         
        super(ChangeProfile, self).__init__(*args,**kwargs) 
    class Meta:
        model=AO
        exclude=('username','picture','password','password2','last_login', 'bid','slug','date_joined',)
        

    def clean_email(self):
        print 'the existed email is '+ self.existed_email
        email=self.cleaned_data['email']
        if email!=self.existed_email:
            try:
                AO.objects.get(email=email)
            except AO.DoesNotExist:
                return email
            except AO.MultipleObjectsReturned:
                raise forms.ValidationError("Denne email er allerede i brug.")
            raise forms.ValidationError("Denne email er allerede i brug.")
        return email
    
class Picture(forms.Form):
        picture=forms.FileField(required=False)    
        def clean_picture(self):
            picture=self.cleaned_data['picture']
            if picture is not None:
                if imghdr.what(picture):
                    if  picture.size> settings.MAX_PIC_SIZE:
                        raise forms.ValidationError('Billedet er for stort. Max størrelse på billedet er  '+str(settings.MAX_PIC_SIZE)+"bit")
                    else:
                        return picture
                else:
                        raise forms.ValidationError(' Denne fil er ikke et billede')
            else:
                return None
    