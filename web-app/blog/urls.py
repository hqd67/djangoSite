from django.urls import path
from . import views

urlpatterns = [
    path("articles/", views.articles_list, name="articles"),
    path("articles/<str:category>/", views.articles_by_category, name="articles_by_category"),

    path("create-article/", views.create_article, name="create_article"),
    path("edit-article/<int:id>/", views.edit_article, name="edit_article"),
    path("delete-article/<int:id>/", views.delete_article, name="delete_article"),

    path("article/<int:id>/", views.article_detail, name="article_detail"),

    path("articles/<str:category>/", views.articles_by_category, name="articles_by_category"),


    path("login/", views.blog_login, name="blog_login"),
    path("logout/", views.blog_logout, name="blog_logout"),
    path("register/", views.register, name="register"),
]
