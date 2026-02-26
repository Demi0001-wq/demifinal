from django.urls import path
from catalog.views import (ProductListView, ContactTemplateView, ProductDetailView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryProductListView)

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('category/<int:pk>/products/', CategoryProductListView.as_view(), name='category_products'),
]
