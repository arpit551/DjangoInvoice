from django.urls import path
from InvoiceEntry import views
urlpatterns = [
        path('create/',views.create,name='create'),
        path('analyse/', views.analyse, name='analyse'),
        ]

