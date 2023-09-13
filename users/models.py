from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    bio = models.TextField(null=True)
    email = models.EmailField(max_length=120)
    profile_picture = models.ImageField(upload_to="users", default="profile_placeholder.png")

    def __str__(self):
        return f"User: {self.username} ({self.name} - {self.email})"
