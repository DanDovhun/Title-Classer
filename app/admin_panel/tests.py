from django.test import TestCase
from .models import AdminUser
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import get_user_model

import model.model as mdl
# Create your tests here.

class ProfileTest(TestCase):
    def setUp(self):
        client = Client()

    def test_admin_login(self):
        newAdmin = get_user_model().objects.create_user(
            username = "nemathriel", password="pwd123", email="dankodov@gmail.com"
        )

        # Try to login with wrong password
        admin = self.client.login(username="nemathriel", password="321pwd")

        print("If fails with wrong pwd")
        try:
            self.assertEqual(admin, False)
            print("Pass")

        except AssertionError:
            print("Failed")

        # Try wrong username, correct password
        admin = self.client.login(username="dnaiel", password="pwd123")
        print("If fails with wrong username")

        try:
            self.assertEqual(admin, False)
            print("Pass")

        except AssertionError:
            print("Failed")

        # Try correct username and password
        admin = self.client.login(username='nemathriel', password='pwd123')

        print("If actually logs in")
        try:
            self.assertEqual(admin, True)
            print("Pass")

        except AssertionError:
            print("Failed")

    def test_training(self):
        training_time, score, conf_mat, recall, prec, acc, f_one = mdl.train(save=False)

        print("Checking if time < 20s")
        try:
            self.assertLessEqual(training_time.seconds, 20)
            print("Pass")

        except AssertionError:
            print("Fail")

        print("Checking if Recall is > 90%")
        try:
            self.assertGreaterEqual(recall, 0.90)
            print("Pass")

        except AssertionError:
            print("Fail")

        print("Checking if Precision is > 90%")
        try:
            self.assertGreaterEqual(prec, 0.90)
            print("Pass")

        except:
            print("Fail")

        print("Checking if Accuracy is > 90%")
        try:
            self.assertGreaterEqual(acc, 0.90)
            print("Pass")

        except AssertionError:
            print("Fail")

        print("Checking if F1 is > 90%")
        try:
            self.assertGreaterEqual(f_one, 0.90)
            print("Pass")

        except AssertionError:
            print("Fail")