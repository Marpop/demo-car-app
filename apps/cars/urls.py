from django.urls import path

from apps.cars import views

urlpatterns = [
    path("cars/", views.CarListView.as_view(), name="cars"),
    path("cars/<int:pk>/", views.CarDestroyView.as_view(), name="cars_detail"),
    path("rate/", views.RateCarView.as_view(), name="rate"),
    path("popular/", views.PopularCarsListView.as_view(), name="popular"),
]
