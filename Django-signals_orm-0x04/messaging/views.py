# accounts/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return render(request, 'accounts/confirm_delete.html')