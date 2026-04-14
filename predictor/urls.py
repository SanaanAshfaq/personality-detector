from django.urls import path
from .views import PredictPersonalityView

urlpatterns = [
    path("predict/", PredictPersonalityView.as_view(), name="predict"),
]