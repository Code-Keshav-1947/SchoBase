from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

from django.shortcuts import render

# Yeh function CSRF fail hone par aapka custom 403 page dikhayega
def custom_csrf_failure(request, reason=""):
    return render(request, '403.html', status=403)
