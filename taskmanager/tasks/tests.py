from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewsTests(TestCase):
    def test_home_page_displays_existing_tasks(self) -> None:
        Task.objects.create(title="Write report", description="Finish by noon")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Write report")
        self.assertContains(response, "Finish by noon")

    def test_home_page_can_create_a_task(self) -> None:
        response = self.client.post(
            reverse("home"),
            {"title": "Review PR", "description": "Check the diff"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Review PR")
