from django.shortcuts import render
from . import views

# Create your views here.
def home(request):
    import json
    import requests

    if request.method == "POST":
        with open("env.json") as json_handle:
            cfg = json.load(json_handle)
        print(cfg)
        zipcode = request.POST['zipcode']
        api_request = requests.get(
            f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&api_key={cfg["api_key"]}&zipCode={zipcode}"
        )
        print(api_request)
        try:
            api = json.loads(api_request.content)
        except:
            api = "Error..."

        if api[0]['Category']['Name'] == "Good":
            category_description = "air quality is good"
            category_color = 'good'
        elif api[0]['Category']['Name'] == "Moderate":
            category_description = "moderate"
            category_color = 'moderate'
        elif api[0]['Category']['Name'] == "Unhealthy for Sensitive Groups":
            category_description = "Air quality is unhealthy."
            category_color = 'Unhealthy for Sensitive Groups'
        elif api[0]['Category']['Name'] == "Very Unhealthy":
            category_description = "Airquality is very unhealthy."
            category_color = 'veryunhealthy'
        elif api[0]['Category']['Name'] == "Hazardous":
            category_description = "Air quality is hazardous."
            category_color = 'hazardous'


        return render(
            request, 'home.html',
            {
                'api': api,
                'category_description': category_description,
                'category_color': category_color
            }
        )

    else:

        with open("env.json") as json_handle:
            cfg = json.load(json_handle)
        print(cfg)
        api_request = requests.get(f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&api_key={cfg["api_key"]}&zipCode=02474")
        print(api_request)
        try:
            api = json.loads(api_request.content)
        except:
            api = "Error..."

        if api[0]['Category']['Name'] == "Good":
            category_description = "air quality is good"
            category_color = 'good'
        elif api[0]['Category']['Name'] == "Moderate":
            category_description = "moderate"
            category_color = '#FFFF00;'
        elif api[0]['Category']['Name'] == "Unhealthy for Sensitive Group":
            category_description = "Air quality is unhealthy."
            category_color = '#FF9900;'
        elif api[0]['Category']['Name'] == "Very Unhealthy":
            category_description = "Airquality is very unhealthy."
            category_color = '#990066;'
        elif api[0]['Category']['Name'] == "Hazardous":
            category_description = "Air quality is hazardous."
            category_color = '#660000;'


        return render(
            request, 'home.html',
            {
                'api': api,
                'category_description': category_description,
                'category_color': category_color
            }
        )

def about(request):
    return render(request, 'about.html', {})