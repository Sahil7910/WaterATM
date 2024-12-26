from django.shortcuts import render

from Transaction.models import Transaction,Quota




# Create your views here.


def add_quota(request):

    if request.method == 'POST':
        gender = request.POST.get('gender')
        daily_quota = request.POST.get('quota')
        active_date = request.POST.get('active_date')
        status = request.POST.get('status')

        print(gender,"",daily_quota,"",active_date,"",status)

        Quota.objects.create(Gender=gender, DAILY_QUOTA=daily_quota, ACTIVE_DATE=active_date, Status=status)

    return render(request, 'add_quota.html')


def list_quota(request):
    quota= Quota.objects.all()
    return render(request, 'list_quota.html',{'quota': quota})

def list_transaction(request):

    transaction=Transaction.objects.all()
    return render(request,'list_transaction.html',{'transaction':transaction})
