from django.contrib import admin
from cars.models import Car, SoldCar
class CarAdmin(admin.ModelAdmin):
    date_hierarchy='end_time'
    search_fields=['plate','brand']
    list_display = ['id', 'plate', 'brand','end_time' ]
    
  
admin.site.register(Car, CarAdmin)
admin.site.register(SoldCar ,CarAdmin)
