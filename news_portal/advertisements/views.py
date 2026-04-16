from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from .models import Advertisement
from .forms import AdvertisementForm


@login_required
@role_required(['advertiser'])
def advertiser_dashboard(request):
    ads = Advertisement.objects.filter(advertiser=request.user)

    return render(request, 'advertisements/dashboard.html', {
        'ads': ads
    })


@login_required
@role_required(['advertiser'])
def create_ad(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.advertiser = request.user
            ad.status = 'pending'
            ad.save()
            return redirect('advertiser_dashboard')
    else:
        form = AdvertisementForm()

    return render(request, 'advertisements/create_ad.html', {'form': form})


@login_required
@role_required(['advertiser'])
def edit_ad(request, id):
    ad = get_object_or_404(Advertisement, id=id, advertiser=request.user)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('advertiser_dashboard')
    else:
        form = AdvertisementForm(instance=ad)

    return render(request, 'advertisements/edit_ad.html', {'form': form})


@login_required
@role_required(['advertiser'])
def delete_ad(request, id):
    ad = get_object_or_404(Advertisement, id=id, advertiser=request.user)
    ad.delete()
    return redirect('advertiser_dashboard')