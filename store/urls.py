from django.urls import path 
from . import views

urlpatterns = [
    path('', views.store, name='store'),

	
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    # registros:

    path('registro/',views.registro,name='registro'),
	path('update_item/', views.updateItem, name="update_item"),
    path('contact/',views.contact,name="contact"),
	#path('process_order/', views.processOrder, name="process_order"),
    path('ver_producto/<int:product_id>/', views.ver_producto, name='ver_producto'),

    path('product_list/', views.product_list, name='product_list'),
    #pagos de paypal
    #path('procesar_pago/',views.procesar_pago,name='procesar_pago'),

]
