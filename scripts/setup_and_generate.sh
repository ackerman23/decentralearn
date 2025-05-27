#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r "$SCRIPT_DIR/requirements.txt"

# Run the documentation generation script
python "$SCRIPT_DIR/generate_docs.py"

# Deactivate virtual environment
deactivate

echo "Documentation generation complete. Check DecentraLearn_Documentation.docx" 