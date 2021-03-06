# -*- coding: utf-8 -*-  
from ao.models import AO, Area, Bid
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from ao.forms import RegiForm, LoginForm, ChangeProfile, Picture
from ao import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cars.models import Car
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from cars.forms import InactiveForm
from skrotIndex import settings
from django.core.mail.message import EmailMessage

def index(request):
    print datetime.now()   
    car=Car.objects.filter(end_time__gte =datetime.now()).order_by('start_time')[:2]  
    print car     
    return render_to_response('index.html',{'car':car}, context_instance=RequestContext(request))

def ao(request, area=None):

    if area is None:
        ao_list=AO.objects.filter( is_active=True).order_by('-last_login')
        paginator = Paginator(ao_list, 9)
    else:
        ar=Area.objects.get(area=area)
        ao_list=AO.objects.filter( area=ar, is_active=True).order_by('-last_login')
        paginator = Paginator(ao_list, 9) 
    page = request.GET.get('page')
    try:
        ao= paginator.page(page)
    except PageNotAnInteger:
        ao = paginator.page(1)
    except EmptyPage:
        ao = paginator.page(paginator.num_pages)           
    return render_to_response('ophugger.html', {'ao':ao, 'area':area}, context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():       # is a section tool
        return HttpResponseRedirect('/profil/')      
    if request.method=='POST': 
        form=RegiForm(request.POST )
        if form.is_valid():
            ar=Area.objects.get(area=form.cleaned_data['area'])
            ao=models.AO(username=form.cleaned_data['email'],company=form.cleaned_data['company'], email=form.cleaned_data['email'], description=form.cleaned_data['description'],
                           cvr=form.cleaned_data['cvr'],  street=form.cleaned_data['street'], postcode=form.cleaned_data['postcode'],
                           city=form.cleaned_data['city'], area=form.cleaned_data['area'], tlf=form.cleaned_data['tlf'], web=form.cleaned_data['web'],is_active=False, is_superuser=False)
            ao.set_password( form.cleaned_data['password'])    
                  
            ao.save()
            loginForm=LoginForm()           
            return render_to_response('login.html',{'form':loginForm,'text':'Registrering færdig. Du vil hurtigst muligt modtage en email, efter din registrering er blevet godkendt.'},context_instance=RequestContext(request))
        else:
            return render_to_response('register.html', {'form':form, 'text':'Forkert indtastning, prøv igen'}, context_instance=RequestContext(request))
    else:
        form=RegiForm() 
        return render_to_response('register.html', {'form':form,'text': 'Indtast din information for at blive registreret'}, context_instance=RequestContext(request))
    
def userLogin(request, slug=None): 
                                        
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profil/')
    if request.method=='POST':
        form=LoginForm(request.POST )
        if form.is_valid():   
            username= form.cleaned_data['username']
            password=form.cleaned_data['password' ]
            loginCustomer=authenticate(username=username,password=password)
            if loginCustomer is not None:
                if loginCustomer.is_staff:
                    return render_to_response('login.html', {'form':form,'text':'Administration skal logge ind på en anden side'},context_instance=RequestContext(request))
                else:
                    login(request,loginCustomer)
                    if not request.POST.get('husk', None):    # none is the defualt return value here
                        request.session.set_expiry(0)
                    if  slug is not None:
                        return HttpResponseRedirect('/bil/%s/' %slug)
                    else:
                        return HttpResponseRedirect('/profil/')
            else:
                return render_to_response('login.html', {'form':form,'text':'Enten brugernavn eller password er ikke korrekt'},context_instance=RequestContext(request))
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
                                    'tlf':ao.tlf,'web':ao.web,'description':ao.description}, existed_email=ao.email)
            if form.is_valid():
                print "in is_valid"
                saveChange(ao, form)
                return render_to_response('editprofile.html',{'ao':ao, 'form':form,'text':'Din profil er blevet ændret'}, context_instance=RequestContext(request))            
            else: 
                print "not valid"    
                return render_to_response('editprofile.html',{'ao':ao, 'form':form}, context_instance=RequestContext(request))             
        else: 
            print" not post" 
            form=ChangeProfile(initial={'company':ao.company, 'email':ao.email,
                                    'cvr':ao.cvr,'street':ao.street, 'postcode':ao.postcode,'city':ao.city, 'area':ao.area,
                                    'tlf':ao.tlf,'web':ao.web,'description':ao.description},existed_email=ao.email)        
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
    ao=AO.objects.get(slug=id)
    return render_to_response('single_ao.html',{'ao':ao}, context_instance=RequestContext(request))

@login_required    
def editPic(request):
        ao=AO.objects.get(pk=request.user.id)
        if request.method=='POST':
            form=Picture(request.POST,request.FILES)
            if form.is_valid():
                pic=form.cleaned_data['picture']
                print pic
                if pic is not None:
                    if 'change' in request.POST:
                        print " we are in change picture now"
                        if not ao.picture:                 # if not return true  with empty string and value 0, if ..is not none check null value.  
                            ao.picture.save(ao.slug+'.jpg',form.cleaned_data['picture'],save=True)
                        else: 
                            ao.picture.delete()
                            ao.picture.save(ao.slug+'.jpg',form.cleaned_data['picture'],save=True)
                        return render_to_response('editpic.html', {'form':form,'ao':ao,'text':'Dit profil billede er ændret'}, context_instance=RequestContext(request))
                        
                    elif 'delete' in request.POST:
                        if not ao.picture:
                            print "do nothing"
                        else:
                            print " we are in delete pciture now"
                            ao.picture.delete()
                        return render_to_response('editpic.html', {'form':form,'ao':ao, 'text':'Dit profil billede er slettet'}, context_instance=RequestContext(request))
                else:
                    return render_to_response('editpic.html', {'form':form,'ao':ao,'text':' Du har endnu ikke uploadet et billede'}, context_instance=RequestContext(request))
            else:
                return render_to_response('editpic.html', {'form':form,'ao':ao}, context_instance=RequestContext(request))
        else:
            form=Picture() 
            return render_to_response('editpic.html', {'form':form,'ao':ao}, context_instance=RequestContext(request))
        
@login_required
def willDeleteProfile(request):
    if request.method=='POST':
        form=InactiveForm(request.POST)
        if form.is_valid():
            id=request.user.id
            message="Bruger med ID "+str(id)+",vil inaktivere sin profil "
            mail= EmailMessage("Inaktiverer profit",message, to=[settings.DEFAULT_FROM_EMAIL])
            mail.send()
            return render_to_response('delete_profile_q.html', {'form':form, 'text':"Din anmodning er sendt, vi vil inaktivere din profil hurtigst mugligt!"}, context_instance=RequestContext(request))
        else:
            return render_to_response('delete_profile_q.html', {'form':form, 'text':"Udfyld form"}, context_instance=RequestContext(request))
    else:
        form=InactiveForm() 
    return render_to_response('delete_profile_q.html', {'id':request.user.id, 'form':form}, context_instance=RequestContext(request))

@login_required
def deleteProfile(request):
        ao=AO.objects.get(pk=request.user.id)
        ao.picture.delete()
        ao.delete()
        logout(request)
        return HttpResponseRedirect("/")


    