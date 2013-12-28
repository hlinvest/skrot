# -*- coding: utf-8 -*-  
from ao.models import AO, Area, Bid
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from ao.forms import RegiForm, LoginForm, ChangeProfile, Picture
from ao import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def ao(request, area=None):

    if area is None:
        ao=AO.objects.filter( is_active=True)
    else:
        ar=Area.objects.get(area=area)
        ao=AO.objects.filter( area=ar, is_active=True)            
    return render_to_response('ophugger.html', {'ao':ao, 'area':area}, context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():       # is a section tool
        return HttpResponseRedirect('/profile/')      
    if request.method=='POST': 
        form=RegiForm(request.POST )
        if form.is_valid():
            ar=Area.objects.get(area=form.cleaned_data['area'])
            ao=models.AO(username=form.cleaned_data['username'],company=form.cleaned_data['company'], email=form.cleaned_data['email'], description=form.cleaned_data['description'],
                           cvr=form.cleaned_data['cvr'],  street=form.cleaned_data['street'], postcode=form.cleaned_data['postcode'],
                           city=form.cleaned_data['city'], area=form.cleaned_data['area'], tlf=form.cleaned_data['tlf'], web=form.cleaned_data['web'],is_active=True, is_superuser=False)
            ao.set_password( form.cleaned_data['password'])    
                  
            ao.save()
            loginForm=LoginForm()           
            return render_to_response('login.html',{'form':loginForm,'text':'færdig med at registere, du kan nu logge in'},context_instance=RequestContext(request))
        else:
            return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form=RegiForm() 
        return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    
def userLogin(request, carid=None): 
                                        
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
                    return HttpResponseRedirect('/bil/%s/' %carid)
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
      
        if request.method=='POST':
            form=ChangeProfile(request.POST,initial={'company':ao.company, 'email':ao.email,
                                    'cvr':ao.cvr,'street':ao.street, 'postcode':ao.postcode,'city':ao.city, 'area':ao.area,
                                    'tlf':ao.tlf,'is_active':ao.is_active,'description':ao.description}, existed_email=ao.email)
            if form.is_valid():
                print "in is_valid"
                saveChange(ao, form)
                return render_to_response('editprofile.html',{'ao':ao, 'form':form,'text':'dit profil er blevet ændret'}, context_instance=RequestContext(request))            
            else: 
                print "not valid"    
                return render_to_response('editprofile.html',{'ao':ao, 'form':form}, context_instance=RequestContext(request))             
        else: 
            print" not post" 
            form=ChangeProfile(initial={'company':ao.company, 'email':ao.email,
                                    'cvr':ao.cvr,'street':ao.street, 'postcode':ao.postcode,'city':ao.city, 'area':ao.area,
                                    'tlf':ao.tlf,'is_active':ao.is_active,'description':ao.description},existed_email=ao.email)        
            return render_to_response('editprofile.html',{'ao':ao, 'form':form}, context_instance=RequestContext(request))
    

def saveChange(ao, form):
    ao.company=form.cleaned_data['company'] 
    ao.email=form.cleaned_data['email']
    ao.cvr=form.cleaned_data['cvr']
    ao.street=form.cleaned_data['street']
    ao.postcode=form.cleaned_data['postcode']
    ao.city=form.cleaned_data['city']
    ao.area=form.cleaned_data['area']
    ao.tlf=form.cleaned_data['tlf']
    ao.is_active=form.cleaned_data['is_active']
    ao.web=form.cleaned_data['web']
    ao.description=form.cleaned_data['description']
    ao.save()
    
def ophugger(request, id):
    ao=AO.objects.get(pk=id)
    return render_to_response('single_ao.html',{'ao':ao}, context_instance=RequestContext(request))

@login_required    
def editPic(request):
        ao=AO.objects.get(pk=request.user.id)
        if request.method=='POST':
            form=Picture(request.POST,request.FILES)
            if form.is_valid():
                if 'change' in request.POST:
                    print " we are in change picture now"
                    if not ao.picture:                 # if not return true  with empty string and value 0, if ..is not none check null value.  
                        ao.picture=form.cleaned_data['picture']
                        ao.save()  
                    else: 
                        ao.picture.delete()
                        ao.picture=form.cleaned_data['picture']
                        ao.save()
                    return render_to_response('editpic.html', {'form':form,'ao':ao,'text':'dit nyt profil billede er ændret/tilføj'}, context_instance=RequestContext(request))
                    
                elif 'delete' in request.POST:
                    if not ao.picture:
                        print "do nothing"
                    else:
                        print " we are in delete pciture now"
                        ao.picture.delete()
                    return render_to_response('editpic.html', {'form':form,'ao':ao, 'text':'dit profil billede er slettet'}, context_instance=RequestContext(request))
            else:
                return render_to_response('editpic.html', {'form':form,'ao':ao}, context_instance=RequestContext(request))
        else:
            form=Picture() 
            return render_to_response('editpic.html', {'form':form,'ao':ao}, context_instance=RequestContext(request))
        
@login_required
def willDeleteProfile(request):
    return render_to_response('delete_profile_q.html', {'id':request.user.id}, context_instance=RequestContext(request))

@login_required
def deleteProfile(request):
    ao=AO.objects.get(pk=request.user.id)
    ao.picture.delete()
    ao.delete()
    logout(request)
    return HttpResponseRedirect("/")

    