-----

# API Data Configuration

This document outlines the structure for configuring API calls and their subsequent data transformations.

-----

## JSON Structure Overview

```json
{
  "api_data": [
    {
      "api_call": "string",
      "args": {
        "api_key": "string",
        "initial_zip": "string"
      },
      "transform": {
        "cat_rec": "string",
        "cat_subtext": "string",
        "color_translate": {
          "string": "string"
        },
        "descr_translate": {
          "string": "string"
        }
      }
    }
  ]
}
```

-----

## Field Descriptions

### `api_data` Array

This is the root element, an array containing configurations for individual API calls. Each object within this array represents a single API integration with its arguments and transformation rules.

-----

### `api_data` Object Properties

| Property Name | Type     | Description |
| :------------ | :------- | :---------- |
| **`api_call`** | `string` | The full URL endpoint for the API request. It uses placeholders (e.g., `{api_key}`, `{initial_zip}`) that are populated by values from the `args` field. |
| **`args`** | `object` | An object containing key-value pairs for the arguments to be substituted into the `api_call` URL. |
| **`transform`** | `object` | An object containing rules to transform the raw JSON response from the API into a more digestible format. |

-----

### Sample `args` Object Properties

| Property Name | Type     | Description |
| :------------ | :------- | :---------- |
| **`api_key`** | `string` | The API key required for authentication with the `airnowapi.org` service. |
| **`initial_zip`** | `string` | The default zip code to be used in the API request. |

-----

### `transform` Object Properties

| Property Name     | Type     | Description                                                                                                                                                                                                     |
| :---------------- | :------- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`cat_rec`** | `string` | A string representing a Python-like expression to extract the Jumbotron category name from the API's JSON response (e.g., `jresult[0]['Category']['Name']`).                                                    |
| **`cat_subtext`** | `string` | A Python f-string template to generate a descriptive subtext about the current category, which can contain JSON references (e.g., `f"Current {jresult[0]['ReportingArea']} Air quality: {jresult[0]['AQI']}"`). |
| **`color_translate`** | `object` | A mapping from the cat_rec to a Jumbotron color string.                                                                                                                                                         |
| **`descr_translate`** | `object` | A mapping from the cat_rec to a custom descriptive phrase for the Jumbotron.                                                                                                                                    |

-----

### Example Values

To illustrate the actual data, here's an example of an `api_data` entry with real values:

```json
{
  "api_data": [
    {
      "api_call": "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&API_KEY={api_key}&zipCode={initial_zip}",
      "args": {
        "api_key": "[yourkey]",
        "initial_zip": "02474"
      },
      "transform": {
        "cat_rec": "jresult[0]['Category']['Name']",
        "cat_subtext": "f\"Current {jresult[0]['ReportingArea']} Air quality: {jresult[0]['AQI']}\"",
        "color_translate": {
          "Good": "green",
          "Moderate": "yellow",
          "USG": "violet",
          "Unhealthy": "burgundy",
          "Very Unhealthy": "brightred",
          "Hazardous": "darkred"
        },
        "descr_translate": {
          "Good": "air quality is good",
          "Moderate": "getting moderate",
          "Unhealthy for Sensitive Groups": "be careful out there if you are in a sensitive group",
          "Very Unhealthy": "everyone stay inside for now",
          "Hazardous": "Air quality is hazardous."
        }
      }
    }
  ]
}
```