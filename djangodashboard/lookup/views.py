from django.shortcuts import render, HttpResponse
from . import views
import json
import requests


def do_transform_logic(result_json, transform_logic):
    fun = lambda jresult: eval(transform_logic)
    return fun(result_json)


def get_api_metadata(env_file_name):
    api_calls = []
    api_transformations = []
    with open(env_file_name) as json_handle:
        api_calls_widget_config = json.load(json_handle)
        api_calls_widget_config = api_calls_widget_config["api_data"]
        for widget_info in api_calls_widget_config:
            api_call = widget_info["api_call"]
            api_call_args = widget_info["args"]
            for arg_no, arg in enumerate(api_call_args):
                token = "{" + str(arg) + "}"
                api_call = api_call.replace(token, api_call_args[arg])
            transform = widget_info["transform"]
            api_calls.append(api_call)
            api_transformations.append(transform)
    return api_calls, api_transformations


def home(request):
    # get config data
    # see env_template.json for a template of a functioning env.json file
    api_calls, api_transformations = get_api_metadata("env2.json")

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
        api_result = requests.get(api_call)
        if api_result.status_code != 200:
            print(f"Received a {api_result.status_code} instead of successful result")
            print(api_result.content.decode())
            dashboard_val = {
                'api_status': 'Exception',
                'category_color': 'darkred',
                'category_description': api_result.content,
                'category_subtext': 'API Error',
                'category_name': 'API Error'
            }
            dashboard_vals.append(dashboard_val)
            api_result_json = 'Exception'
            continue

        # var assignments
        primary_keys = ['cat_rec', 'cat_subtext', 'color_translate', 'descr_translate']
        missing_keys = []
        for pk in primary_keys:
            if pk not in api_transformations[api_no].keys():
                missing_keys.append(pk)
        if missing_keys:
            raise KeyError
        else:
            cat_rec_xf = api_transformations[api_no]["cat_rec"]
            cat_subtext_xf = api_transformations[api_no]["cat_subtext"]
            cat_color_xf = api_transformations[api_no]["color_translate"]
            descr_xf = api_transformations[api_no]["descr_translate"]

        # perform transform logic
        api_result_json = json.loads(api_result.content)
        category_name = do_transform_logic(
            api_result_json,
            cat_rec_xf
        )
        category_subtext = do_transform_logic(
            api_result_json,
            cat_subtext_xf
        )

        # get transformation dicts/matrices
        category_color = cat_color_xf[category_name]
        category_description = descr_xf[category_name]

        # we have our 5 values for each widget
        dashboard_val = {
            'api_status': api_result_json,
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
            'api_status': api_result_json,
            'dashboard_vals': dashboard_vals
        }
    )


def about(request):
    return render(request, 'about.html', {})
