from django.urls import path

from . import views

urlpatterns = [
    path('', views.portfolioView, name = 'portfolio-view'),  
    path('<str:chartOption>', views.portfolioView, name ='portfolio-view-with-options'),
    path('<str:tickerName>', views.portfolioView, name ='portfolio-ticker-view'),    
    path('<str:tickerName>/<str:chartOption>', views.portfolioView, name ='portfolio-ticker-view-with-options'),
    path('edit/', views.portfolioView),
    path('testform/', views.normalview),
]