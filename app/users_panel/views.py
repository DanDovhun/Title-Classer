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
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            search_input = form.cleaned_data["paragraph"]

            cat = classify(search_input)
            category = categories[cat[0]]

            print(category)

        else:
            return redirect("/")

        return render(request, 'user_dashboard.html', {
            'search_input': search_input,
            "category": category,
        })

    else:
        form = ArticleForm()

        return render(request, 'user_dashboard.html', {
            "form": form,
        })
