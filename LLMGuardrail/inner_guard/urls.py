from django.urls import path

from .views import InnerGuardrailView

urlpatterns = [
    path('safedecoding/', InnerGuardrailView.as_view(), name='inner_guardrail'),
]
