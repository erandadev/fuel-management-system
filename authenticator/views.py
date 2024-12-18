from django.shortcuts import render,redirect
from django.contrib.auth.forms  import AuthenticationForm
from django.contrib.auth import login


def login_view(request):
    # return render(request, 'login.html')
    if request.user.is_authenticated:
        return redirect("fuel_records")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('fuel_records')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', { 'login_form': form })
