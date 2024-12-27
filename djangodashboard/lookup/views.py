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
            f"https://www.airnowapi.org/aq/observation/zipCode/current/"
            f"?format=application/json&api_key={cfg["api_key"]}&zipCode={zipcode}"
        )
        print(api_request)
        try:
            api = json.loads(api_request.content)
            cat_rec = api[0]['Category']['Name']
        except KeyError:
            api = "Error..."

        translate_cat_to_descr = {
            "Good": "air quality is good",
            "Moderate": "getting moderate",
            "Unhealthy for Sensitive Groups": "be careful out there if you are in a sensitive group",
            "Very Unhealthy": "everyone stay inside for now",
            "Hazardous": "Air quality is hazardous."

        }

        category_color = cat_rec.lower().replace(" ", "")
        category_description = translate_cat_to_descr[cat_rec]

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
        api_request = requests.get(f"https://www.airnowapi.org/aq/observation/zipCode/current/?"
                                   f"format=application/json&api_key={cfg["api_key"]}&zipCode=02474")
        print(api_request)
        try:
            api = json.loads(api_request.content)
        except KeyError:
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
