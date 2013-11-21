# -*- coding: utf-8 -*-  
from ao.models import AO, Area, Bid
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from ao.forms import RegiForm, LoginForm, ChangeProfile
from ao import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request, area=None):

    if area is None:
        ao=AO.objects.filter( is_active=True)
    else:
        ar=Area.objects.get(area=area)
        ao=AO.objects.filter( area=ar, is_active=True)     
#    paginator=Paginator(jobs, 2)
#    page=request.GET.get('page')
#    try:
        
    return render_to_response('index.html', {'ao':ao, 'area':area}, context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():       # is a section tool
        return HttpResponseRedirect('/profile/')      
    if request.method=='POST': 
        form=RegiForm(request.POST )
        if form.is_valid():
            ar=Area.objects.get(area=form.cleaned_data['area'])
            ao=models.AO(username=form.cleaned_data['username'],company=form.cleaned_data['company'], email=form.cleaned_data['email'], description=form.cleaned_data['description'],
                           cvr=form.cleaned_data['cvr'],  street=form.cleaned_data['street'], postcode=form.cleaned_data['postcode'],
                           city=form.cleaned_data['city'], area=form.cleaned_data['area'], tlf=form.cleaned_data['tlf'], is_active=True, is_superuser=False)
            ao.set_password( form.cleaned_data['password'])    
                  
            ao.save()
            loginForm=LoginForm()           
            return render_to_response('login.html',{'form':loginForm,'text':'færdig med at registere, du kan nu logge in'},context_instance=RequestContext(request))
        else:
            return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form=RegiForm() 
        return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    
def userLogin(request, carid=None):                                              # don't call it login()
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profil/')
    if request.method=='POST':
        form=LoginForm(request.POST )
        if form.is_valid():   
            username= form.cleaned_data['username']
            password=form.cleaned_data['password' ]
            loginCustomer=authenticate(username=username,password=password)
            if loginCustomer is not None:
                login(request,loginCustomer) 
                if  carid is not None:
                    return HttpResponseRedirect('/jobvalg/%s/' %carid)
                else:
                    return HttpResponseRedirect('/profil/')
            else:
                return render_to_response('login.html', {'form':form,'text':'Burgernavn og password passer ikke'},context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form':form},context_instance=RequestContext(request))
    else:
        form=LoginForm()
        return render_to_response('login.html',{'form':form}, context_instance=RequestContext(request))
    
def userLogout(request):
    logout(request)
    return HttpResponseRedirect("/")
    
@login_required
def profile(request):
    company=AO.objects.get(id=request.user.id)
    bid=Bid.objects.filter(ao=request.user.id)
    return render_to_response('profile.html',{'company':company, 'bid':bid},context_instance=RequestContext(request))


@login_required
def editProfile(request):
        ao=AO.objects.get(id=request.user.id)
#        area=Area.objects.get(area=ao.area)
#        print area.id
        print ao.area.id
        form=ChangeProfile(initial={'username':ao.username, 'company':ao.company, 'email':ao.email,
                                    'cvr':ao.cvr,'street':ao.street, 'postcode':ao.postcode,'city':ao.city, 'area':ao.area,
                                    'tlf':ao.tlf,'is_active':ao.is_active,'description':ao.description})
      
        if request.method=='POST':
            if form.is_valid():
                saveChange(ao, form)
                return render_to_response('editprofile.html',{'ao':ao, 'form':form,'text':'dit profil er blevet ændret'}, context_instance=RequestContext(request))            
            else:     
                return render_to_response('editprofile.html',{'ao':ao, 'form':form}, context_instance=RequestContext(request))             
        else:          
            return render_to_response('editprofile.html',{'ao':ao, 'form':form}, context_instance=RequestContext(request))
    
@login_required
def saveChange(ao, form):
    ao.username=form.cleaned_data['username']
    ao.company=form.cleaned_data['company'] 
    ao.email=form.cleaned_data['email']
    ao.cvr=form.cleaned_data['cvr']
    ao.street=form.cleaned_data['street']
    ao.postcode=form.cleaned_data['postcode']
    ao.city=form.cleaned_data['city']
    ao.area=form.cleaned_data['area']
    ao.tlf=form.cleaned_data['tlf']
    ao.is_active=form.cleaned_data['is_active']
    ao.description=form.cleaned_data['description']
    ao.save()
