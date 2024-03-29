from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from admin_panel.models import AdminUser

import model.model as mdl

# Create your tests here.

class Article():
    def __init__(self, article, label):
        self.article = article
        self.label = label

    def classify(self):
        # Call mdl.classify and return the first variable
        cat, _, _ = mdl.classify(self.article)
        return cat[0]

class ArticleTest(TestCase):
    def setup(self):
        pass
    
    def test_articles(self):
        art_a = Article("The software development landscape is on the cusp of a revolution. Enter Devin AI and Microsoft AutoDev, two groundbreaking advancements in AI-powered coding that promise to reshape how software is built. But with such distinct approaches, which reigns supreme? Let’s delve into the intricate details of Devin and AutoDev, exploring their strengths, weaknesses, and potential for collaboration:",2)
        art_b = Article("It was the summer of 2008, and I was one year away from receiving my MFA in Graphic Design from the Rhode Island School of Design (RISD). It was the same summer I landed an internship at Apple on a team I was eager to meet. The same design team responsible for the iPhone; a magical device that launched the year prior at Macworld Expo in San Francisco. One could only imagine the size of my butterflies as I flew to Cupertino and arrived at 1 Infinite Loop. To add to the uncontrollable fluttering, I had no idea what project I would be given, the size of the team, where I would sit, or if I could really bike to work (I’m terrible on bikes).", 2)
        art_c = Article("The hardest part of my data scientist job is convincing the non-technical stakeholders to realize how yet another data science solution can help them make better decisions.This is not new to me, though. It’s been like this in my 5+ years of experience as a data scientist and machine learning engineer.", 2)
        art_d = Article("Nepotism in sports broadcasting: ‘A tremendous advantage,’ but ‘what do you do with it?’", 1)
        art_e = Article("Virgil van Dijk x LeBron James: The unlikely bond inspiring Liverpool’s captain", 1)
        art_f = Article("A mysterious illness halted his promising NHL career. Eight years later, hope and a comeback", 1)
        print(art_a.label)
        try:
            self.assertEqual(art_a.classify(), 2)
            print("Pass")

        except AssertionError:
            print("Failed")

        try:
            self.assertEqual(art_b.classify(), 2)
            print("Pass")

        except AssertionError:
            print("Failed")

        try:
            self.assertEqual(art_c.classify(), 2)
            print("Pass")

        except AssertionError:
            print("Failed")

        try:
            self.assertEqual(art_d.classify(), 2)
            print("Pass")

        except AssertionError:
            print("Failed")

        try:
            self.assertEqual(art_e.classify(), 2)
            print("Pass")

        except AssertionError:
            print("Failed")

        try:
            self.assertEqual(art_f.classify(), 2)
            print("Pass")

        except AssertionError:
            print("Failed")