from django.shortcuts import render,redirect
from django.http import HttpResponse

from Consumer.models import Consumer,Membership




# Create your views here.



def home(request):
    return render(request, 'base.html')

def add_user(request):
    if request.method == 'POST':
        print(request.POST)  # Log all POST data to confirm what is being sent

        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        print(name, " ", gender, " ", age)  # Debug output

        # Ensure all fields are populated
        if not all([name, gender, age]):
            return HttpResponse("All fields are required.", status=400)

        # Save the data to the database
        Consumer.objects.create(name=name, age=age, gender=gender)
        return render(request, 'add_user.html')

    return render(request, 'add_user.html')


def list_user(request):
    users = Consumer.objects.all()
    return render(request, 'list_user.html', {'users': users})


def add_card(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        status = request.POST.get('status')
        consumer_id = request.POST.get('consumer')  # Get the consumer ID from the form

        # Ensure the consumer exists
        consumer = Consumer.objects.get(id=consumer_id)

        # Create and save the Membership object
        Membership.objects.create(number=number, status=status, consumer_id=consumer)

        return redirect('add_card')  # Redirect to another view after saving

    users = Consumer.objects.all()
    return render(request,'add_card.html',{'users': users})

def list_card(request):
    cards = Membership.objects.all()
    return render(request, 'list_card.html',{'cards': cards})


