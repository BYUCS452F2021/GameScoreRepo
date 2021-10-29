Game Score Backend

Installation:
1. Make sure that MySQL is installed and running.
2. If you are on MacOS or another UNIX based system, run the command ```source setup``` to create the virtual environment and install the required modules. This will also populate the tables automatically. 

Running the Server:
1. Set the Flask App Variable with ```export FLASK_APP=flask_api```
2. Run the server with ```python3 -m flask run```

Adding new modules:
1. If you install a new python module in the virtual environment, you can run ```pip freeze -l > requirements.txt``` to update the ```requirements.txt``` document with all the new modules.