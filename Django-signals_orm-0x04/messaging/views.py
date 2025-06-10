# accounts/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return render(request, 'accounts/confirm_delete.html')



def conversation_threads(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    threads = Message.objects.get_conversation_threads(request.user, other_user)
    return render(request, 'messaging/threads.html', {'threads': threads})

def message_thread(request, message_id):
    thread = Message.objects.get_full_thread(message_id)
    root_message = thread.first() if thread.exists() else None
    return render(request, 'messaging/thread.html', {
        'thread': thread,
        'root_message': root_message
    })