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
        zipcode = None
    # make a filter here
    
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
        except KeyError:
            api = "Error..."
        category_name = cat_rec
        fun = lambda jresult: eval(api_transformations[api_no]["cat_subtext"])
        category_subtext = fun(api)
        cat_color_matrix = api_transformations[api_no]["color_translate"]
        category_color = cat_color_matrix[cat_rec]
        cat_descr_matrix = api_transformations[api_no]["descr_translate"]
        category_description = cat_descr_matrix[cat_rec]
        api_status = api
        # we have our 4 values for each widget
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
