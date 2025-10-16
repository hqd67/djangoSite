from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views import View
from django.http import HttpResponse

def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/detail_view.html'
    context_object_name = 'article'
    def get_object(self, queryset=None):
        try:
            return Articles.objects.get(pk=self.kwargs['pk'])
        except Articles.DoesNotExist:
            class MockArticle:
                def __init__(self, pk):
                    self.pk = pk
                    self.title = f"Статья {pk} (не найдена)"
                    self.content = "Эта статья не существует"
            
            return MockArticle(self.kwargs['pk'])

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'

    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news_delete.html'

def create(request):
    error = ''
    if request.method == 'POST':
        form =ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была не верной'


    form =ArticlesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'news/create.html', data)