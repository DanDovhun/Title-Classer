from django.shortcuts import render, redirect
from .models import AdminUser
from users_panel.models import UserReport
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Received username:", username)
        print("Received password:", password)

        admin = authenticate(request, username=username, password=password)
        if admin is not None:
            login(request, admin)
            print("Authentication successful")
            return redirect("admin_model")
        else:
            error_message = "Invalid username or password"
            print("Authentication failed")
            return render(request, "admin_login.html", {"error_message": error_message})
    else:
        return render(request, "admin_login.html")


def admin_logout(request):
    logout(request)
    return redirect("admin_login")


@login_required
def admin_model(request):
    return render(request, "admin_model.html")


@login_required
@csrf_protect
def admin_reports(request):
    if request.method == "POST":
        if "reject_report" in request.POST:
            report_id = request.POST.get("report_id")
            UserReport.objects.filter(id=report_id).delete()
            return redirect("admin_reports")
    user_reports = UserReport.objects.all()
    return render(request, "admin_reports.html", {"user_reports": user_reports})


@login_required
@csrf_protect
def admin_admins(request):
    if request.method == "POST":
        if "create_admin" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            try:
                AdminUser.objects.create_user(
                    username=username, password=password, email=email
                )
                return redirect("admin_admins")
            except Exception as e:
                print(f"Error creating admin user: {e}")
        elif "delete_admin" in request.POST:
            admin_id = request.POST.get("admin_id")
            AdminUser.objects.filter(id=admin_id).delete()
            return redirect("admin_admins")
    admin_users = AdminUser.objects.all()
    return render(request, "admin_admins.html", {"admin_users": admin_users})
