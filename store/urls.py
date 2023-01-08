from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static  import static





urlpatterns = [
    path('', views.index),  
    path('home',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='login'),
    path('user_logout',views.user_logout,name='logout'),
    path('admin_login/',views.admin_login,name='adminlogin'),
    path('admin_dashboard',views.admin_dashboard,name='dashboard'),
    path('admin_userinfo',views.admin_userinfo,name='user'),
    path('admin_listproduct',views.admin_listproduct,name='product'),
    path('admin_addproduct',views.admin_addproduct,name='product'),
    path('admin_categoryadd',views.admin_categoryadd,name='category'),
    path('view_category',views.view_category,name='category'),
    path('block/<int:id>',views.block,name='block'),
    path('unblock/<int:id>',views.unblock,name='unblock'),
    path('admin_logout',views.admin_logout),
    path('delete_category/<int:id>',views.delete_category,name='cancel'),
    path('product_details/<int:id>',views.product_details),
    path('updatepro/<int:id>',views.updatepro),
    path('deletepro/<int:id>',views.deletepro),
    path('product1',views.product1), 
    path('product2',views.product2),
    path('product',views.product),
    path('cart',views.cart,name='cart'),
    path('add_to_cart',views.add_to_cart,name='addtocart'),
    path('checkout',views.checkout,name='checkout'),
    path('orders',views.orders,name='orders'),
    path('product_details',views.product_details,name='product_details'),
    path('delete_from_cart/<int:id>',views.delete_from_cart,name='delete_from_cart'),
    path('cart_update/<int:id>',views.cart_update,name='cart_update'),
    path('add_quantity/<int:id>',views.add_quantity,name='add_quantity'),
    path('sub_quantity/<int:id>',views.sub_quantity,name='sub_quantity'),
    path('add_address',views.add_address,name='add_address'),
    path('admin_order_management',views.admin_order_management,name='admin_order_management'),
    path('admin_cancel_order/<int:id>',views.admin_cancel_order, name='admin_cancel_order'), 
    path('admin_order_detailed_view/<int:id>',views.admin_order_detailed_view, name='admin_order_detailed_view'),
    path('paypal_checkout',views.paypal_checkout,name='paypal_checkout'),
    path('payment_methods/<int:order_total>',views.payment_methods, name='payment_methods'), 
    path('payment_confirm/<int:order_total>',views.payment_confirm, name='payment_confirm'), 
    path('payment_complete/', views.payment_complete, name="payment_complete"),
    path('payment_methods_razorpay/<int:id>',views.payment_methods_razorpay, name='payment_methods'),
    path('razor_pay/<int:id>', views.razor_pay, name="razor_pay"),
    path('apply_coupan/',views.apply_coupan, name='apply_coupan'),
    path('view_coupon',views.view_coupon,name='view_coupon'),
    path('coupan_management', views.coupan_management, name="coupan_management"),
    path('delete_coupan_offer/<int:id>',views.delete_coupan_offer, name='delete_coupan_offer'),
    path('offers',views.offers, name='view_offers'),
    path('product_offer_management/', views.product_offer_management, name="product_offer_management"),
    path('delete_product_offer/<int:id>',views.delete_product_offer, name='delete_product_offer'),
    path('category_offer_management/', views.category_offer_management, name="category_offer_management"),
    path('delete_category_offer/<int:id>',views.delete_category_offer, name='delete_category_offer'),
    path('admin_dash/',views.admin_dash),
    path('sales',views.sales_report_date, name='sales'),
    path('export_to_pdf',views.export_to_pdf, name='export_to_pdf'),
    path('export_to_excel',views.export_to_excel, name='export_to_excel'),
    path('otp/',views.otp),
    path('smslogin',views.smslogin),
    path('myprofile/',views.myprofile, name='myprofile'),
    path('address_management/',views.address_management, name='address_management'),
    path('delete_address/<int:id>',views.delete_address, name='delete_address'),
    path('edit_profile/<int:id>',views.edit_profile, name='edit_profile'),
    path('user_order_management/',views.user_order_management, name='user_order_management'),
    path('user_cancel_order/<int:id>',views.user_cancel_order, name='user_cancel_order'),
    path('user_order_detailed_view/<int:id>',views.user_order_detailed_view, name='user_order_detailed_view'), 
    path('download/<int:productID>',views.download, name='download'),
    path('view_wishlist/',views.view_wishlist, name='view_wishlist'),
    path('filter_order/<str:status>',views.filter_order,name='filter_order'),
    
    

    



    


     













]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)








