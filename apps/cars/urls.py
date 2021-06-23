from django.urls import path

from apps.cars import views

urlpatterns = [
    path("cars/", views.CarListView.as_view(), name="cars"),
    path("cars/<int:id>/", views.CarListDestroyView.as_view(), name="cars-detail")
]
