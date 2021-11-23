Game Score Backend

Installation (MySQL):
1. Make sure that MySQL is installed and running.
2. If you are on MacOS or another UNIX based system, run the command ```source setup``` to create the virtual environment and install the required modules. This will also populate the tables automatically. 

Installation (DynamoDB):
1. Make sure you have the AWS credentials in the location indicated in ```startserver``` or that they are set as your AWS CLI default profile. The tables have already been created and filled in the cloud so there's nothing else to do to set up.

Running the Server:
1. Run the script with `bash startserver`
   
Adding new modules:
1. If you install a new python module in the virtual environment, you can run ```pip freeze -l > requirements.txt``` to update the ```requirements.txt``` document with all the new modules.
