from telnetlib import LOGOUT
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from urllib import response
from store.models import User
from.models import *
from django.shortcuts import render,redirect
from django.contrib.auth import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
#import paginator
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import datetime
import razorpay
from django.contrib import messages
from django.utils import timezone
import random
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import io
from xhtml2pdf import pisa 
from django.template.loader import get_template
import xlwt

 
# Create your views here.
def index(request):
    data=Product.objects.all()
    return render(request,'index.html',{'data':data})

@never_cache
def home(request):
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=Product.objects.all() 
            return render(request, 'index.html',{'data':data})
        data=Product.objects.filter(product_name__icontains=search)
        return render(request, 'home.html',{'data':data})
    a=Product.objects.all()
    if 'user_id' in request.session:
      data=Product.objects.all()
      return render(request,'home.html',{'data':data})
    else:
        return redirect(user_login)
    
@never_cache    
def register(request):
    if request.method =='POST':
        username =request.POST['username']
        email =request.POST['email']
        phone =request.POST['phone']
        password =request.POST['password']
        if username=='' or email=='' or phone=='' or password=='':
         return render(request,"register.html")


        profile=User.objects.create(name=username,password=password,phone=phone,email=email)
        profile.save()
        print("profile Saved")
        return redirect(user_login)
    return render(request,'register.html')    

def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user=User.objects.filter(name=username,password=password)
        if user:
          status=User.objects.get(name=username,password=password)
          print(status.name,status.status)
          if status.status==True:
            request.session['user_id']=status.id
            return redirect(home)

        else:
            messages.info(request,'invalid credentials')
            return render(request, 'user_login.html')
    if 'user_id' in request.session:
                return redirect(home)

    return render(request, 'user_login.html')
@never_cache
def user_logout(request):
    logout(request)
    return redirect(index)

def admin_login(request):
    if request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None and user.is_superuser:
              login(request,user)
              request.session['username'] =username
              return render(request,'admin_dashboard.html')
        else:
                return redirect('/admin_login')
    else:
        return render(request,'admin_login.html')
@never_cache
@login_required(login_url=admin_login)
def admin_logout(request):
    logout(request)
    return redirect('/admin_login')
@never_cache
@login_required(login_url=admin_login)  
def admin_dashboard(request):
     return render(request,'admin_dashboard.html')
def admin_userinfo(request):
     profile=User.objects.all()
      #setup paginator
     p=Paginator(profile,2)
     page=request.GET.get('page')
     product=p.get_page(page)
     return render(request,'admin_userinfo.html',{'profile':product,'product':product})
def admin_listproduct(request):
     data=Product.objects.all()
     #setup paginator
     p=Paginator(data,3)
     page=request.GET.get('page')
     product=p.get_page(page)
     return render(request,'admin_listproduct.html',{'data':data,
     'product':product})
def admin_addproduct(request):
    if request.method=='POST':
        
        product_name = request.POST.get('p_name')
        p_description = request.POST.get('p_description')
        price = request.POST.get('pric')
        print("price",price)
       
        c_id=request.POST.get('c_id')
        print("stock",c_id)
        stock=request.POST.get('stock')
        cat_id = add_category.objects.get(id=c_id)
        image1 = request.FILES.get('img1')
        image2 = request.FILES.get('img2')
        image3 = request.FILES.get('img3')
        image4 = request.FILES.get('img4')
        c=Product.objects.create(product_name=product_name,p_description=p_description,price=price,stock=stock,category=cat_id,image1=image1,image2=image2,image3=image3,image4=image4)
        c.save()
    data=add_category.objects.all()
    return render(request, 'admin_addproduct.html',{'data':data})


def admin_categoryadd(request):
    if request.method=='POST':
        category=request.POST['category']
        reg=add_category.objects.create(category_name=category)
        reg.save()
    return render(request,'admin_category add.html')
def view_category(request):
    data=add_category.objects.all()
    return render(request,'view_category.html',{'data':data})

def block(request,id):
    profile=User.objects.get(id=id)
    profile.status=False
    profile.save()
    return redirect(admin_userinfo)
def unblock(request,id):
    profile=User.objects.get(id=id)
    profile.status=True
    profile.save()
    return redirect(admin_userinfo)
def delete_category(request,id):
    add_category.objects.get(id=id).delete()
    return redirect('/view_category')
def product_details(request,id):
    if request.method == "POST":
        if request.POST.get('cart_button'):
            if 'user_id' in request.session:
                user_id=request.session.get('user_id')
                cart_for_check=Cart.objects.filter(user_id=user_id,product_id=id)
                if cart_for_check:
                    cart_last=Cart.objects.get(user_id=user_id,product_id=id)
                    cart_last.product_qty=int(cart_last.product_qty)+1
                    cart_last.save()
                else:
                    product_id=id
                    quantity=1
                    data1=User.objects.get(id=user_id)
                    data2=Product.objects.get(id=product_id)
                    my_cart=Cart.objects.create(user_id=data1,product_id=data2,product_qty=quantity)
                    my_cart.save()
            # else:
            #     return redirect(add_cart_guest,id)
        if request.POST.get('wishlist_button'):
            if 'user_id' in request.session:
                user_id=request.session.get('user_id')
                product_id=id
                data1=User.objects.get(id=user_id)
                data2=Product.objects.get(id=product_id)
                my_wishlist=Wishlist.objects.create(user_table=data1,product_table=data2)
                my_wishlist.save()
            else:
                return redirect(user_login)
    data=Product.objects.get(id=id)
    # if 'user_id' in request.session:
    #     return render(request,'product_details1.html',{'data':data})
    return render(request,'product_details.html',{'data':data})
def updatepro(request,id):
    data1=Product.objects.get(id=id)
    if request.method=='POST':
        data2=Product.objects.get(id=id)
        pro=Product(id=id)
        pro.product_name=request.POST.get('p_name')
        pro.p_description=request.POST.get('p_description')
        pro.price=request.POST.get('price')
        pro.category=data2.category
        pro.stock=request.POST.get('stock')
        pro.image1=request.FILES.get('img1')
        pro.image2=request.FILES.get('img2')
        pro.image3=request.FILES.get('img3')
        pro.image4=request.FILES.get('img4')
        pro.save()
    data=add_category.objects.all()
    return render(request,'updatepro.html',{'data':data,'data1':data1})
def deletepro(request,id):
    data=Product.objects.get(id=id)
    data.delete()
    return redirect(admin_listproduct)
def product1(request):
    if 'user_id' in request.session:
      data=Product.objects.all()
      return render(request,'product1.html',{'data':data})
def product2(request):
    if 'user_id' in request.session:
      data=Product.objects.all()
      return render(request,'product2.html',{'data':data})
def product(request):
    return render(request,'product.html')
# def cart(request):

#     return render(request,'cart.html')
# Add to cart
def add_to_cart(request):
    if request.method=='POST':
        pro_id = request.POST.get('prod_id')
        user=User.objects.get(name=user)
        print(user)
        product=Product.objects.get(id=pro_id)
   
        new = Cart.objects.create(user_id=user.id,Product_id=product)
    return redirect("/cart")
# def cart(request):
#    user=request.user
#    user = User.objects.get(name=user)
#    cart=Cart.objects.filter(user_id=user.id)
#    return render(request,'cart.html',{'cart':cart})


def cart(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        a=0                                                          
        for i in cart:
            a = a+i.product_id.price*int(i.product_qty)
        if request.method == "POST":
            if cart:
                return redirect(checkout)
            else:
                return redirect(cart)
        return render(request,'cart.html',{'cart':cart,'total':a})
    return redirect(user_login)
def add_quantity(request,id):
    data=Cart.objects.get(id=id)
    data.product_qty=int(data.product_qty)+1
    data.save()
    return redirect(cart)
def sub_quantity(request,id):
    data=Cart.objects.get(id=id)
    f=int(data.product_qty)
    if f != 1:
        data.product_qty=int(data.product_qty)-1
    else:
        pass
    data.save()
    return redirect(cart)
def delete_from_cart(request,id):
    data=Cart.objects.get(id=id)
    data.delete()
    return redirect("/cart")
def cart_update(request):
   print('cart')
   body = json.loads(request.body)
   cart = Cart.objects.get(id=body['cart_id'])
   cart.Product_qty = body['product_qty']
#    cart.total_price = body['total']
   cart.save()
   print("cart_test",body)
   print("update cart")
   return redirect(cart)
    



    
def checkout(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        if cart:
            id = request.session.get('user_id')
            cart=Cart.objects.filter(user_id=id)
            a=0
            for i in cart:
                a = a+i.product_id.price*int(i.product_qty)
            coupan_price=0
            total1=a
            if 'coupan_session' in request.session:
                coupan_id=request.session.get('coupan_session')
                request.session['not_valid']=coupan_id
                del request.session['coupan_session']
            if 'not_valid' in request.session:
                coupan_id=request.session.get('not_valid')
                coupan_obj=Coupan.objects.get(id=coupan_id)
                coupan_price=coupan_obj.discount_amount
                a=a - int(coupan_price)
            address=Address.objects.filter(user_id=id)
            if request.method=='POST':
                payment_method=request.POST['payment_method']
                selected_address_id=request.POST.get('selected_address')
                print("selected_Address_id",selected_address_id)
                request.session['address_session']=selected_address_id
                print("selected_address_id_using_session",request.session.get('address_session'))
                if payment_method == 'paypal':
                    return redirect(payment_methods,a)
                user_id = request.session.get('user_id')
                data1=User.objects.get(id=user_id)
                reg=Payment()
                reg.user=data1
                if payment_method == 'COD':
                    reg.payment_method=payment_method
                    reg.status='pending'
                    if 'not_valid' in request.session:
                        user=data1.id
                        if 'not_valid' in request.session:
                            b=request.session.get('not_valid')
                            print("cod_coupan_id",b)
                            cou=Coupan_applied.objects.create(coupan=b,user=user)
                            cou.save()
                            del request.session['not_valid']
                reg.save()
                data=Order()
                data.user=data1
                data.payment=reg
                selected_address_id=request.session.get('address_session')
                print("rijin raju",selected_address_id)
                data.address=Address.objects.get(id=selected_address_id)
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                data.order_number = current_date + str(reg.id)
                data.order_total=a
                data.save()
                for i in cart:
                    data2=OrderProduct()
                    data2.order=data
                    data2.payment=reg
                    data2.user=data1
                    data2.product=Product.objects.get(id=i.product_id.id)
                    data2.quantity=i.product_qty
                    data2.product_price=i.product_id.price
                    data2.save()
                if payment_method == 'razorpay':
                    return redirect(payment_methods_razorpay, reg.pk) 
                for item in cart:
                    product1 = Product.objects.get(id=item.product_id.id)
                    product1.stock -= int(item.product_qty)
                    product1.save()                    
                cart.delete()
                return render(request,'order_successfully.html')
            return render(request,'checkout.html',{'cart':cart,'total':a,'address':address,'total1':total1,'coupan_price':coupan_price})
        else:
            return redirect(cart)
    else:
        return redirect(user_login)

def orders(request):
    user_id=request.session.get('user_id')
    data=OrderProduct.objects.filter(user=user_id)
    for i in data:
        print(i.status)
    return render(request,'orders.html',{'data':data})
def product_details2(request):
    return render(request,'product_details2.html')
def add_address(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        buyer_name = request.POST['b_name']
        buyer_phone = request.POST['b_phone']
        address=request.POST['b_address']
        pincode=request.POST['b_pincode']
        city=request.POST['b_city']
        state=request.POST['b_state']
        country="india"
        reg=Address.objects.create(user_id=user_id,buyer_name=buyer_name,buyer_phone=buyer_phone,address=address,pincode=pincode,city=city,state=state,country=country)
        reg.save()
        return redirect(checkout)
    return render(request,'add_address.html')
@never_cache
@login_required(login_url=admin_login)
def admin_order_management(request):
    data=OrderProduct.objects.filter(ordered=False)
    #setup pagination
    p=Paginator(OrderProduct.objects.filter(ordered=False),5)
    page=request.GET.get('page')
    product=p.get_page(page)
    return render(request,'admin_orders_management.html',{'data':product,'product':product})
@never_cache
@login_required(login_url=admin_login)
def admin_cancel_order(request,id):
    data=OrderProduct.objects.get(id=id)
    data.ordered=True
    data.save()
    return redirect(admin_order_management)

@never_cache
@login_required(login_url=admin_login)
def admin_order_detailed_view(request,id):
    data=OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        status=request.POST.get('status_update_adminside')
        print("status",status)
        data=OrderProduct.objects.get(id=id)
        if status == 'Out for Delivery':
            data.out_for_delivery = datetime.datetime.now()
        data.status=status
        data.save()
    return render(request,'admin_order_detailedview.html',{'i':data})
def paypal_checkout(request):
    return render(request,'paypal_checkout.html')

def payment_methods(request,order_total):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        print("cart 123",cart)
        # order = Order.objects.get(payment_id=id)
        a= order_total
       
    return render(request,'paypal_checkout.html',{'cart':cart,'total':a})

def payment_confirm(request,order_total):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        user_id = request.session.get('user_id')
        data1=User.objects.get(id=user_id)
        body = json.loads(request.body)
        print("nothing to worry",body)
        reg=Payment()
        reg.user=data1
        reg.payment_id = body['transId']
        reg.payment_method = 'Paypal'
        reg.amount_paid = order_total
        reg.status= body['status']
        reg.save()
        if 'not_valid' in request.session:
            user=data1.id
            b=request.session.get('not_valid')
            print("cod_coupan_id",b)
            cou=Coupan_applied.objects.create(coupan=b,user=user)
            cou.save()
            del request.session['not_valid']
        data=Order()
        data.user=data1
        data.payment=reg
        selected_address_id=request.session.get('address_session')
        print("rijin raju",selected_address_id)
        data.address=Address.objects.get(id=selected_address_id)
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        data.order_number = current_date + str(reg.id)
        data.order_total=order_total
        data.save()
        for i in cart:
            data2=OrderProduct()
            data2.order=data
            data2.payment=reg
            data2.user=data1
            data2.product=Product.objects.get(id=i.product_id.id)
            data2.quantity=i.product_qty
            data2.product_price=i.product_id.price
            data2.save()  
        for item in cart:
            product1 = Product.objects.get(id=item.product_id.id)
            product1.stock -= int(item.product_qty)
            product1.save()                  
        cart.delete()
        data={
            'transId': reg.payment_id,
        }
        return JsonResponse(data)       

def payment_complete(request):
     return render(request,'order_successfully.html')

def payment_methods_razorpay(request,id):
    print(id)
    if 'razorpay_payment_for_order' in request.session:
        del request.session['razorpay_payment_for_order']
    if 'user_id' in request.session:
        usrr=request.session.get('user_id')
        user=User.objects.get(id=usrr)
        order = Order.objects.get(payment_id=id)
        a= order.order_total

        client = razorpay.Client(auth=("rzp_test_Aw0U31Agzn6ZY3", "Nc9XcsquNXcdt4aXPDfXEeyz"))

        data = { "amount": a*100,
                 "currency": "INR", 
                 "receipt": "order_rcptid_11"
                }
        payment = client.order.create(data=data)
        print(payment)
        cart = OrderProduct.objects.filter(payment_id=id)
        print("cart 123",cart)
        request.session['razorpay_payment_for_order']=payment
        
    return render(request,'razorpay_checkout.html',{'cart':cart,'total':a,'Razorpay_payment_id':id,'order':order,'payment':payment})

@csrf_exempt
def razor_pay(request,id):
    if 'user_id' in request.session:
        order = Order.objects.get(payment_id=id)
        userid=request.session.get('user_id')
        user=User.objects.get(id=userid)
        payment=request.session.get('razorpay_payment_for_order')
        pay = Payment.objects.get(id=id)
        pay.payment_method = 'razorpay'
        pay.status = payment['status']
        pay.payment_id = payment['id']
        pay.user = user
        actual_amount=payment['amount']
        actual_amount=actual_amount/100
        pay.amount_paid = actual_amount
        pay.save()
        cart1=Cart.objects.filter(user_id=userid)
        for item in cart1:
            product1 = Product.objects.get(id=item.product_id.id)
            product1.stock -= int(item.product_qty)
            product1.save()   
            cart1.delete()
        if 'razorpay_payment_for_order' in request.session:
            del request.session['razorpay_payment_for_order']
    return render(request,'order_successfully.html')

#search
# def search(request):
#     q=request.GET['q']
#     data=Product.objects.filter(title_icontains=q).order_by('-id')
#     return render(request,'search.html',{'data':data})

def apply_coupan(request):
    if 'user_id' in request.session:
        user=request.session.get('user_id')
        if request.method=='POST':
            coupan_code = request.POST['coupan_code']
            c=Coupan.objects.filter(coupan_code=coupan_code)
            if c:
                coupan=Coupan.objects.get(coupan_code=coupan_code)
                d=Coupan_applied.objects.filter(coupan=coupan.id,user=user)
                if d:
                    messages.info(request,'Already Applied Coupon Code')
                    return render(request,'apply_coupan.html')
                now = timezone.now()
                start_date_and_time=coupan.start_date_and_time
                if start_date_and_time < now:
                    if now < coupan.end_date_and_time:
                        coupan_id=coupan.id
                        print(coupan_code,coupan_id)
                        request.session['coupan_session']=coupan_id
                        return redirect(checkout)
                    else:
                        messages.info(request,'Coupon Expired')
                        return render(request,'apply_coupan.html')
                else:
                    messages.info(request,'Coupon is from coupan.start_date_and_time ')
                    return render(request,'apply_coupan.html')
            else:
                messages.info(request,'invalid Coupon Code')
                return render(request,'apply_coupan.html')        
        return render(request,'apply_coupan.html')
    else:
        return redirect(user_login)



def view_coupon(request):
    categories = Coupan.objects.all()
    return render(request,'view_coupon.html',{'coupan':categories})  
@never_cache
@login_required(login_url=admin_login)
def coupan_management(request):
    if request.method=='POST':
        coupan_code = request.POST.get('c_code')
        start_date_and_time = request.POST.get('s_date')
        end_date_and_time = request.POST.get('e_date')
        discount_amount = request.POST.get('d_amount')
        maximum_usage = 0
        print(coupan_code,start_date_and_time,type(start_date_and_time),end_date_and_time,type(end_date_and_time),discount_amount,maximum_usage )
        a=Coupan.objects.create(coupan_code=coupan_code,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_amount=discount_amount,maximum_usage=maximum_usage)
        a.save()
        messages.info(request,'Created successfully')
    return render(request,'coupan_management.html')
def delete_coupan_offer(request,id):
    print(id)
    Coupan.objects.get(id=id).delete()
    return redirect(view_coupon)
@never_cache
@login_required(login_url=admin_login)    
def offers(request):
    product_offer = Product_offer.objects.all()
    category_offer=Category_offer.objects.all()
    return render(request,'offers.html',{'product':product_offer,'category':category_offer})
@never_cache
@login_required(login_url=admin_login)
def product_offer_management(request):
    if request.method=='POST':
        product_id = request.POST.get('c_code')
        print('idhajkhbfkjd',product_id)
        product1=Product.objects.get(id=product_id)
        start_date_and_time = datetime.datetime.now()
        end_date_and_time = request.POST.get('e_date')
        discount_percentage = request.POST.get('d_percentage')
        a=Product_offer.objects.create(product=product1,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_percentage=discount_percentage)
        a.save()
        messages.info(request,'Created successfully')
    category=Product.objects.all()
    return render(request,'product_offer_management.html',{'category':category})
def delete_product_offer(request,id):
    print(id)
    Product_offer.objects.get(id=id).delete()
    return redirect(offers) 
def category_offer_management(request):
    if request.method=='POST':
        category_id = request.POST.get('c_code')
        category=add_category.objects.get(id=category_id)
        start_date_and_time = datetime.datetime.now()
        end_date_and_time = request.POST.get('e_date')
        discount_percentage = request.POST.get('d_percentage')
        a=Category_offer.objects.create(Category=category,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_percentage=discount_percentage)
        a.save()
        messages.info(request,'Created successfully')       
    category=add_category.objects.all()
    return render(request,'categoryoffer_management.html',{'category':category})
def delete_category_offer(request,id):
    print(id)
    Category_offer.objects.get(id=id).delete()
    return redirect(offers)
@never_cache
@login_required(login_url=admin_login)
def admin_dash(request):

    users_count=User.objects.all().count()




  
    
    return render(request,'admin_dash.html',{'users_count':users_count})

@never_cache
@login_required(login_url=admin_login)
def sales_report_date(request):
    data = OrderProduct.objects.all()
    p=Paginator(data,2)
    page=request.GET.get('page')
    venues=p.get_page(page)
    
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum'],'venues':venues}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum'],'venues':venues}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'sales_report_.html')
@never_cache
@login_required(login_url=admin_login)
def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response

@never_cache
@login_required(login_url=admin_login)
def export_to_pdf(request):
    prod = Product.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

@never_cache
@login_required(login_url=admin_login)
def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at_gte=date1,created_at_lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'sales_report_.html')

#my_profile
def myprofile(request):
    user_id=request.session.get('user_id')
    data=User.objects.get(id=user_id)
    return render(request,'myprofile.html',{'data':data})
def address_management(request):
    user_id=request.session.get('user_id')
    data=Address.objects.filter(user_id=user_id)
    return render(request,"address_management.html",{'data':data})

def delete_address(request,id):
    data=Address.objects.get(id=id)
    data.delete()
    return redirect(address_management)

def edit_profile(request,id):
    data = User.objects.get(id=id)
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        phone =request.POST['phone']
        password =request.POST['password']
        data_tb=User.objects.get(id=id)
        data_tb.name=username
        data_tb.email=email
        data_tb.phone=phone
        data_tb.password=password
        data_tb.save() 
        messages.info(request,'Updated successfully')
        return redirect(edit_profile,id)
    return render(request,"update.html",{'data':data})

def user_order_management(request):
    user_id=request.session.get('user_id')
    data=OrderProduct.objects.filter(user=user_id)
    # for i in data:
    #     print(i.status)
    
    p=Paginator(data,3)
    page=request.GET.get('page')
    product=p.get_page(page)
    return render(request,'user_order_management.html',{'data':data,'product':product})
def user_cancel_order(request,id):
    data=OrderProduct.objects.get(id=id)
    print("gfshjkghkshgbklrshk",data)
    data.ordered=True
    data.save()
    return redirect(user_order_management)



def user_order_detailed_view(request,id):
    data=OrderProduct.objects.get(id=id)
    return render(request,'user_order_detailed_view.html',{'i':data})

#wishlist
def view_wishlist(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        wishlist=Wishlist.objects.filter(user_table=id)
        return render(request,'view_wishlist.html',{'wishlist': wishlist})
    return redirect(login)
def delete_from_wishlist(request,id):
    data=Wishlist.objects.get(id=id)
    data.delete()
    return redirect(view_wishlist)

    
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download(request,productID):
    v=OrderProduct.objects.get(id=productID)
    totalprice=v.product.price *v.quantity
    mydict={
        'customerName':v.user.name,
        'customerEmail':v.user.email,
        'customerMobile':v.user.phone,
        'shipmentAddress':v.order.address.address,
        'orderStatus':v.status,
        'quantity':v.quantity,
        'totalprice':totalprice,
        'productimage':v.product.image1,
        'productName':v.product.product_name,
        'productPrice':v.product.price,
        'productDescription':v.product.p_description,
    }
    return render_to_pdf('download.html',mydict)


#otp login
def otp(request):
    

    if request.method=='POST':
        global phone
        phone=str(request.POST.get('phone'))
        print("post success")
        print(phone)
        print()

        if User.objects.filter(phone=phone).exists():
             print("if success")


        
             global otp_number
             otp_number=random.randint(1000,9999)
             account_sid = 'AC26f7fc1dc014b0ba70653b1d63569536'
             auth_token = '50799347b597e9e514ceb3f62f650138'
             client = Client(account_sid, auth_token)

             client.api.account.messages.create(
                                 body=otp_number,
                                 from_='+14793982895',
                                 to='+917012247797',
                             )
             print("otp success")

                
             return render(request,'smslogin.html')
        else:
            print("invalid user")
        
            return render(request,'otp.html',{'message':"invalid phone"})
            

    else:
        print("not post")
        return render(request,'otp.html')


def smslogin(request):
    
    if request.method=='POST':
        Otp1=request.POST.get('otp')
        print(Otp1,otp_number)
        if str(Otp1) == str(otp_number):

            print('eee')
            
            return render(request,'index1.html')
        else:

            return render(request,'smslogin.html',{'message':'invalid otp'})
    else: 


     return render(request,'smslogin.html') 
@never_cache
@login_required(login_url=admin_login)
def filter_order(request,status):
    data=OrderProduct.objects.filter(ordered=False,status=status)
    return render(request,'admin_orders_management.html',{'data':data})



        

    
    







