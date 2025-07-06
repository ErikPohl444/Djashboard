from django.shortcuts import render
import json
import requests


def do_transform_logic(result_json: json, transform_logic: str) -> json:
    fun = lambda jresult: eval(transform_logic)
    try:
        result = fun(result_json)
    except IndexError as e:
        print(f"IndexError: error with transform logic {transform_logic} resulting in {e}")
        raise
    return result


def get_api_metadata(env_file_name) -> (list[str], list[json]):
    """ Open a widget configuration file and load all widgets into two lists"""

    api_calls: list[str] = []
    api_transformations: list[json] = []
    with open(env_file_name) as json_handle:
        api_calls_widget_config: json = json.load(json_handle)
        api_calls_widget_config = api_calls_widget_config["api_data"]
        for widget_info in api_calls_widget_config:
            api_call: str = widget_info["api_call"]
            api_call_args: str = widget_info["args"]
            for arg_no, arg in enumerate(api_call_args):
                token: str = "{" + str(arg) + "}"
                api_call: str = api_call.replace(token, api_call_args[arg])
            transform: json = widget_info["transform"]
            api_calls.append(api_call)
            api_transformations.append(transform)
    return api_calls, api_transformations


def get_dashboard_vals(api_calls, api_transformations) -> (list[dict], json):
    dashboard_vals: list[dict] = []

    for api_no, api_call in enumerate(api_calls):
        # extract
        api_result: json = requests.get(api_call)
        if api_result.status_code != 200 or (api_result.text == '[]'):
            print(f"Received a {api_result.status_code} instead of successful result")
            print(api_result.content.decode())
            dashboard_val: dict = {
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
        cat_rec_xf: str = api_transformations[api_no]["cat_rec"]
        cat_subtext_xf: str = api_transformations[api_no]["cat_subtext"]
        color_xf: str = api_transformations[api_no]["color_translate"]
        descr_xf: str = api_transformations[api_no]["descr_translate"]

        # perform transformations using evaluations
        api_result_json: json = json.loads(api_result.content)
        category_name: json = do_transform_logic(
            api_result_json,
            cat_rec_xf
        )
        category_subtext: json = do_transform_logic(
            api_result_json,
            cat_subtext_xf
        )

        # perform transformations using matrices
        category_color: str = color_xf[category_name]
        category_description: str = descr_xf[category_name]

        # we have our 5 values for each widget
        dashboard_val: dict = {
            'api_status': api_result_json,
            'category_color': category_color,
            'category_description': category_description,
            'category_subtext': category_subtext,
            'category_name': category_name
        }
        dashboard_vals.append(dashboard_val)
    return dashboard_vals, api_result_json


def render_home_page(request):
    # get config data
    # see env_template.json for a template of a functioning env.json file
    api_calls, api_transformations = get_api_metadata("env2.json")

    # extract
    if request.method == "POST":
        zipcode = request.POST['zipcode']
    else:
        zipcode = None

    # extract and transform
    dashboard_vals, api_result_json = get_dashboard_vals(api_calls, api_transformations)

    # display
    return render(
        request, 'home.html',
        {
            'api_status': api_result_json,
            'dashboard_vals': dashboard_vals
        }
    )
