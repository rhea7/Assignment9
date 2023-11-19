## Description:
This iteration of the Barky application introduces the Command Query Responsibility Segregation (CQRS) pattern and Dependency Injection (DI) Bootstrapping, enhancing the architecture for better scalability and maintainability. The CQRS pattern separates the read (query) responsibilities from the write (command) responsibilities, while DI Bootstrapping sets up the application services and dependencies.

## Dependencies:
The application requires Flask and SQLAlchemy, as well as the previously established Barky application environment.

## Instructions:
To get the application up and running:

Ensure Python 3.6+ and pip are installed on your machine.
Clone the repository and navigate to the directory of the application.
Run pip install -r requirements.txt to install the necessary packages.
Execute python app.py to start the Flask server, which will serve the API on http://localhost:5000/.


## CQRS and DI Bootstrapping:
The application's read and write operations are now handled by separate models, with a message bus routing commands to their corresponding handlers.
Dependency Injection is utilized to bootstrap and configure the application's services and dependencies, providing a modular and testable structure.

## Testing:
Tests can be run using the following command:


python -m unittest discover
The tests are designed to ensure that the CQRS commands are processed correctly and that the DI Bootstrapped services interact as expected.