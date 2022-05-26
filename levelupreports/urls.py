from django.urls import path
from .views import UserGameList, GamerEventList

urlpatterns = [
    path('reports/usergames', UserGameList.as_view()),
    path('reports/userevents', GamerEventList.as_view()),
]
