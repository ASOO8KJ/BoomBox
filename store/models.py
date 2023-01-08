from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    password=models.CharField(max_length=200,null=True)
    status=models.BooleanField(default=True)
class add_category(models.Model):
    category_name=models.CharField(max_length=100)

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    p_description=models.CharField(max_length=200)
    price=models.IntegerField()
    stock=models.IntegerField()
    category=models.ForeignKey(add_category,on_delete=models.CASCADE,related_name="add_category_table")
    image1=models.ImageField(upload_to='media',blank=True)
    image2=models.ImageField(upload_to='media',blank=True)
    image3=models.ImageField(upload_to='media',blank=True)
    image4=models.ImageField(upload_to='media',blank=True)
class Cart(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField()
class Address(models.Model):
    user_id=models.IntegerField()
    buyer_name=models.CharField(max_length=50)
    buyer_phone=models.CharField(max_length=11)
    address=models.CharField(max_length=100)
    pincode=models.CharField(max_length=7)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=30)
    country=models.CharField(max_length=50)
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out of delivery','Out of delivery'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField()
    status = models.CharField(max_length=50,choices=STATUS,default='Confirmed')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,default='Confirmed')
    out_for_delivery = models.DateTimeField(blank=True,null=True)
class Wishlist(models.Model):
    user_table=models.ForeignKey(User,on_delete=models.CASCADE)
    product_table=models.ForeignKey(Product,on_delete=models.CASCADE)

class Coupan(models.Model):
    coupan_code=models.CharField(max_length=25)
    start_date_and_time=models.DateTimeField()
    end_date_and_time=models.DateTimeField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage=models.CharField(max_length=5,blank=True)
    maximum_usage=models.IntegerField(blank=True)

class Coupan_applied(models.Model):
    coupan=models.IntegerField()
    user=models.IntegerField()

class Category_offer(models.Model):
    Category=models.ForeignKey(add_category,on_delete=models.CASCADE)
    start_date_and_time=models.DateField()
    end_date_and_time=models.DateField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage=models.CharField(max_length=5,blank=True)

class Product_offer(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    start_date_and_time=models.DateField()
    end_date_and_time=models.DateField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage= models.CharField(max_length=5,blank=True)
class CartGuestUser(models.Model):
    user_session=models.CharField(max_length=20)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.CharField(max_length=5)


class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()    
