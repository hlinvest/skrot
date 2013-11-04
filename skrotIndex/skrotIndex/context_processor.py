from ao.models import Area
def all_areas(request):
    all_areas=Area.objects.all()
    return {'all_areas':all_areas}