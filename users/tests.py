from django.test import TestCase
from .models import User

# Create your tests here.


class UserModelTest(TestCase):
    def setUpTestData():
        User.objects.create(name="John Doe", username="testuser",
                            email="john.doe@gmail.com", bio="Hi, i'm Joe!")

    def test_return_string(self):
        user = User.objects.get(id=1)
        self.assertEqual(
            user.__str__(), "User: testuser (John Doe - john.doe@gmail.com)")

    def test_bio_string(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.bio, "Hi, i'm Joe!")

    def test_bio_null_true(self):
        user = User.objects.get(username="testuser")
        allow_null = user._meta.get_field("bio").null
        self.assertTrue(allow_null)

    def test_name_max_length(self):
        user = User.objects.get(username="testuser")
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_email_max_length(self):
        user = User.objects.get(username="testuser")
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 120)
