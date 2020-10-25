from django.urls import path
from .views import ListCollection, ListDetail

urlpatterns = [
    path("<int:boardId>/lists", ListCollection.as_view()),
    path("<int:boardId>/lists/<int:pk>", ListDetail.as_view()),
]
