from django.urls import path
from . import views
urlpatterns = [
    path('',views.registrationView,name='registrationView'),
    path('registrationOrgInfoView/',views.registrationOrgInfoView,name='registrationOrgInfoView'),
    path('registrationSendOtpView/',views.registrationSendOtpView,name='registrationSendOtpView'),
    path('registrationReceiveOtpView/',views.registrationReceiveOtpView,name='registrationReceiveOtpView'),
    path('login/',views.loginView,name='loginView'),
    path('logout/',views.logoutView,name='logoutView'),
]