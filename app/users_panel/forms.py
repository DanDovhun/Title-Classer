from django import forms

class ArticleForm(forms.Form):  
    paragraph = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "search-input",
                "name": "search-input",
                "placeholder": "Enter the First paragraph of your article..."
            }
        )
    )

