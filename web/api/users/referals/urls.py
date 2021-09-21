from django.urls import path, include

from.views import ReferralActivate

urlpatterns = [
    path("activate", ReferralActivate.as_view()),
]