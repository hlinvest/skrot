# -*- coding: utf-8 -*-  
from django_cron import CronJobBase, Schedule    # add the path to PYTHONPATH after install django_cron with pip , https://pypi.python.org/pypi/django-cron/
from ao.models import Bid
from datetime import datetime
from cars.models import SoldCar, Car, highest_bid
from django.core.mail import send_mail
from skrotIndex import settings





class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every minute
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cars.my_cron_job' 
    
    
    
    def do(self):
        print " cron works fine"
        car=Car.objects.filter(end_time__lte=datetime.now())[0:1]
        if car is not None:
            print "car is not none"
            for a in car:
                print a.brand+a.plate+str(a.id)
                sc=SoldCar(id=a.id,plate=a.plate,year=a.year,brand=a.brand,address=a.address,city=a.city,pickup=a.pickup,email=a.email,tlf=a.tlf,
                           start_time=a.start_time,end_time=a.end_time,picture=a.picture)
                print str(a.id)+str(a.plate)+str(a.brand)
                sc.save()
                bid=Bid.objects.filter(car=a.id).order_by('price')[:3]
                if not bid[0]:
                    print "der er ingen byd"
                    send_mail('Der blev ikke bydet noget pris på din bil', 'Der blevet ikke noget byde på din bil.', settings.DEFAULT_FROM_EMAIL ,
                    [a.email], fail_silently=False)
                else:
                    self.sendEmailToAO(bid[0])
                    self.sendEmailToSeller(bid)
                    self.moveBid(bid)
                
                a.delete()
                        
    def moveBid(self,bid):
        for b in bid:
            print str(b.id)+str(b.car)+str(b.ao)+str(b.price)
            hb=highest_bid(carID=b.car,bider=b.ao,price=b.price)
            hb.save()
            b.delete()
            
    def sendEmailToSeller(self, bid): 
            print bid[0].car.email
            print " send email til sælger" 
            self.emailMessegeToSeller(bid) 
            
    def sendEmailToAO(self,vbid):
        print" send email til AO"+vbid.ao.email
        st='Du har vundet auktion med %s ,årgang: %s, pris: %s \n' %( vbid.car.brand,str(vbid.car.year),str(vbid.price))
        st+='Ejern kan kontaktes med email: %s og telefon: %s.' %(vbid.car.email,vbid.car.tlf)
        send_mail('Tillykke! Du har vundet den auktion', st, settings.DEFAULT_FROM_EMAIL ,
                      [vbid.ao.email], fail_silently=False)
    
    def emailMessegeToSeller(self, bid):
        carEmail=bid[0].car.email
        st='der er blevet bydet %s gang/gange, det vil vise tre højeste byder( vis der er 3 eller over): \n' % (str(bid.count()))
        for b in bid:
            st+=' fra %s, price: %s, email %s, telephone: %s \n'  % (b.ao.company, str(b.price),b.ao.email, str(b.ao.tlf))
        send_mail('der er byd på din bil', st, settings.DEFAULT_FROM_EMAIL ,  [carEmail], fail_silently=False)
            
#email with template, delete every auction that is more than 14 days. create link of aucton to emails. 
        
         



if __name__ == '__main__':
    mc=MyCronJob()
    mc.do()