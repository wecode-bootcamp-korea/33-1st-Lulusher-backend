from django.urls import path
from products.views import productListView, MenuListView, ReviewView

urlpatterns = [
    path('/productList', productListView.as_view()),
    path('/menu', MenuListView.as_view()),
    path('/<int:product_id>/review', ReviewView.as_view()),
    path('/<int:product_id>/review/<int:review_id>', ReviewView.as_view()),
    ]