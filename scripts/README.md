# Documentation Generation Scripts

This directory contains scripts for generating and managing DecentraLearn documentation.

## Available Scripts

### `generate_docs.py`

Generates a comprehensive Word document containing all DecentraLearn documentation.

#### Usage

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   python generate_docs.py
   ```

3. The script will generate `DecentraLearn_Documentation.docx` in the current directory.

#### Features

- Combines all documentation files into a single Word document
- Maintains proper formatting and structure
- Includes table of contents
- Preserves code blocks and examples
- Adds page breaks between sections

## Requirements

- Python 3.8 or higher
- python-docx package
- markdown package

## Output

The generated Word document will include:

1. Development Setup Guide
2. Code Style Guide
3. Testing Guide
4. API Documentation
5. Architecture Documentation
6. Tutorials
7. Examples

## Notes

- The script assumes all documentation files are in their standard locations
- Make sure all documentation files are up to date before generating the document
- The generated document can be further customized using Microsoft Word 