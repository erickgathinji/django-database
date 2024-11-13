from django.http import HttpResponse
from django.shortcuts import render

from sacco.models import Customer, Deposit


# Create your views here.
def test(request):
    # save a customer
    # c1 = Customer(first_name='Sam', last_name='Kim', email='kim@haveen.com', dob='1999-6-03', gender='Male',
    #               weight='62')
    #
    # c1.save()
    #
    # c2 = Customer(first_name='Glo', last_name='Shi', email='glo@veen.com', dob='2000-6-03', gender='Female',
    #               weight='65')
    # c2.save()
    customer_count = Customer.objects.count()

    #fetching one customer
    c1 = Customer.objects.get(id=1) #same as sql - SELECT * FROM customers where id=1
    print(c1)  #to display this, check the setup in  models [def __str__(self)] just before Meta

    d1 = Deposit(amount=1000, status = True, customer = c1)
    d1.save()

    deposit_count = Deposit.objects.count()


    return HttpResponse(f"Ok, Done. We have {customer_count} customers and {deposit_count} deposits")

