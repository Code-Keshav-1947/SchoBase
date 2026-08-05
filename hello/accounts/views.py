from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from notification.models import Notification

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                Notification.objects.create(
                    title = 'Welcome Message!',
                    user = request.user,
                    message = 'Welcome to SchoBase! We are thrilled to have you on board. Explore the platform and make the most of its features. If you have any questions or need assistance, feel free to reach out to our support team. Enjoy your journey with us!'
                )
                return redirect("/")


    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})

    return render(request, "accounts/login.html", {"form": form})