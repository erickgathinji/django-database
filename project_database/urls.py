"""
URL configuration for project_database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from sacco import views

urlpatterns = [

    path('', views.customers, name='customers'),  # add /customers on host url in browser if you specified 'test'

    path('add/customer', views.add_customer, name='add_customer'),

    path('customers/delete/<int:customer_id>', views.delete_customer, name='delete_customer'), # this is the delete button

    path('customers/details/<int:customer_id>', views.customer_details, name='customer_details'), # this is the details button


    path('admin/', admin.site.urls),
]
