# -*- coding: utf-8 -*-  
from cars.forms import CarForm, BidForm, ContactForm
from ao.models import Area, Bid, AO
from cars import models
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from cars.models import BidArea, Car, SoldCar, highest_bid
from datetime import datetime,timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import ao
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from skrotIndex import settings
from django.core.mail.message import EmailMessage
import getCarData
from django.utils import timezone



def skrot(request):
    if request.method=='POST':
        if 'findCarData' in request.POST:
            plade=request.POST.get('numField')
            stel=request.POST.get('stelField')
            print str(plade)+str(stel)
            if plade:
                data=getCarData.getCarDataByPlateOrStel(plate=plade)
                if data is not None:
                    num_data=data['Registreringsnr:']
                    stel_data=data['Stelnummer:']
                    art_data=data['Art:']
                    year_data=data[u'F\xf8rste Registreringsdato:']
                    brand_data=data[u'M\xe6rke:']
                    form=CarForm(initial={'plate':num_data, 'stelNum':stel_data,'art':art_data,'year':year_data, 'brand':brand_data})
                    return render_to_response('skrot.html', {'form':form, 'text': 'Du kan også indtaste bilens oplysninger manuelt her'}, context_instance=RequestContext(request))
                else: 
                    form=CarForm()
                    return render_to_response('skrot.html', {'form':form, 'text': 'Du kan også indtaste bilens oplysninger manuelt her','errorsText':'Kan ikke finde bilen med denne nummerplade'}, context_instance=RequestContext(request))  
            elif stel:
                data=getCarData.getCarDataByPlateOrStel(stel=stel)
                if data is not None:
                    num_data=data['Registreringsnr:']
                    stel_data=data['Stelnummer:']
                    art_data=data['Art:']
                    year_data=data[u'F\xf8rste Registreringsdato:']
                    brand_data=data[u'M\xe6rke:']
                    form=CarForm(initial={'plate':num_data, 'stelNum':stel_data,'art':art_data,'year':year_data, 'brand':brand_data})
                    return render_to_response('skrot.html', {'form':form, 'text': 'Du kan også indtaste bilens oplysninger manuelt her'}, context_instance=RequestContext(request))
                else: 
                    form=CarForm()
                    return render_to_response('skrot.html', {'form':form, 'text': 'Du kan også indtaste bilens oplysninger manuelt her','errorsText':'Kan ikke finde bilen med dette stelnummer'}, context_instance=RequestContext(request))   
            else:
                form=CarForm()
                return render_to_response('skrot.html', {'form':form, 'text': 'Du kan også indtaste bilens oplysninger manuelt her', 'errorsText':'Mangler at indtaste bilens nummerplade eller stelnummer'}, context_instance=RequestContext(request))   
                
                
                
#            html="<html><body>Lad vær med det. Det er forbudt.</body></html>"
#            return HttpResponse(html) 
        else:
            form=CarForm(request.POST,request.FILES )
            if form.is_valid():
                d=form.cleaned_data['duration']
                now = datetime.now() #datetime.now().strftime('%y-%m-%d %H:%M')
                end=now+timedelta(days=int(d))
                
                car=models.Car(plate=form.cleaned_data['plate'], year=form.cleaned_data['year'], brand=form.cleaned_data['brand'],
                               address=form.cleaned_data['address'],  city=form.cleaned_data['city'],pickup=form.cleaned_data['pickup'], email=form.cleaned_data['email'],
                               tlf=form.cleaned_data['tlf'], start_time=now, end_time=end, picture=form.cleaned_data['picture'], )         
                car.save()
    #            car.picture.save(car.plate,form.cleaned_data['picture'],save=True )  
                aos=[]
                for g in request.POST.getlist('bid_area'):
                    ar=Area.objects.get(pk=g)
                    bid_area_to_car=BidArea(car=car,area=ar)
                    bid_area_to_car.save()
                    ao_from_one_area=AO.objects.filter(area=ar)
                    aos.append( ao_from_one_area)
                new_car_email(car,aos)
                             
                return render_to_response('skrot.html', {'form':form,'text':'Du har nu registreret din bil i vores database, og den er nu klar til at blive budt på.'},context_instance=RequestContext(request))
            else:
                return render_to_response('skrot.html', {'form':form, 'text':"Forkert indtastning, indtast bilens oplysninger igen"}, context_instance=RequestContext(request))
    else:
        form=CarForm() 
        return render_to_response('skrot.html', {'form':form, 'text': 'Du kan også indtaste bilens oplysninger manuelt her'}, context_instance=RequestContext(request))
    
def biler(request, area=None):
    
    if area is None:
        car_list=Car.objects.filter(end_time__gte =datetime.now())
        paginator = Paginator(car_list, 20)
    else:
        ar=Area.objects.get(area=area)
        car_list=Car.objects.filter(bid_area=ar,end_time__gte =datetime.now()).order_by('start_time') 
        paginator = Paginator(car_list, 20)
    page = request.GET.get('page')
    try:
        car= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)

    return render_to_response('skrot_biler.html', {'car':car, 'area':area}, context_instance=RequestContext(request))

def bil(request,slug):
    car=Car.objects.get(slug=slug)
    bid=Bid.objects.filter(car=car).order_by('price')
    now = timezone.now()
    if car.end_time<now:
        expired=True
    else:
        expired=False
        print str(expired)+"inside else"
    if expired:
        return render_to_response('bil.html', {'car':car,'bid':bid, 'expired':expired}, context_instance=RequestContext(request))
    else:
        if request.user.id is not None:        
            try:
                a=AO.objects.get(id=request.user.id)
            except a.DoesNotExist:
                return render_to_response('bil.html', {'car':car, 'text': 'Du kan ikke byde med din konto.'}, context_instance=RequestContext(request))
            if request.method=='POST':
                form=BidForm(request.POST , initial={'car':car.id} )
                if form.is_valid():
                    b=ao.models.Bid(car=car,ao=a,price=form.cleaned_data['price'])
                    b.save()
                    bid_no=Bid.objects.filter(car=car)
                    if bid_no.exists() :
                        print bid_no
                        pass
                    else:
                        second_email=[Bid.objects.filter(car=car)[1].ao.email]
                        print second_email
                        if not second_email:
                            pass
                        else:
                            message= " Der er kommet et bud, som er højere end dit. Hvis du vil byde igen, så klik på linket eller indsæt det i din browser "+settings.SITE_DOMAIN+"bil/%s" %(slug)                    
                            send_mail("Du er blevet overbudt",message, settings.DEFAULT_FROM_EMAIL, second_email,fail_silently=False)
                    new_bid=Bid.objects.filter(car=car).order_by('price')
                    return render_to_response('bil.html', {'car':car,'bid':new_bid, 'form':form, 'expired':expired}, context_instance=RequestContext(request))
                else:
                    print "havn't save the bid"
                    return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form,'expired':expired}, context_instance=RequestContext(request))
            else:
                form=BidForm(initial={'car':car.id} )
                return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form, 'expired':expired}, context_instance=RequestContext(request))    
        else:
            form=BidForm(initial={'car':car.id} )
            return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form}, context_instance=RequestContext(request))
    
#@login_required  doesn't required it in boostrap version
#def confirmDeleteBid(request,bidID):
#    bid=Bid.objects.get(pk=bidID)
#    return render_to_response('delete_bid_q.html', {'bid':bid}, context_instance=RequestContext(request))

@login_required
def deleteBid(request,bidID):
    userid=request.user.id
    bid=Bid.objects.get(pk=bidID)
    if userid==bid.ao_id:
        bid.delete()
        return redirect('ao.views.profile')
    else:
        html="<html><body>Lad vær med det. Det er forbudt.</body></html>"
        return HttpResponse(html)
        

def expiredCar(request, carID):
    car=SoldCar.objects.get(pk=carID)
    bid=highest_bid.objects.filter(carID=carID)
    return  render_to_response('expired_car.html', {'car':car,'bid':bid}, context_instance=RequestContext(request))

def new_car_email(car, aos):
    ao_list=[]
    for ao in aos:
        print ao
        for a in ao:
            print a.email
            ao_list.append(a.email)
    print ao_list
        
    message="Hej \n"+"Ny bil på auktion: "+ car.brand+" , fra "+str(car.year)+"Click på linken "+settings.SITE_DOMAIN+"bil/"+car.slug 
    email = EmailMessage("Der blev lagt en ny bil på siden",message, settings.DEFAULT_FROM_EMAIL,[],ao_list)
    email.send(fail_silently=False)

def contactUs(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            body=form.cleaned_data['body']
            print name+email+body
            return render_to_response('contact.html', {'form':form, 'text':"Dit spørgsmål er sendt, vi vil svare dig hurtigst mugligt!"}, context_instance=RequestContext(request))
        else:
            return render_to_response('contact.html', {'form':form, 'text':"Forkert indtastning"}, context_instance=RequestContext(request))
    else:
        form=ContactForm() 
        return render_to_response('contact.html', {'form':form}, context_instance=RequestContext(request))
    
    
