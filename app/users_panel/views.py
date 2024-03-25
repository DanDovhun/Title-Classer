from django.shortcuts import render, redirect
from model.model import classify

from .forms import ArticleForm

def user_dashboard(request):
    categories = {
        0: "Politics",
        1: "Sport",
        2: "Technology",
        3: "Entertainment",
        4: "Business"
    }

    possibly_other = False
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            search_input = form.cleaned_data["paragraph"]

            cat, second, second_prob = classify(search_input)
            category = categories[cat[0]]
            second_likely = categories[second]

            if second_prob > 0.2:
                possibly_other = True

        else:
            return redirect("/")

        return render(request, 'user_dashboard.html', {
            'search_input': search_input,
            "category": category,
            "second": second_likely,
            "prob": round(second_prob*100, 2),
            "second_exists": possibly_other,
        })

    else:
        form = ArticleForm()

        return render(request, 'user_dashboard.html', {
            "form": form,
        })
