from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api_v1 import views
from api_v1.views import OrdersView, OrderProductsView

app_name = 'api_v1'
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('orderproducts', views.OrderProductsView)

urlpatterns = [
    # для  APIView
    path('orders/', OrdersView.as_view(), name='OrdersView'),
    path('orders/<int:pk>/', OrdersView.as_view(), name='OrdersView'),

    # path('products/', ProductsView.as_view()),
    # path('products/<int:pk>/', ProductsView.as_view()),
    # для viewsets.ModelViewSet
    path('', include(router.urls)),
    # для получения Токена
    path('login/', obtain_auth_token, name='api_token_auth'),
    # Для удаления токена
    path('logout/', LogoutView.as_view(), name='logout_view'),
]
