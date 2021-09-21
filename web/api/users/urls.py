from django.urls import path, include

urlpatterns = [
    path("referals/", include("users.referals.urls")),
]