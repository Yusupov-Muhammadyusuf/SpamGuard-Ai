from django.shortcuts import render
from .services import get_emails_with_prediction

def inbox_view(request):
    emails = None

    if request.method == "POST":
        email = request.POST.get("email")
        app_password = request.POST.get("password")

        emails = get_emails_with_prediction(email, app_password, limit=10)
    
    return render(request, "email_ai/inbox.html", {"emails": emails})