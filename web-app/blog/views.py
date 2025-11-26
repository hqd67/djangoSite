from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm, CommentForm
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LogoutView
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import HttpResponse
from .forms import BlogLoginForm
from .models import Article, User
from .forms import ArticleForm, CommentForm, UserRegisterForm, BlogLoginForm
from .utils import blog_login_required


def articles_list(request):
    articles = Article.objects.all()

    categories = Article.objects.values_list("category", flat=True).distinct()

    return render(request, "blog/articles.html", {
        "articles": articles,
        "categories": categories,
    })



def articles_by_category(request, category):
    categories = Article.objects.values_list("category", flat=True).distinct()

    if category not in categories:
        return render(request, "blog/category_not_found.html", {"category": category})

    articles = Article.objects.filter(category=category)
    return render(request, "blog/articles.html", {"articles": articles, "category": category})


@blog_login_required
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("articles")
    else:
        form = ArticleForm()

    return render(request, "blog/create.html", {"form": form})


@blog_login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("articles")
    else:
        form = ArticleForm(instance=article)

    return render(request, "blog/edit.html", {"form": form})

@blog_login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect("articles")


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect("article_detail", id=id)
    else:
        form = CommentForm()

    return render(request, "blog/article_view.html", {
        "article": article,
        "comments": comments,
        "form": form
    })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.hashed_password = make_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")  
    else:
        form = UserRegisterForm()

    return render(request, "blog/register.html", {"form": form})

class LogoutViewAllowGet(LogoutView):
    http_method_names = ["get", "post"]

def blog_login(request):
    if request.method == "POST":
        form = BlogLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Пользователь не найден.")
                return redirect("blog_login")

            if check_password(password, user.hashed_password):
                request.session["blog_user_id"] = user.id
                return redirect("articles")
            else:
                messages.error(request, "Неверный пароль.")
                return redirect("blog_login")

    form = BlogLoginForm()
    return render(request, "blog/login_blog.html", {"form": form})

def blog_logout(request):
    if "blog_user_id" in request.session:
        del request.session["blog_user_id"]
    return redirect("blog_login")

def articles_by_category(request, category):
    categories = Article.objects.values_list("category", flat=True).distinct()

    if category not in categories:
        return render(request, "blog/category_not_found.html", {"category": category})

    articles = Article.objects.filter(category=category)
    
    return render(request, "blog/articles.html", {
        "articles": articles,
        "category": category,
        "categories": categories
    })
