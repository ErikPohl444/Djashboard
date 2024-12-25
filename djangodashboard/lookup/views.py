from django.shortcuts import render
from . import views

# Create your views here.
def home(request):
    import json
    import requests

    with open("env.json") as json_handle:
        cfg = json.load(json_handle)
    print(cfg)
    api_request = requests.get(f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&api_key={cfg["api_key"]}&zipCode=02474")
    print(api_request)
    try:
        api = json.loads(api_request.content)
    except:
        api = "Error..."

    return render(request, 'home.html', {'api': api})

def about(request):
    return render(request, 'about.html', {})