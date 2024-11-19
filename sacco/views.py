from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# from django.template.context_processors import request

from sacco.app_forms import CustomerForm, DepositForm, LoginForm
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

    # fetching one customer
    c1 = Customer.objects.get(id=1)  # same as sql - SELECT * FROM customers where id=1
    print(c1)  # to display this, check the setup in  models [def __str__(self)] just before Meta

    d1 = Deposit(amount=1000, status=True, customer=c1)
    d1.save()

    deposit_count = Deposit.objects.count()

    return HttpResponse(
        f"Ok, Done. We have {customer_count} customers and {deposit_count} deposits")  # Create your views here.

@login_required #ensure LOGIN_URL = 'login' is defined in settings otherwise define in brackets beside the decoration
def customers(request):
    # data = Customer.objects.all().order_by('-id').values() #id without - sorts from 1
    data = Customer.objects.all().order_by('-id').values()  # select * from customers
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)  # 1 is a default page loaded if the page input is missing
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)  # 1 is a default page loaded if the page input is invalid

    return render(request, "customers.html", {
        "data": paginated_data})  # note that the data object carries key paginated information. also used in the customers.html loop

@login_required
def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)  # select * from customers where id = ?
    customer.delete()  # delete from customers where id = ?
    messages.info(request, f"Customer {customer.first_name} was deleted!")
    return redirect('customers')  # this redirect needs the exact name in urls page. ie name=customers

@login_required
def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = Deposit.objects.filter(customer_id=customer_id)
    total = Deposit.objects.filter(customer=customer).filter(status=True).aggregate(Sum('amount'))['amount__sum']
    return render(request, "details.html", {'deposits': deposits, 'customer': customer, 'total': total})

@login_required
def add_customer(request):
    if request.method == "POST":  # save your form data to db
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} was added!" )
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {"form": form})

@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} was updated!" )
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_update_form.html', {"form": form})

@login_required
def search_customer(request):
    search_term = request.GET.get(
        'search')  # the search (in brackets) must match to the name put in master.html navbar search - input
    data = Customer.objects.filter(
        Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term) | Q(email__icontains=search_term))
    # data = generates select * from customers where first_name LIKE '%noel%' OR last_name LIKE '%noel%'

    # paste paginator info from customers function, then factor in the html pg, and the above data variable
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)  # 1 is a default page loaded if the page input is missing
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)  # 1 is a default page loaded if the page input is invalid

    return render(request, "search.html", {
        "data": paginated_data, "customer": data})

@login_required
def deposit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            depo = Deposit(amount=amount, status=True, customer=customer)
            depo.save()
            messages.success(request, 'Your deposit has been successfully saved!')
            return redirect('customers')
    else:
        form = DepositForm()
    return render(request, 'deposit_form.html', {"form": form, 'customer': customer})


def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login_form.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user) #sessions #cookies
                return redirect('customers')
        messages.error(request, 'Invalid username or password!')
        return render(request, "login_form.html", {"form": form})

@login_required
def signout_user(request):
    logout(request)
    return redirect ('login')
