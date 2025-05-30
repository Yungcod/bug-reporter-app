# Bug Reporter

A simple Streamlit application for tracking and managing bug reports.


https://bug-reporter-app.streamlit.app/

## Features

- Submit bug reports with title, description, severity, type, and status
- Upload screenshots for visual bug documentation
- View all submitted bug reports in a sortable table
- Filter bug reports by status and type
- Download individual bug reports as Markdown files
- View bug statistics and counts by category


## Screenshot 
![image](https://github.com/user-attachments/assets/03533525-5279-4a9c-bbd5-564974c04c67)


## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/bug-reporter-app.git
cd bug-reporter-app
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
streamlit run app.py
```

## How to Use

The app will open in your browser. From there you can:
- Fill out the bug report form with details about the issue
- Upload a screenshot if available
- Submit the report
- View your report and all existing reports in the table below
- Filter reports by status and type
- Download any report as a Markdown file

## Project Structure

- `app.py`: Main Streamlit interface
- `bug_utils.py`: Helper functions for data handling
- `requirements.txt`: Required Python packages

The app automatically creates:
- `bugs.csv`: Database file for storing bug reports
- `reports/`: Directory for storing uploaded screenshots

## Notes

This app runs entirely locally and doesn't use any external services.
It was designed as a practical tool for internal QA teams.

## Author

**Artur Arutinashvili**  
