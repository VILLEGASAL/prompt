from django.urls import path
from . import views

urlpatterns = [

    path('optimize/', views.optimize_prompt, name = "optimize_prompt")
]