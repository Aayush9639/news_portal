from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required

@login_required
@role_required(['advertiser'])
def advertiser_dashboard(request):
    return render(request, 'advertisements/advertiser_dashboard.html')