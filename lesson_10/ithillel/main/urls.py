from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cards/', views.cards, name='cards'),
    path('newcard/', views.newcard, name='newcard'),
]
