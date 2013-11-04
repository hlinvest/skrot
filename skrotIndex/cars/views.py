# -*- coding: utf-8 -*-  
from cars.forms import CarForm
from ao.models import Area, Bid
from cars import models
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cars.models import BidArea, Car
from datetime import datetime,timedelta

def skrot(request):
    if request.method=='POST':
        form=CarForm(request.POST )
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
            return render_to_response('skrot.html', {'form':form, 'text':"prøv at indtaste din virksomhedens information igen"}, context_instance=RequestContext(request))
    else:
        form=CarForm() 
        print 'directly'
        return render_to_response('skrot.html', {'form':form, 'text': 'indtaste bilens information her.'}, context_instance=RequestContext(request))
    
def biler(request, area=None):
    if area is None:
        car=Car.objects.all()
    else:
        ar=Area.objects.get(area=area)
        car=Car.objects.filter( area=ar).order_by('start_time')     
#    paginator=Paginator(jobs, 2)
#    page=request.GET.get('page')
#    try:
        
    return render_to_response('skrot_biler.html', {'car':car, 'area':area}, context_instance=RequestContext(request))

def bil(request,id):
    car=Car.objects.get(pk=id)
    bid=Bid.objects.filter(car=id).order_by('end_time')
    return render_to_response('bil.html', {'car':car,'bid':bid}, context_instance=RequestContext(request))

