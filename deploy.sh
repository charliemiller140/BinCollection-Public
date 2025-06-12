#!/bin/bash

# Define project directory and zip file
PROJECT_DIR="$HOME/bin-collection"
ZIP_FILE="function.zip"

# Change to project directory
cd $PROJECT_DIR || { echo "Project directory not found!"; exit 1; }

# Remove any existing zip file
echo "Removing existing $ZIP_FILE..."
rm -f $ZIP_FILE

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found! Please create one with 'python -m venv venv'."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found!"
    exit 1
fi

# Install required packages into a temporary folder
echo "Installing dependencies..."
pip install -r requirements.txt --target ./package

# Navigate to the package directory
cd package

# Zip the dependencies
echo "Zipping dependencies..."
zip -r9 ../$ZIP_FILE .

# Go back to the project root directory
cd ..

# Add the lambda_function.py file to the zip
echo "Adding lambda_function.py to the zip..."
zip -g $ZIP_FILE lambda_function.py

# Upload the zip file to AWS Lambda
echo "Uploading to AWS Lambda..."
aws lambda update-function-code --function-name BinCollectionSkill --zip-file fileb://$ZIP_FILE

# Cleanup
echo "Cleaning up..."
rm -rf package

echo "Deployment complete!"
