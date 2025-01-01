from django.shortcuts import render
from . import views
import json
import requests


# Create your views here.


def home(request):
    # get config data
    # see env_template.json for a template of a functioning env.json file

    api_calls = []
    api_transformations = []
    with open("env.json") as json_handle:
        cfg = json.load(json_handle)
    api_key = cfg["api_key"]
    with open("env2.json") as json_handle:
        cfg2 = json.load(json_handle)
        cfg2 = cfg2["api_data"]
        for api_info in cfg2:
            api_call = api_info["api_call"]
            args = api_info["args"]
            for arg_no, arg in enumerate(args):
                token = "{"+str(arg_no)+"}"
                api_call = api_call.replace(token, args[arg])
            transform = api_info["transform"]
            api_calls.append(api_call)
            api_transformations.append(transform)

    # extract
    if request.method == "POST":
        zipcode = request.POST['zipcode']
    else:
        zipcode = cfg["initial_zip"]
        # right now do nothing with zipcode

    # extract and transform
    dashboard_vals = []
    for api_no, api_call in enumerate(api_calls):
        # extract
        api_request = requests.get(
            api_call
        )

        # transform
        try:
            api = json.loads(api_request.content)
            fun = lambda jresult: eval(api_transformations[api_no]["cat_rec"])
            cat_rec = fun(api)

            # cat_rec = api[0]['Category']['Name']
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
        category_subtext = f"Current {api[0]['ReportingArea']} Air quality: {api[0]['AQI']}"
        category_name = cat_rec
        api_status = api
        dashboard_val = {
            'category_color': category_color,
            'category_description': category_description,
            'category_subtext': category_subtext,
            'category_name': category_name
        }
        dashboard_vals.append(dashboard_val)

    # display
    return render(
        request, 'home.html',
        {
            'api_status': api_status,
            'category_description': category_description,
            'category_subtext': category_subtext,
            'category_color': category_color,
            'category_name': category_name,
            'dashboard_vals': dashboard_vals
        }
    )


def about(request):
    return render(request, 'about.html', {})
