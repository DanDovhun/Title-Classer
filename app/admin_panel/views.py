from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from users_panel.models import UserReport
from .models import AdminUser, ModelInfo
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from model.model import train, add_report
from sklearn.metrics import ConfusionMatrixDisplay
from .forms import EnterArticleForm

import matplotlib.pyplot as plt
import seaborn as sns


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
def admin_dashboard(request):
    # return render(request, 'admin_dashboard.html')
    return redirect("/admin/model")


@login_required
def admin_model(request):
    if request.method == "POST":
        form = EnterArticleForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["text"]
            label = form.cleaned_data["labels"]
            try:
                add_report(text, label)
            except Exception as e:
                messages.error(request, f"Error adding to dataset: {e}")
            else:
                messages.success(request, "Successfully added to dataset")

    form = EnterArticleForm()
    ai_model = ModelInfo.objects.all()
    model_info = ai_model[0]

    acc = []

    if model_info.old_acc == -1:
        acc.append("N/A")

    else:
        acc.append(round(model_info.old_acc, 5))

    return render(
        request,
        "admin_model.html",
        {
            "conf_mat": model_info.conf_matrix,
            "train_time": model_info.training_time,
            "old_acc": round(100 * acc[0], 5),
            "accuracy": round(100 * model_info.accuracy, 5),
            "precision": round(100 * model_info.precision, 5),
            "recall": round(100 * model_info.recall, 5),
            "f_one": round(100 * model_info.f_one, 5),
            "form": form,
        },
    )


@login_required
@csrf_protect
def admin_reports(request):
    if request.method == "POST":
        if "reject_report" in request.POST:
            report_id = request.POST.get("report_id")

            try:
                UserReport.objects.filter(id=report_id).delete()
            except Exception as e:
                messages.error(request, f"Error rejecting report: {e}")
            else:
                messages.success(request, "Succefully rejected User report")
                return redirect("admin_reports")

        elif "accept_report" in request.POST:
            report_id = request.POST.get("report_id")
            report = UserReport.objects.get(id=report_id)

            text = report.reportParagraph
            actual_label = report.reportUserPrediction

            categories = {
                "Politics": 0,
                "Sports": 1,
                "Technology": 2,
                "Entertainment": 3,
                "Business": 4,
            }

            cat = categories[actual_label]

            try:
                add_report(text, cat)
            except Exception as e:
                messages.error(request, f"Error adding to dataset: {e}")
            else:
                UserReport.objects.filter(id=report_id).delete()
                messages.success(request, "Successfully added to dataset.")

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

            print(request.POST)

            try:
                AdminUser.objects.create_user(
                    username=username, password=password, email=email
                )
            except IntegrityError:
                messages.error(request, "Error creating Admin: Duplicate username")
            except Exception as e:
                messages.error(request, f"Error creating Admin: {e}")
            else:
                messages.success(request, f"Successfully created Admin: {username}")
                return redirect("admin_admins")
        elif "delete_admin" in request.POST:

            admin_id = request.POST.get("admin_id")

            try:
                AdminUser.objects.filter(id=admin_id).delete()
            except Exception as e:
                messages.error(request, f"Error deleting Admin: {e}")

            else:
                messages.success(request, "Successfully deleted Admin")
                return redirect("admin_admins")
    admin_users = AdminUser.objects.all()
    return render(request, "admin_admins.html", {"admin_users": admin_users})


@login_required
def retrain(user):
    cf_loc = "admin_panel/static/conf_mat.png"
    training_time, score, conf_mat, recall, prec, acc, f_one = train(save=True)
    ai_model = ModelInfo.objects.all()

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
    sns.heatmap(
        conf_mat,
        cmap="Blues",
        fmt="",
        annot=True,
        cbar=False,
        annot_kws={"fontsize": 10, "fontweight": "bold"},
        square=False,
    )

    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(cf_loc)

    if len(ai_model) == 0:
        model = ModelInfo(
            conf_matrix=cf_loc,
            training_time=training_time,
            old_acc=-1,
            accuracy=acc,
            precision=prec,
            recall=recall,
            f_one=f_one,
        )

        model.save()

    else:
        ai_model[0].training_time = training_time
        ai_model[0].old_acc = ai_model[0].accuracy
        ai_model[0].accuracy = acc
        ai_model[0].precision = prec
        ai_model[0].recall = recall
        ai_model[0].f_one = f_one

        ai_model[0].save()

    return redirect("/admin/model")
