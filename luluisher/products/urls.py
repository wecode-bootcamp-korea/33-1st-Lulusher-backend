from django.urls import path
from products.views import MenuListView

urlpatterns = [
    path('/menu', MenuListView.as_view()),
    ]