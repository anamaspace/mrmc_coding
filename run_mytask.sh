#!/bin/bash

# Install the virtualenv package
pip3 install virtualenv==16.4.0

# Create the virtual env
if test -f "mymrmc_task/bin/activate"; then
    echo "Virtual environment mymrmc_task is already created!"
else
    virtualenv -p python3 mymrmc_task
fi

# Activate the virtual env
source mymrmc_task/bin/activadte

# Install python packages
pip3 install -r requirements.txt

# Run task
echo "RUNNING: Wait while task runs."
python3 task.py > ./output/output_task.txt

# Deactivate the virtual env
deactivate

# Where you can find the results.
echo "OUTPUT: You can find the results in the output_task.txt file."


