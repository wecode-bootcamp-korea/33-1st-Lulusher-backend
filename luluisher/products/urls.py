from django.urls import path
from products.views import productListView

urlpatterns = [
    path('/productList', productListView.as_view()),
    ]