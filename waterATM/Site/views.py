from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib import messages

from Site.models import Site
# Create your views here.


def add_site(request):

    if request.method == 'POST':
        print(request.POST)

        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')

        print(name, " ", address, " ", city,"", country)

        # Ensure all fields are populated
        if not all([name, address, city, country]):
            return HttpResponse("All fields are required.", status=400)

        # Save the data to the database
        Site.objects.create(Name=name, Address=address, City=city, Country=country)
        return render(request, 'add_site.html')

    return render(request, 'add_site.html')



def list_sites(request):
    sites = Site.objects.all()
    return render(request, 'list_sites.html', {'sites': sites})

def delete_site(request, site_id):
    if request.method == 'POST':
        site = get_object_or_404(Site, id=site_id)
        site.delete()
        messages.success(request, 'Site deleted successfully.')
    return redirect('list_sites')

