from django.urls import path
from app import views as AppViews
from . import views


urlpatterns = [
    path('', AppViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile')
]