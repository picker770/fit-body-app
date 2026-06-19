from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),
]