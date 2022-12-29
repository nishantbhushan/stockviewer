from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name = 'account-login-view'),    
    path('', views.login_view, name = 'account-login-view'),  
    path('logout/', views.logout_view, name = 'account-logout-view'),
    path('register/', views.register_view, name = 'account-register-view'), 
]