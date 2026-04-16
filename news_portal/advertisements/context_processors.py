from .models import Advertisement

def ads_processor(request):
    ads = Advertisement.objects.filter(status='approved').order_by('?')[:5]
    return {'ads': ads}