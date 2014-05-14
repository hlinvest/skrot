# -*- coding: utf-8 -*- 
from django.core.management.base import BaseCommand, CommandError
from ao.models import Bid
from datetime import datetime
from cars.models import SoldCar, Car, highest_bid
from django.core.mail import send_mail
from skrotIndex import settings








class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        print " cron works fine"
        car=Car.objects.filter(end_time__lte=datetime.now())[0:1]
        if car is not None:
           
            for a in car:
                print a.brand+a.plate+str(a.id)
                sc=SoldCar(id=a.id,plate=a.plate,stelNum=a.steNum,year=a.year,brand=a.brand,address=a.address,city=a.city,pickup=a.pickup,email=a.email,tlf=a.tlf,
                           start_time=a.start_time,end_time=a.end_time,picture=a.picture)
                print str(a.id)+str(a.plate)+str(a.brand)
                sc.save()
                bid=Bid.objects.filter(car=a.id).order_by('price')[:3]
                if not bid:
                    print "Der er ingen bud"
                    send_mail('Der er ingen bud på din bil', 'Auktionen er slut, og der var desværre ingen bud. Prøv igen.',  settings.DEFAULT_FROM_EMAIL,
                    [a.email], fail_silently=False)
                else:
                    self.sendEmailToAO(bid[0])
                    self.sendEmailToSeller(bid)
                    self.moveBid(bid)
                print a
                a.delete()
                        
    def moveBid(self,bid):
        for b in bid:
            print str(b.id)+str(b.car)+str(b.ao)+str(b.price)
            hb=highest_bid(carID=b.car,bider=b.ao,price=b.price)
            hb.save()
            b.delete()
            
    def sendEmailToSeller(self, bid): 
            print bid[0].car.email
            print " Send email til sælger" 
            self.emailMessegeToSeller(bid) 
            
    def sendEmailToAO(self,vbid):
        print" Send email til AO"+vbid.ao.email
        st='Du har vundet auktionen med %s ,årgang: %s, pris: %s \n' %( vbid.car.brand,str(vbid.car.year),str(vbid.price))
        st+='Ejeren kan kontaktes på email: %s og telefon: %s.' %(vbid.car.email,vbid.car.tlf)
        send_mail('Tillykke! Du har vundet denne auktion', st,  settings.DEFAULT_FROM_EMAIL,
                      [vbid.ao.email], fail_silently=False)
    
    def emailMessegeToSeller(self, bid):
        carEmail=bid[0].car.email
        st='Der er blevet budt %s gang/gange, her er de tre højeste bud( hvis der er 3, eller over): \n' % (str(bid.count()))
        for b in bid:
            st+=' Fra %s, pris: %s, email %s, telefon: %s \n'  % (b.ao.company, str(b.price),b.ao.email, str(b.ao.tlf))
        send_mail('Der er budt på din bil', st, settings.DEFAULT_FROM_EMAIL ,  [carEmail], fail_silently=False)
            
#email with template, delete every auction that is more than 14 days. create link of aucton to emails. 
        
         


#
#if __name__ == '__main__':
#    mc=MyCronJob()
#    mc.do()