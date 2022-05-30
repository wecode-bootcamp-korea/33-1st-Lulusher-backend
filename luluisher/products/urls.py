from django.urls import path
from products.views import productListView, MenuListView

urlpatterns = [
    path('/productList', productListView.as_view()),
    path('/menu', MenuListView.as_view()),
    ]