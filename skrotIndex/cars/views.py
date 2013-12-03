# -*- coding: utf-8 -*-  
from cars.forms import CarForm, BidForm
from ao.models import Area, Bid, AO
from cars import models
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from cars.models import BidArea, Car
from datetime import datetime,timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import ao
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def skrot(request):
    if request.method=='POST':
        form=CarForm(request.POST,request.FILES )
        if form.is_valid():
            d=form.cleaned_data['duration']
            
            print d
            print 'here is the string of now '+str(d)
            print datetime.now()
            now =datetime.now() #datetime.now().strftime('%y-%m-%d %H:%M')
            end=datetime.now()+timedelta(days=int(d))
            print str(now)+"end time"+str(end)
            
            car=models.Car(plate=form.cleaned_data['plate'], year=form.cleaned_data['year'], brand=form.cleaned_data['brand'],
                           address=form.cleaned_data['address'],  city=form.cleaned_data['city'],pickup=form.cleaned_data['pickup'], email=form.cleaned_data['email'],
                           tlf=form.cleaned_data['tlf'], start_time=now, end_time=end, picture=form.cleaned_data['picture'], )           
            car.save() 
            for g in request.POST.getlist('bid_area'):
                ar=Area.objects.get(pk=g)
                bid_area_to_car=BidArea(car=car,area=ar)
                bid_area_to_car.save()
                
            print 'save the object'         
            return render_to_response('skrot.html', {'form':form,'text':'Du har nu regiteret din bil, den vil nu blive byde imod den højste pris'},context_instance=RequestContext(request))
        else:
            print 'invalid information'
            return render_to_response('skrot.html', {'form':form, 'text':"forkert indsatning,  indtaste bilens information igen"}, context_instance=RequestContext(request))
    else:
        form=CarForm() 
        print 'directly'
        return render_to_response('skrot.html', {'form':form, 'text': 'indtaste bilens information her.'}, context_instance=RequestContext(request))
    
def biler(request, area=None):
    
    if area is None:
        car_list=Car.objects.filter(end_time__gte =datetime.now())
        paginator = Paginator(car_list, 25)
    else:
        ar=Area.objects.get(area=area)
        car_list=Car.objects.filter(bid_area=ar,end_time__gte =datetime.now()).order_by('start_time') 
        paginator = Paginator(car_list, 25)
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

def bil(request,carid):
    car=Car.objects.get(pk=carid)
    bid=Bid.objects.filter(car=carid).order_by('price')
    if request.user.id is not None:        
        try:
            a=AO.objects.get(id=request.user.id)
        except a.DoesNotExist:
            return render_to_response('bil.html', {'car':car, 'text': 'Du kan ikke byde med din konto.'}, context_instance=RequestContext(request))
        if request.method=='POST':
            form=BidForm(request.POST , initial={'car':car} )
            if form.is_valid():
                b=ao.models.Bid(car=car,ao=a,price=form.cleaned_data['price'])
                b.save()
                return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form}, context_instance=RequestContext(request))
            else:
                print "havn't save the bid"
                return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form}, context_instance=RequestContext(request))
        else:
            form=BidForm(initial={'car':id} )
            return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form}, context_instance=RequestContext(request))    
    else:
        form=BidForm(initial={'car':id} )
        return render_to_response('bil.html', {'car':car,'bid':bid, 'form':form}, context_instance=RequestContext(request))
    
@login_required
def confirmDeleteBid(request,bidID):
    bid=Bid.objects.get(pk=bidID)
    return render_to_response('delete_bid_q.html', {'bid':bid}, context_instance=RequestContext(request))

@login_required
def deleteBid(request,bidID):
    userid=request.user.id
    bid=Bid.objects.get(pk=bidID)
    if userid==bid.ao_id:
        bid.delete()
        return redirect('ao.views.profile')
    else:
        html="<html><body>lad vær med det. det er forbudt.</body></html>"
        return HttpResponse(html)
        




