from django.urls import path
from .views import TaskCollection, TaskDetail

urlpatterns = [
    path("<int:listId>/tasks", TaskCollection.as_view()),
    path("<int:listId>/tasks/<int:pk>", TaskDetail.as_view()),
]