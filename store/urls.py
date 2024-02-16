from django.urls import path 
from . import views

urlpatterns = [
    path('', views.store, name='store'),

    # registros:
    #path('registro/',views.registro,name='registro'),
	
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
   # path('accounts/signup',views.signup,name='signup'),
    path('registro/',views.registro,name='registro'),
	path('update_item/', views.updateItem, name="update_item"),
    path('contact/',views.contact,name="contact"),
	#path('process_order/', views.processOrder, name="process_order"),
    path('verproductos',views.verproductos,name='verproductos'),

    path('product_list/', views.product_list, name='product_list'),

]
