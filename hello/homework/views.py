from django.shortcuts import render

# Create your views here.
def ViewHomework(request):
    return render(request,'homework/view_homework.html')