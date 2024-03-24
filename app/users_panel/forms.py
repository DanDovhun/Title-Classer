from django import forms
from .models import UserReport


class ArticleForm(forms.Form):
    paragraph = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "search-input",
                "name": "search-input",
                "placeholder": "Enter the First paragraph of your article...",
            }
        )
    )


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        # Setting the readonly values for The user report based on input
        self.initial["reportParagraph"] = kwargs.get("initial", {}).get(
            "reportParagraph", ""
        )
        self.initial["reportModelPrediction"] = kwargs.get("initial", {}).get(
            "reportModelPrediction", ""
        )

    class Meta:
        model = UserReport
        fields = [
            "reportParagraph",
            "reportModelPrediction",
            "reportUserPrediction",
            "reportURL",
            "reportComment",
        ]
        labels = {
            "reportParagraph": "Your Input: ",
            "reportModelPrediction": "Predicted Category:",
            "reportUserPrediction": "Your Category:",
            "reportURL": "URL (Optional):",
            "reportComment": "Comment (Optional):",
        }

        widgets = {
            "reportParagraph": forms.Textarea(
                attrs={"class": "reportParagraph", "readonly": True, "rows": 5}
            ),
            "reportModelPrediction": forms.TextInput(
                attrs={"class": "reportModelPrediction", "readonly": True}
            ),
            "reportUserPrediction": forms.Select(
                attrs={"class": "reportUserPrediction"}
            ),
            "reportURL": forms.URLInput(
                attrs={"class": "reportURL", "placeholder": "Enter the article's URL"}
            ),
            "reportComment": forms.Textarea(
                attrs={
                    "class": "reportComment",
                    "placeholder": "Enter additional comments",
                    "rows": 5,
                }
            ),
        }
