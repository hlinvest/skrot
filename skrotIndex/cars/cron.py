from django_cron import CronJobBase, Schedule    # add the path to PYTHONPATH after install django_cron with pip , https://pypi.python.org/pypi/django-cron/
from ao.models import Bid
from datetime import datetime
from cars.models import SoldCar, Car, highest_bid

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every hours
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cars.my_cron_job' 
    
    def do(self):
        print " cron works fine"
        car=Car.objects.filter(end_time__lte=datetime.now())[0:1]
        if car is not None:
            for a in car:
                sc=SoldCar(id=a.id,plate=a.plate,year=a.year,brand=a.brand,address=a.address,city=a.city,pickup=a.pickup,email=a.email,tlf=a.tlf,start_time=a.start_time,end_time=a.end_time)
                print str(a.id)+str(a.plate)+str(a.brand)
                sc.save()
                a.delete()
                bid=Bid.objects.filter(car=a.id).order_by('price')[:3]
                if bid is not None:
                    for b in bid:
                        print str(b.id)+str(b.car)+str(b.ao)+str(b.price)
                        hb=highest_bid(carid=b.car,bider=b.ao,price=b.price)
                        hb.save()
#                    