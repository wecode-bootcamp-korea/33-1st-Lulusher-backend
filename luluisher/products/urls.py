from django.urls import path

from products.views import MenuListView, ProductListView, ReviewView, ProductDetailView

urlpatterns = [
    path('/menu', MenuListView.as_view()),
    path('/list', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/review', ReviewView.as_view()),
    path('/<int:product_id>/review/<int:review_id>', ReviewView.as_view()),
    ] 