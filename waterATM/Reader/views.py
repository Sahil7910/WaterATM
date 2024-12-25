from django.shortcuts import render
from django.http import HttpResponse
from Reader.models import Configuration

from Site.models import Site


# Create your views here.

def add_reader(request):
    config = Configuration.objects.all()
    sites = Site.objects.all()
    context = {
        'config': config,
        'sites':sites
        }

    return render(request, 'add_reader.html',context)


def list_reader(request):
    return render(request, 'list_reader.html')


def add_config(request):

    if request.method == "POST":

        ip_address = request.POST.get('ipaddress')
        duration_for_1ltr=request.POST.get('1ltr')
        duration_for_2ltr = request.POST.get('2ltr')
        duration_for_3ltr = request.POST.get('3ltr')
        duration_for_5ltr=request.POST.get('5ltr')

        print(ip_address,"",duration_for_1ltr,"",duration_for_2ltr,"",duration_for_3ltr,"",duration_for_5ltr)

        if not all([ip_address,duration_for_1ltr,duration_for_2ltr,duration_for_3ltr,duration_for_5ltr]):
            return HttpResponse("All fields are required.", status=400)

        Configuration.objects.create(SERVER_IP=ip_address, DURATION_1LTR= duration_for_1ltr, DURATION_2LTR=duration_for_2ltr, DURATION_3LTR=duration_for_3ltr, DURATION_5LTR=duration_for_5ltr)

        return render(request, 'add_configuration.html')


    return render(request, 'add_configuration.html')

def list_config(request):

    config= Configuration.objects.all()

    context = {
        'config': config,
        'memberships': memberships,
    }

    return render(request, 'list_configuration.html',{'config':config})
