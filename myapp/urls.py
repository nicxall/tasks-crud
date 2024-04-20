from django.urls import path
from .AccountOperations import (SigninUser, TemplateHome, Signup, SessionCloseUser)
from .TaskOperations import (TaskCreate, TaskList, TaskDetail, DeleteTask)

urlpatterns = [
	path('home/', TemplateHome.as_view(), name = 'home'),
	path('', SigninUser.as_view(), name = "signin"),
	path('signup/', Signup.as_view(), name = 'signup'),
	path('logout/', SessionCloseUser, name = 'logout'),
	#endpoint de task
	path('create/task/', TaskCreate.as_view(), name = 'createtask'),
	path('task/list/', TaskList.as_view(), name = 'tasklist'),
	path('task/detail/<int:pk>/', TaskDetail.as_view(), name = 'taskdetail'),
	path('delete/task/<int:id>/', DeleteTask, name = 'deletetask'),
]  