"""
URL configuration for brokart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('cart', views.show_cart,name='cart'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:item_id>',views.remove_from_cart,name='remove_from_cart'),
    path('update_cart_quantity/<int:item_id>',views.update_cart_quantity,name='update_cart_quantity'),
    path('checkout',views.checkout,name='checkout'),
    path('order_history',views.order_history,name='order_history'),
    path('order/<int:order_id>',views.order_detail,name='order_detail'),
]

