from django.shortcuts import render
from . import views

# Create your views here.
def home(request):
    import json
    import requests

    api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&api_key=02A407DD-7F9F-4D01-ADAD-A582AD35789F&zipCode=02474")
    try:
        api = json.loads(api_request.content)
    except:
        api = "Error..."

    return render(request, 'home.html', {'api': api})

def about(request):
    return render(request, 'about.html', {})