from django.shortcuts import render
from . import views
import json
import requests


def do_transform_logic(result_json, transform_logic):
    fun = lambda jresult: eval(transform_logic)
    return fun(result_json)

def home(request):
    # get config data
    # see env_template.json for a template of a functioning env.json file

    api_calls = []
    api_transformations = []
    with open("env2.json") as json_handle:
        api_calls_widget_config = json.load(json_handle)
        api_calls_widget_config = api_calls_widget_config["api_data"]
        for widget_info in api_calls_widget_config:
            api_call = widget_info["api_call"]
            api_call_args = widget_info["args"]
            for arg_no, arg in enumerate(api_call_args):
                token = "{" + str(arg_no) + "}"
                api_call = api_call.replace(token, api_call_args[arg])
            transform = widget_info["transform"]
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
            api_result = json.loads(api_request.content)
            cat_rec = do_transform_logic(
                api_result,
                api_transformations[api_no]["cat_rec"]
            )
        except KeyError:
            api_result = "Error..."
        category_name = cat_rec
        category_subtext = do_transform_logic(
            api_result,
            api_transformations[api_no]["cat_subtext"]
        )
        cat_color_matrix = api_transformations[api_no]["color_translate"]
        category_color = cat_color_matrix[cat_rec]
        cat_descr_matrix = api_transformations[api_no]["descr_translate"]
        category_description = cat_descr_matrix[cat_rec]
        api_status = api_result
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
