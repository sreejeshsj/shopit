from django.urls import path
from . import views
urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:pk>/',views.addCart,name='add_cart'),
    path('remove/<int:pk>/',views.remove,name='remove'),
    path('decrease_quantity/<int:pk>/',views.decrease,name='decrease_quantity'),
    path('increase_quantity/<int:pk>/',views.increase,name='increase_quantity'),
    path('checkout/',views.checkout,name='checkout'),
    path('success/',views.success,name='success'),
    path('orders/',views.orders,name='orders'),
    path('ordersearch/',views.order_search,name='order_search')
    
]
