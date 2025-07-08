# Djashboard

Django web app to display as many jumbotron alert widgets on the same dashboard as you define in a JSON config file.

![Blade Runner Jumbotron](20120427125043blade-runner-470x251.webp)

## Table of Contents
- [Future Plans](#future-plans)
- [Disclaimer](#disclaimer)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
  - [Running the Project](#running-the-project)
- [Running the Tests](#running-the-tests)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Future Plans
- [ ] Implement user authentication to allow personalized dashboards.
- [ ] Add detailed documentation for advanced JSON configuration options.

## Disclaimer
This project is under active development. Details and functionality might change as it evolves.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites
- Python 3.x installed on your system.
- Django framework installed (can be installed via the `requirements.txt` file).
- Docker (optional, for containerized deployment).

### Installing
1. Clone the repository:
   ```bash
   git clone https://github.com/ErikPohl444/Djashboard.git
   cd Djashboard
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Configuring an environment_file

An environment file is mandatory and controls the output of the Djashboard.

See these instructions to create one for your usage.  [Environment File Creation Instructions](./docs/environment_template_instructions.md)

Here's additional context:
[Djashboard Concept](./docs/concept.md)

### Running the Project

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Running the Tests
Run the automated tests to ensure everything is functioning as expected:
```bash
python manage.py test
```

## Contributing
I’m excited to receive pull requests! For now, there are no strict contribution guidelines. Feel free to fork the repo, make your changes, and submit a pull request.

## Authors
- **Erik Pohl** - *Initial work*

See the list of [contributors](https://github.com/ErikPohl444/Djashboard/graphs/contributors) who have participated in this project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Acknowledgments
- Thanks to everyone who has motivated me to learn more.
- Special thanks to the Django community for their excellent documentation and support.
