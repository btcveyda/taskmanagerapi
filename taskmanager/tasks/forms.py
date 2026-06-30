from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Task title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description"}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
