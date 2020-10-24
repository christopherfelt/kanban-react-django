from django.urls import path
from .views import ListCollection, ListDetail

urlpatterns = [
    path("<int:boardId>", ListCollection.as_view()),
    path("<int:boardId>/listid/<int:pk>", ListDetail.as_view()),
]
