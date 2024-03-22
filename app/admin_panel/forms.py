from django import forms

ARTICLE_OPTIONS =( 
    (0, "Politics"), 
    (1, "Sports"), 
    (2, "Technology"), 
    (3, "Entertainment"), 
    (4, "Business"), 
) 

class EnterArticleForm(forms.Form):  
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "search-input",
                "name": "search-input",
                "placeholder": "Enter the First paragraph of your article..."
            }
        )
    )

    labels = forms.ChoiceField(choices = ARTICLE_OPTIONS) 
