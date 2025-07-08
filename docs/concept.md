# About Djashboards

A **djashboard** is a customizable Django web application dashboard made up of one or more widgets. At present, the only supported widget type is the **jumbotron**.  

## Widgets

- Each widget in a djashboard currently takes the form of a **jumbotron**.
- Every jumbotron widget is linked to a specific API call.
- The data returned from the API call is parsed by djashboard according to options set in a configuration file provided by the user.
- The configurations consist of dynamically coded translations and transformations which render predictably formatted jumbotrons based on api result data of your choosing.

## Configuration Options

For each widget (jumbotron), users can specify several options in the configuration file:

- **Jumbotron Color:** Sets the color/style of the jumbotron widget based on attributes of the api result you choose.
- **Jumbotron Category Name:** Defines the main category or title shown on the jumbotron, defined by dynamic coding in your configuration.
- **Jumbotron Category Subtext:** Adds a secondary, smaller text beneath the category name, selected from the api results by instructions in your configuration.
- **Jumbotron Description:** Provides a detailed description or message to display in the widget based on a translation you code into your configuration.

## How it Works

1. Djashboard reads the configuration file containing the widget definitions and their respective options.
2. For every widget configuration, djashboard makes the associated API call.
3. The API response is parsed using the configuration options specified by the user.
4. Based on these options and the API data, a jumbotron widget is rendered and displayed on the dashboard.

**In summary:**  
For each widget configuration in your config file, a jumbotron widget will be displayed on your djashboard, styled and populated according to the API response and your chosen options.

**See a sample config file**

 [Sample config file instructions](./docs/environment_template_instructions.md)
