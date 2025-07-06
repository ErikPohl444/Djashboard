from django.shortcuts import render, HttpResponse
from .services.home_service import render_home_page


def home(request) -> HttpResponse:
    """ Render the home screen """
    return render_home_page(request)


def about(request) -> HttpResponse:
    """ Render the about screen"""
    return render(request, 'about.html', {})
