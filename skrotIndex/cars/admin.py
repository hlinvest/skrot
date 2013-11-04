from django.contrib import admin
from cars.models import Car, SoldCar
class CarAdmin(admin.ModelAdmin):
    date_hierarchy='end_time'
    search_field='plate','brand'
    
  
admin.site.register(Car, CarAdmin)
admin.site.register(SoldCar ,CarAdmin)
