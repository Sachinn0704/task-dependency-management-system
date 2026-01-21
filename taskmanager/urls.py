from django.contrib import admin
from django.urls import path
from myapp.views import home, task_list
from myapp.views import home, task_list, task_api
from myapp.views import dependency_api
from myapp.views import graph_view




urlpatterns = [
    path('', home),
    path('tasks/', task_list),
    path('admin/', admin.site.urls),
]
urlpatterns = [
    path('', home),
    path('tasks/', task_list),
    path('api/tasks/', task_api), 
    path('api/dependencies/', dependency_api),
    path('admin/', admin.site.urls),
    path('graph/', graph_view),

]
