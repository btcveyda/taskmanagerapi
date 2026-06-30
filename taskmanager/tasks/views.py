from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task


def home(request):
    tasks = Task.objects.order_by("-created_at")
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm()

    return render(request, "tasks/home.html", {"tasks": tasks, "form": form})
