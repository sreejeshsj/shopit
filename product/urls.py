
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('product/',views.product,name='product'),
    path('product_details/<int:pk>/',views.productDetails,name='product_details'),
    path('search/',views.search,name='search')
]