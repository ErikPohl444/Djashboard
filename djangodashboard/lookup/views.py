from django.shortcuts import render
from . import views
import json
import requests

# Create your views here.


def home(request):

    # see env_template.json for a template of a functioning env.json file
    with open("env.json") as json_handle:
        cfg = json.load(json_handle)
    api_key = cfg["api_key"]
    if request.method == "POST":
        zipcode = request.POST['zipcode']
    else:
        zipcode = cfg["initial_zip"]
    api_request = requests.get(
        f"https://www.airnowapi.org/aq/observation/zipCode/current/"
        f"?format=application/json&api_key={api_key}&zipCode={zipcode}"
    )
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


def about(request):
    return render(request, 'about.html', {})
