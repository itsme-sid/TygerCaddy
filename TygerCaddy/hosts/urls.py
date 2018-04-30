from django.urls import path
from .views import CreateHost, UpdateHost, DeleteHost

urlpatterns = [
    path('add/', CreateHost.as_view(), name="create-host"),
    path('update/<int:pk>/', UpdateHost.as_view(), name="update-host"),
    path('delete/<int:pk>/', DeleteHost.as_view(), name="delete-host"),

]