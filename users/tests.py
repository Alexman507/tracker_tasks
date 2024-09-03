from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasker.models import Task
from users.models import User


class TaskTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@osnova-3d.ru")
        self.task = Task.objects.create(
            name="Задоджить",
            deadline="2024-09-03T15:00:00Z",
            status="Продалося",
            responsible_manager=self.user,
            priority=1,
            notes="а каво писать",
            updated_at="2024-09-03T12:31:00.992Z",
            executor=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_task_retrieve(self):
        url = reverse("tasker:tasker-detail", args=(self.task.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("notes"), self.task.notes)

    def test_task_create(self):
        url = reverse("tasker:tasker-list")
        data = {
            "name": "Задоджить",
            "deadline": "2024-09-03T15:00:00Z",
            "status": "Продалося",
            "responsible_manager": 1,
            "priority": 1,
            "notes": "а каво писать",
            "updated_at": "2024-09-03T12:31:00.992Z",
            "executor": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_list(self):
        url = reverse("tasker:tasker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_update(self):
        url = reverse("tasker:tasker-detail", args=(self.task.pk,))
        data = {
            "notes": "посмотреть фильм",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("notes"), "посмотреть фильм")

    # def test_public_task_list(self):
    #     url = reverse("tasker:public")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_delete(self):
        url = reverse("tasker:tasker-detail", args=(self.task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)
