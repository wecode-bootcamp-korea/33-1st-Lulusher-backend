from django.urls import path
from products.views import productListView, MenuListView

urlpatterns = [
    path('/menu', MenuListView.as_view()),
    ]