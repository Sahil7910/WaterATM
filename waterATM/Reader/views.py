from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from Reader.models import Configuration,Reader
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Consumer.models import Membership
from Site.models import Site



# Create your views here.

def add_reader(request):
    config = Configuration.objects.all()
    sites = Site.objects.all()
    context = {
        'config': config,
        'sites':sites
        }
    if request.method == 'POST':
        position= request.POST.get('position')
        mac = request.POST.get('mac')
        installDate= request.POST.get('idate')
        Status = request.POST.get('status')
        config_id = request.POST.get('Config')
        site_id = request.POST.get('sites')

        configuration = get_object_or_404(Configuration, id=config_id)
        sites = get_object_or_404(Site, id=site_id)

        Reader.objects.create(position=position, mac=mac, install_date=installDate, status=Status, config=configuration, site=sites)

    return render(request, 'add_reader.html',context)


@csrf_exempt
@require_http_methods(["POST"])
def keep_live(request):

    mac_id = request.GET.get('macid')

    if not mac_id:
        return JsonResponse({'error': 'MAC ID is required.'}, status=400)

    try:

        reader = get_object_or_404(Reader, mac=mac_id)


        reader.last_seen_timestamp = now()
        reader.save()


        return JsonResponse({'success': True, 'message': 'Last seen timestamp updated.'}, status=200)
    except Reader.DoesNotExist:
        return JsonResponse({'error': 'Reader not found.'}, status=404)




def list_reader(request):
    reader = Reader.objects.all()
    return render(request, 'list_reader.html', {'reader': reader})


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
    memberships=Membership.objects.all()

    context = {
        'config': config,
        'memberships': memberships,
    }

    return render(request, 'list_configuration.html',{'config':config})


