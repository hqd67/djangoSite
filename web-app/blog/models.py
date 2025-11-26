from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.CharField(max_length=50, default="general")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=50)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author_name}: {self.text[:20]}"
