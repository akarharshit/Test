from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('grant_permission/', views.grant_permission, name='grant_permission'),
]
