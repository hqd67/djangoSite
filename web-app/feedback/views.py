from django.shortcuts import render
from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            print(f"Feedback from {name} ({email}): {message}")
            
            return render(request, 'feedback/success.html', {
                'name': name,
                'email': email,
                'message': message
            })
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/form.html', {'form': form})