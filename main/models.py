from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Creator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return "%s" % (self.name)
class GPU(models.Model):
    name = models.CharField(max_length=100)
    type_memory = models.CharField(max_length=20)
    count_memory = models.IntegerField(max_length=10)
    def __str__(self):
        return "%s" % (self.name)
class CPU(models.Model):
    name = models.CharField(max_length=100)
    frequency = models.IntegerField(max_length=10)
    count_core = models.IntegerField(max_length=2)
    def __str__(self):
        return "%s" % (self.name)

class Product(models.Model):
    code_product = models.IntegerField(max_length=10, primary_key=True, auto_created=False, unique=True)
    name = models.CharField(max_length=50)
    cpu = models.ForeignKey(to=CPU, on_delete=models.PROTECT)
    price_z = models.DecimalField(max_digits=30, decimal_places=3)
    price_p = models.DecimalField(max_digits=30, decimal_places=3)
    photo = models.ImageField(null=True, blank=True)
    count = models.IntegerField(max_length=10)
    gpu = models.ForeignKey(to=GPU, on_delete=models.PROTECT)
    ram = models.IntegerField(max_length=10)
    rom = models.IntegerField(max_length=10)
    lenght = models.FloatField(max_length=5)
    width = models.FloatField(max_length=5)
    height = models.FloatField(max_length=5)
    creator = models.ForeignKey(to=Creator, on_delete=models.PROTECT)

    def __str__(self):
        return "%s, %s, " % (self.code_product, self.name)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, null=True, blank=True)
    otchestvo = models.CharField(max_length=50, verbose_name='Отчество')
    area = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    home = models.CharField(max_length=10, null=True, blank=True)
    room = models.CharField(max_length=10, null=True, blank=True)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otchestvo = models.CharField(max_length=50)
    count_orders = models.IntegerField(default=0)

    class Meta:
        ordering = ['count_orders']

class State(models.Model):
    state = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return "%s" % (self.state)

class Order(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT)
    manager = models.ForeignKey(to=Manager,on_delete=models.PROTECT)
    state = models.ForeignKey(to=State, on_delete=models.PROTECT)
    date_create = models.DateField()
    time_create = models.TimeField(null = True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    is_created = models.BooleanField(default=False)

    def __str__(self):
        return "%s, %s, %s" % (self.pk, self.date_create, self.state.state)


class Orders_products(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    count = models.IntegerField(max_length=5)
    def __str__(self):
        return "%s, %s, %s" % (self.order.pk, self.product.pk, self.count)