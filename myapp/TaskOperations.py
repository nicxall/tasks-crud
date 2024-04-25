from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .models import TaskModel
from django.views.generic import UpdateView, TemplateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.utils import timezone
from django.http import HttpResponse
from .forms import TaskForm
import asyncio



# Funciones auxiliares

def get_user_tasks(request):
    return TaskModel.objects.filter(user=request.user).order_by('-created', 'title')

# Vistas

class TaskCreate(View):
    template_task_create = "taskcreate.html"

    def get(self, request):
        return render(request, self.template_task_create)

    def post(self, request):
        try:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                form_valid = task_form.save(commit=False)
                form_valid.user = request.user
                form_valid.save()
                return redirect('home')
        except Exception as e:
            # Manejo de excepciones más específico
            if isinstance(e, ValidationError):
                messages.error(request, e.messages)
            else:
                messages.error(request, "Ocurrió un error al crear la tarea")
            return render(request, self.template_task_create, {'form': task_form})

class TaskList(View):
    template_task_list = "tasklist.html"

    def get(self, request):
        tasks = get_user_tasks(request)
        return render(request, self.template_task_list, {'tasks': tasks})

class TaskDetail(View):
    def get(self, request, pk):
        task = get_object_or_404(get_user_tasks(request), pk=pk)
        return render(request, 'taskdetail.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(get_user_tasks(request), pk=pk)
        task_form = TaskForm(request.POST, instance=task)
        task_form.save()
        return redirect('home')

def DeleteTask(request, id):
    task_to_delete = get_object_or_404(TaskModel, pk=id)
    task_to_delete.delete()
    return redirect('tasklist')