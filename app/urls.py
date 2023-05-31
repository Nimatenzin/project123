from django.urls import path, include
from app import views
from app.views import * 


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser.html'),
    path('login/', views.login, name='login'),
    path('show_available_time_slots/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('unknownDashboard/', views.unknownDashboard, name='unknownDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('customer/', include('customer.urls')),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('show_available_time_slots/', views.show_available_time_slots, name='show_available_time_slots'),
    path('book_time_slot/<int:time_slot_id>/', views.book_time_slot, name='book_time_slot'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment-approval/', views.payment_approval, name='payment-approval'),
    path('payment-approval/approve/<int:payment_id>/', views.approve_payment, name='approve-payment'),
    path('payment-approval/cancel/<int:payment_id>/', views.cancel_payment, name='cancel-payment'),
    path('cust_availability/', views.cust_availability, name='cust_availability'),
    path('contact/', views.contact, name='contact'),
    

]


