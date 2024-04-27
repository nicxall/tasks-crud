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

class TaskOperationFactory:
    @staticmethod
    def create_operation(operation_type):
        if operation_type == 'create':
            return TaskCreate()
        elif operation_type == 'list':
            return TaskList()
        elif operation_type == 'detail':
            return TaskDetail()
        elif operation_type == 'delete':
            return TaskDelete()
        else:
            raise ValueError("Tipo de operacion denegada")

#Clase base para operaciones de tareas
class TaskOperation(View):
    template_name = None
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        raise NotImplementError("Metodo post no implementado")

# Funciones auxiliares
def get_user_tasks(request):
    return TaskModel.objects.filter(user=request.user).order_by('-created', 'title')

# Vistas
class TaskCreate(TaskOperation):
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

class TaskList(TaskOperation):
    template_task_list = "tasklist.html"
    
    def get(self, request):
        try:
            tasks = get_user_tasks(request)
            return render(request, self.template_task_list, {'tasks': tasks})
        except Exception as e:
            print(f'El error es: {e}')


class TaskDetail(TaskOperation):
    
    def get(self, request, pk):
        task = get_object_or_404(get_user_tasks(request), pk=pk)
        return render(request, 'taskdetail.html', {'task': task})
    
    def post(self, request, pk):
        task = get_object_or_404(get_user_tasks(request), pk=pk)
        task_form = TaskForm(request.POST, instance=task)
        task_form.save()
        return redirect('home')


class TaskDelete(TaskOperation):
    def post(self, request, pk):
        task = get_object_or_404(TaskModel, pk=pk, user = request.user)
        task.delete()
        return redirect('tasklist')

def task_operation_view(request, operation_type, *args, **kwargs):
    task_operation = TaskOperationFactory.create_operation(operation_type)
    return task_operation.dispatch(request, *args, **kwargs)