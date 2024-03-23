from django.shortcuts import render, redirect
from model.model import classify

from .forms import ArticleForm, ReportForm
from .models import UserReport


def user_dashboard(request):
    categories = {
        0: "Politics",
        1: "Sport",
        2: "Technology",
        3: "Entertainment",
        4: "Business",
    }

    if request.method == "POST":
        article_form = ArticleForm(request.POST)

        if article_form.is_valid():
            search_input = article_form.cleaned_data["paragraph"]

            cat = classify(search_input)
            category = categories[cat[0]]

            print(category)

            request.session["search_input"] = search_input
            request.session["category"] = category

            return redirect("user_prediction")

    else:
        article_form = ArticleForm()
        return render(request, "user_dashboard.html", {"form": article_form})


def user_prediction(request):
    if request.method == "POST":
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report = report_form.save()
            return redirect("user_prediction")
        else:
            return render(request, "user_prediction.html", {"report_form": report_form})
    else:
        search_input = request.session.get("search_input", "")
        category = request.session.get("category", "")
        report_form = ReportForm(
            initial={
                "reportParagraph": search_input,
                "reportModelPrediction": category,
            }
        )
        return render(
            request,
            "user_prediction.html",
            {
                "search_input": search_input,
                "category": category,
                "report_form": report_form,
            },
        )
