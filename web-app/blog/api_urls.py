from django.urls import path
from . import api_views
from . import jwt_views


urlpatterns = [
    path("articles/", api_views.api_articles_list),
    path("articles/<int:id>/", api_views.api_article_detail),
    path("articles/category/<str:category>/", api_views.api_articles_by_category),
    path("articles/sort/date/", api_views.api_articles_sort_date),

    path("comment/", api_views.api_comment_list),
    path("comment/<int:id>/", api_views.api_comment_detail),

    path("token/", jwt_views.get_tokens),
    path("token/refresh/", jwt_views.refresh_access_token),

]
