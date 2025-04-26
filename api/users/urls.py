from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("me/", views.UserDetailView.as_view(), name="user-detail"),
]
