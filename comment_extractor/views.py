from django.views.decorators.http import require_http_methods
from django.shortcuts import render


@require_http_methods(["GET"])
def homepage(request):
    return render(request, 'index.html')
