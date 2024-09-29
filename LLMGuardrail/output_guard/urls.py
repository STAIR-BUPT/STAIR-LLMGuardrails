from django.contrib import admin
from django.urls import path, include

from output_guard.views import OutputEvaluatoreView
from output_guard.views import OutputGuardView

urlpatterns = [
    path('output_evaluation/', OutputEvaluatoreView.as_view(), name='output_evaluation'),
    path('output_guardrail/', OutputGuardView.as_view(), name='output_guardrail'),
]