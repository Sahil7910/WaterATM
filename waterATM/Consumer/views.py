from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Sum
from Consumer.models import Consumer,Membership
from Reader.models import Reader
from Transaction.models import Quota,Transaction


def home(request):
    return render(request, 'base.html')

def add_user(request):
    if request.method == 'POST':
        print(request.POST)

        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        print(name, " ", gender, " ", age)


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
        consumer_id = request.POST.get('consumer')


        consumer = Consumer.objects.get(id=consumer_id)


        Membership.objects.create(number=number, status=status, consumer_id=consumer)

        return redirect('add_card')

    users = Consumer.objects.all()
    return render(request,'add_card.html',{'users': users})

def list_card(request):
    cards = Membership.objects.all()
    return render(request, 'list_card.html',{'cards': cards})


@csrf_exempt
@require_http_methods(["POST"])
def authorize_transaction(request):
    # Get query parameters
    card_number = request.GET.get('card')
    reader_id = request.GET.get('reader')
    quantity = request.GET.get('qty')

    print(card_number, reader_id, quantity)

    # Validate card and reader
    try:
        card = Membership.objects.get(number=card_number)
        reader = Reader.objects.get(mac=reader_id)
    except Membership.DoesNotExist:
        return JsonResponse({'error': 'Invalid card number.'}, status=404)
    except Reader.DoesNotExist:
        return JsonResponse({'error': 'Invalid reader ID.'}, status=404)


    consumer = card.consumer_id
    try:
        quota = Quota.objects.get(Gender=consumer.gender, Status=1)
    except Quota.DoesNotExist:
        return JsonResponse({'error': 'Quota not found for the specified gender.'}, status=404)


    try:
        consumed_qty = int(quantity)
        daily_quota = int(quota.DAILY_QUOTA)
    except ValueError:
        return JsonResponse({'error': 'Invalid quantity or quota.'}, status=400)

    # Calculate total consumed quantity for the day
    today = date.today()
    total_consumed_today = Transaction.objects.filter(
        MEMBERSHIP_ID=card,
        Txn_DateTime__date=today
    ).aggregate(Sum('CONSUMED_QTY'))['CONSUMED_QTY__sum'] or 0

    if (total_consumed_today + consumed_qty) > daily_quota:
        return JsonResponse({'error': 'Insufficient quota for the day.'}, status=400)

    balance_qty = daily_quota - (total_consumed_today + consumed_qty)


    transaction = Transaction.objects.create(
        CONSUMED_QTY=consumed_qty,
        BALANCE_QTY=balance_qty,
        MEMBERSHIP_ID=card,
        READER_ID=reader
    )


    return JsonResponse({
        'success': True,
        'message': 'Transaction authorized.',
        'txn_id': transaction.id,
        'dispense_duration_in_sec': consumed_qty * 1
    }, status=200)
# def authorize_transaction(request):
#     # Get query parameters
#     card_number = request.GET.get('card')  # Adjust to POST
#     reader_id = request.GET.get('reader')  # Adjust to POST
#     quantity = request.GET.get('qty')  # Adjust to POST
#
#     print(card_number, reader_id, quantity)
#
#     # Validate card and reader
#     try:
#         card = Membership.objects.get(number=card_number)
#         reader = Reader.objects.get(mac=reader_id)
#     except Membership.DoesNotExist:
#         return JsonResponse({'error': 'Invalid card number.'}, status=404)
#     except Reader.DoesNotExist:
#         return JsonResponse({'error': 'Invalid reader ID.'}, status=404)
#
#     # Fetch consumer and related quota
#     consumer = card.consumer_id
#     try:
#         quota = Quota.objects.get(Gender=consumer.gender, Status=1)
#     except Quota.DoesNotExist:
#         return JsonResponse({'error': 'Quota not found for the specified gender.'}, status=404)
#
#     # Validate and calculate quantities
#     try:
#         consumed_qty = int(quantity)  # Convert quantity to integer
#         daily_quota = int(quota.DAILY_QUOTA)  # Ensure DAILY_QUOTA is an integer
#     except ValueError:
#         return JsonResponse({'error': 'Invalid quantity or quota.'}, status=400)
#
#     balance_qty = daily_quota - consumed_qty
#     if balance_qty < 0:
#         return JsonResponse({'error': 'Insufficient quota for the day.'}, status=400)
#
#     # Save the transaction
#     transaction = Transaction.objects.create(
#         CONSUMED_QTY=consumed_qty,
#         BALANCE_QTY=balance_qty,
#         MEMBERSHIP_ID=card,
#         READER_ID=reader
#     )
#
#     # Return success response
#     return JsonResponse({
#         'success': True,
#         'message': 'Transaction authorized.',
#         'txn_id': transaction.id,
#         'dispense_duration_in_sec': consumed_qty * 1  # Adjust logic as needed
#     }, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def get_quota(request):
    # Extract query parameters
    card_number = request.GET.get('card')
    reader_id = request.GET.get('reader')

    if not card_number or not reader_id:
        return JsonResponse({'error': 'Card number and reader ID are required.'}, status=400)

    try:
        # Get the Membership and Reader
        card = Membership.objects.get(number=card_number)
        reader = Reader.objects.get(mac=reader_id)
    except Membership.DoesNotExist:
        return JsonResponse({'error': 'Invalid card number.'}, status=404)
    except Reader.DoesNotExist:
        return JsonResponse({'error': 'Invalid reader ID.'}, status=404)


    consumer = card.consumer_id
    try:

        quota = Quota.objects.get(Gender=consumer.gender, Status=1)
    except Quota.DoesNotExist:
        return JsonResponse({'error': 'Quota not found for the specified gender.'}, status=404)

    # Calculate total and available balance quota
    total_allowed_quota = int(quota.DAILY_QUOTA)
    consumed_qty = Transaction.objects.filter(MEMBERSHIP_ID=card).aggregate(
        consumed=Sum('CONSUMED_QTY'))['consumed'] or 0
    balance_available_quota = total_allowed_quota - consumed_qty


    return JsonResponse({
        'total_allowed_quota': total_allowed_quota,
        'balance_available_quota': balance_available_quota
    }, status=200)