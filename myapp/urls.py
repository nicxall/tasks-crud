from django.urls import path
from .AccountOperations import (SigninUser, TemplateHome, Signup, SessionCloseUser)
from .TaskOperations import (task_operation_view)

urlpatterns = [
	path('home/', TemplateHome.as_view(), name = 'home'),
	path('', SigninUser.as_view(), name = "signin"),
	path('signup/', Signup, name = 'signup'),
	path('logout/', SessionCloseUser, name = 'logout'),
	#endpoint de task
	path('task/<str:operation_type>/', task_operation_view, name='task_operation'),
    path('task/<str:operation_type>/<int:pk>/', task_operation_view, name='task_operation_detail'),
]  