from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from .models import Article, Comment



@csrf_exempt
def api_articles_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        data = [model_to_dict(a) for a in articles]
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        user_id = request.user_id
        try:
            body = json.loads(request.body)
            title = body.get("title")
            text = body.get("text")
            category = body.get("category")
            

            if not (title and text and category and user_id):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            article = Article.objects.create(
                title=title,
                text=text,
                category=category,
                user_id=user_id
            )
            return JsonResponse(model_to_dict(article), status=201)

        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
def api_article_detail(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(model_to_dict(article))

    elif request.method == "PUT":
        user_id = request.user_id
        try:
            body = json.loads(request.body)

            article.title = body.get("title", article.title)
            article.text = body.get("text", article.text)
            article.category = body.get("category", article.category)
            article.user_id = body.get("user", article.user_id)
            article.save()

            return JsonResponse(model_to_dict(article))

        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == "DELETE":
        user_id = request.user_id
        article.delete()
        return JsonResponse({"success": True})

@csrf_exempt
def api_articles_by_category(request, category):
    articles = Article.objects.filter(category=category)
    data = [model_to_dict(a) for a in articles]
    return JsonResponse(data, safe=False)

@csrf_exempt
def api_articles_sort_date(request):
    articles = Article.objects.order_by("-created_date")
    data = [model_to_dict(a) for a in articles]
    return JsonResponse(data, safe=False)





@csrf_exempt
def api_comment_list(request):
    if request.method == "GET":
        comments = Comment.objects.all()
        data = [model_to_dict(c) for c in comments]
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        user_id = request.user_id
        try:
            body = json.loads(request.body)
            text = body.get("text")
            article_id = body.get("article")
            author_name = body.get("author_name")

            if not (text and article_id and author_name):
                return JsonResponse({"error": "Missing fields"}, status=400)

            comment = Comment.objects.create(
                text=text,
                article_id=article_id,
                author_name=author_name
            )

            return JsonResponse(model_to_dict(comment), status=201)

        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
def api_comment_detail(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(model_to_dict(comment))

    elif request.method == "PUT":
        user_id = request.user_id
        try:
            body = json.loads(request.body)
            comment.text = body.get("text", comment.text)
            comment.author_name = body.get("author_name", comment.author_name)
            comment.article_id = body.get("article", comment.article_id)
            comment.save()
            return JsonResponse(model_to_dict(comment))

        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == "DELETE":
        user_id = request.user_id
        comment.delete()
        return JsonResponse({"success": True})
