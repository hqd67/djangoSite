from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog.views import LogoutViewAllowGet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('', include('feedback.urls')),
    path('', include("blog.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("", include("blog.urls")),
    path("api/", include("blog.api_urls")),
]
