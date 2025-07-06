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


def get_api_metadata(env_file_name: str) -> (list[str], list[json]):
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


def create_exception_widget(api_result: json, category_description: str, exception_message: str) -> dict:
    print(api_result.content.decode())
    print(exception_message)
    widget_value: dict = {
        'api_status': 'Exception',
        'category_color': 'darkred',
        'category_description': category_description,
        'category_subtext': 'API Error',
        'category_name': 'API Error'
    }
    return widget_value


def build_valid_widget(api_result: json, widget_api_result_transformations: dict, widget_api_index: int) -> dict:
    # var assignments
    cat_rec_xf: str = widget_api_result_transformations[widget_api_index]["cat_rec"]
    cat_subtext_xf: str = widget_api_result_transformations[widget_api_index]["cat_subtext"]
    color_xf: str = widget_api_result_transformations[widget_api_index]["color_translate"]
    descr_xf: str = widget_api_result_transformations[widget_api_index]["descr_translate"]

    # perform transformations using evaluations
    widget_api_result: json = json.loads(api_result.content)
    category_name: json = do_transform_logic(
        widget_api_result,
        cat_rec_xf
    )
    category_subtext: json = do_transform_logic(
        widget_api_result,
        cat_subtext_xf
    )

    # perform transformations using matrices
    category_color: str = color_xf[category_name]
    category_description: str = descr_xf[category_name]

    # we have our 5 values for each widget
    widget_value: dict = {
        'api_status': widget_api_result,
        'category_color': category_color,
        'category_description': category_description,
        'category_subtext': category_subtext,
        'category_name': category_name
    }
    return widget_value


def get_widget_values(widget_api_calls, widget_api_result_transformations) -> (list[dict], json):
    widget_values: list[dict] = []
    overall_dashboard_health = 'No valid widgets processed'

    for widget_api_index, widget_api_call in enumerate(widget_api_calls):
        # extract
        api_result: json = requests.get(widget_api_call)
        if api_result.status_code != 200:
            widget_values.append(
                create_exception_widget(
                    api_result,
                    f'status of {api_result.status_code} and content of {api_result.content}',
                    f"Received a {api_result.status_code} instead of successful result"
                )
            )
            continue
        if api_result.text == '[]':
            widget_values.append(
                create_exception_widget(
                    api_result,
                    f'text of response is {api_result.text} despite 200 status code',
                    f"Received an empty list instead of successful result"
                )
            )
            continue

        widget_value = build_valid_widget(api_result, widget_api_result_transformations, widget_api_index)
        widget_values.append(widget_value)
        overall_dashboard_health = 'At least one widget was okay'

    return widget_values, overall_dashboard_health


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
    dashboard_widget_values, widget_api_result = get_widget_values(api_calls, api_transformations)

    # display
    return render(
        request, 'home.html',
        {
            'overall_dashboard_health': widget_api_result,
            'widgets': dashboard_widget_values
        }
    )
