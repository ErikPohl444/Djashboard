from django.shortcuts import render, HttpResponse
import json
import requests


def do_transform_logic(result_json: json, transform_logic: str) -> json:
    fun = lambda jresult: eval(transform_logic)
    return fun(result_json)


def get_api_metadata(env_file_name) -> (list[str], list[json]):
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


def home(request) -> HttpResponse:
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
    dashboard_vals: list[dict] = []
    for api_no, api_call in enumerate(api_calls):
        # extract
        api_result: json = requests.get(api_call)
        if api_result.status_code != 200:
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
        color_xf: str = api_transformations[api_no]["color"]
        descr_xf: str = api_transformations[api_no]["descr"]

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

    # display
    return render(
        request, 'home.html',
        {
            'api_status': api_result_json,
            'dashboard_vals': dashboard_vals
        }
    )


def about(request) -> HttpResponse:
    return render(request, 'about.html', {})
