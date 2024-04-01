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

    possibly_other = False

    if request.method == "POST":
        form = ArticleForm(request.POST)

    if request.method == "POST":
        article_form = ArticleForm(request.POST)

        if article_form.is_valid():
            search_input = article_form.cleaned_data["paragraph"]

            cat, second, second_prob = classify(search_input)
            category = categories[cat[0]]
            second_likely = categories[second]

            if second_prob > 0.2:
                possibly_other = True

            request.session["search_input"] = search_input
            request.session["category"] = category
            request.session["second"] = second_likely
            request.session["prob"] = round(second_prob * 100, 2)
            request.session["second_exists"] = possibly_other

            return redirect("user_prediction")

        """return redirect(request, 'user_dashboard.html', {
            'search_input': search_input,
            "category": category,
            "second": second_likely,
            "prob": round(second_prob*100, 2),
            "second_exists": possibly_other,
        })"""
    else:
        article_form = ArticleForm()
        return render(request, "user_dashboard.html", {"form": article_form})


def user_prediction(request):
    error = False
    if request.method == "POST":
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            model_prediction = report_form.cleaned_data["reportModelPrediction"]
            user_prediction = report_form.cleaned_data["reportUserPrediction"]

            if model_prediction == user_prediction:
                print("model and user prediction are the same")
                error_message = (
                    "Your prediction can't be the same as the model prediction"
                )
                error = True
                return render(
                    request,
                    "user_prediction.html",
                    {
                        "report_form": report_form,
                        "error_message": error_message,
                        "error": error,
                    },
                )
            else:

                report = report_form.save()
                return redirect("user_prediction")
        else:
            # Form is invalid, handle URL validation errors
            error = True
            return render(
                request,
                "user_prediction.html",
                {"report_form": report_form, "error": error},
            )
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
