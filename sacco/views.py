from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from sacco.app_forms import CustomerForm
from sacco.models import Customer, Deposit


# Create your views here.
# This below folded table is the initial test table
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


    return HttpResponse(f"Ok, Done. We have {customer_count} customers and {deposit_count} deposits") # Create your views here.

def customers(request):
    # data = Customer.objects.all().order_by('-id').values() # select * from customers
    data = Customer.objects.all().order_by('id').values()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1) #1 is a default page loaded if the page input is missing
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage  :
        paginated_data = paginator.page(1) #1 is a default page loaded if the page input is invalid

    return render(request, "customers.html", {"data": paginated_data}) #note that the data object carries key paginated information. also used in the customers.html loop


def delete_customer(request, customer_id):
    customer= Customer.objects.get(id=customer_id) # select * from customers where id = ?
    customer.delete() #delete from customers where id = ?
    return redirect('customers') #this redirect needs the exact name in urls page. ie name=customers


def add_customer(request):
    if request.method == "POST": # save your form data to db
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {"form": form})


#install these apps - then load them up under settings - installed apps
# pip install django-crispy-forms
# pip install crispy-bootstrap5




