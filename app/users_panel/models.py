from django.db import models


class UserReport(models.Model):
    USER_PREDICTION_CATEGORIES = [
        ("", "Choose a Category"),
        ("Business", "Business"),
        ("Entertainment", "Entertainment"),
        ("Politics", "Politics"),
        ("Sport", "Sport"),
        ("Technology", "Technology"),
    ]

    reportParagraph = models.TextField()
    reportModelPrediction = models.CharField(max_length=20)
    reportUserPrediction = models.CharField(
        choices=USER_PREDICTION_CATEGORIES, max_length=20
    )
    reportURL = models.URLField(blank=True)
    reportComment = models.TextField(blank=True)
    reportTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User Report - {self.reportParagraph[:20]} ..."
