from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from tasker.models import Task
from tasker.paginations import TaskPaginator
from tasker.permissions import IsOwner
from tasker.serializers import TaskSerializer


# TaskerViewSet, PublicTaskerListAPIView

class TaskerViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = TaskPaginator
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("action",)
    ordering_fields = ("time",)


class PublicTaskerListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(priority=1)
    pagination_class = TaskPaginator
