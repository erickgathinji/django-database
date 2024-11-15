from django.db import models

# Create your models here.
#These are your tables
#no need for an id column, it is automatically added
class Customer(models.Model):
    first_name = models.CharField(max_length=30) #charfield = varchar
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True) #varchar + ensures email is unique
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    weight = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.gender}"

    class Meta:
        db_table = 'customers'

class Deposit(models.Model):
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.first_name} - {self.amount}"


    class Meta:
        db_table = 'deposits'

#run the migrations
# python manage.py makemigrations
# python manage.py migrate

#command to import json data file
#python manage.py populate
