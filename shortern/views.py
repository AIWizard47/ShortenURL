# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import ShortURL

validate_url = URLValidator()

def home(request):
    short_url = None
    if request.method == "POST":
        original = request.POST.get("url", "").strip()

        # Basic validation
        if not original:
            messages.error(request, "Please provide a valid URL.")
        else:
            try:
                validate_url(original)
            except ValidationError:
                messages.error(request, "Invalid URL format. Include http:// or https://")
            else:
                # Reuse existing mapping if you want idempotency
                obj = ShortURL.objects.filter(original_url=original).first()
                if not obj:
                    obj = ShortURL.objects.create(original_url=original)  # short_code auto-generated

                # Build the full short URL using a named route for redirect
                # Ensure you have a URL pattern named 'goto' that accepts short_code
                short_path = reverse("goto", kwargs={"code": obj.short_code})
                short_url = request.build_absolute_uri(short_path)

                messages.success(request, "Your short URL is ready!")

    return render(request, "home.html", {"short_url": short_url})

# views.py (add this)
from django.http import Http404

def goto(request, code):
    try:
        obj = ShortURL.objects.get(short_code=code)
    except ShortURL.DoesNotExist:
        raise Http404("Short URL not found")
    return redirect(obj.original_url)
