from django.http import HttpResponse
from django.shortcuts import render
from .models import Task


def home(request):
    return HttpResponse("<h1>Welcome to Task Management System</h1>")


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer


@api_view(['GET', 'POST'])
def task_api(request):
    if request.method == 'GET':
        status_filter = request.query_params.get('status')
        tasks = Task.objects.all()

        if status_filter:
            valid_statuses = {value for value, _ in Task.STATUS_CHOICES}
            if status_filter not in valid_statuses:
                return Response(
                    {
                        'error': 'Invalid status filter.',
                        'allowed_statuses': sorted(valid_statuses),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            tasks = tasks.filter(status=status_filter)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .models import TaskDependency
from .serializers import TaskDependencySerializer


@api_view(['GET', 'POST'])
def dependency_api(request):
    # GET → list all dependencies
    if request.method == 'GET':
        deps = TaskDependency.objects.all()
        serializer = TaskDependencySerializer(deps, many=True)
        return Response(serializer.data)

    # POST → add a dependency
    if request.method == 'POST':
        serializer = TaskDependencySerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def graph_view(request):
    tasks = Task.objects.all()
    return render(request, 'graph.html', {'tasks': tasks})
