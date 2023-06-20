from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('cart/', views.cart),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item")
    # path('login/', auth_views.LoginView.as_view(), name = 'login')
]