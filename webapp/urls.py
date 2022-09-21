from django.urls import path

from webapp.views import IndexView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView, CartAddView, \
    CartView, CartDeleteView, CartDeleteOneView, OrderCreate

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('products/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/add-to-cart/', CartAddView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='remove_for_cart'),
    path('cart/<int:pk>/one-delete/', CartDeleteOneView.as_view(), name='remove_one_for_cart'),
    path('order/create/', OrderCreate.as_view(), name='order_create')
]
