import uuid
import os
import pandas as pd
from PIL import Image
import io
from datetime import datetime
import random

def generate_bug_id():
    """Creates a short unique ID for the bug"""
    return str(uuid.uuid4())[:8]

def save_bug_report(report):
    """Adds a new bug report to the CSV database"""
    # Make sure we have a CSV file to work with
    if not os.path.exists('bugs.csv'):
        df = pd.DataFrame(columns=['id', 'title', 'description', 'severity', 'type', 'status', 'reporter', 'screenshot', 'timestamp'])
        df.to_csv('bugs.csv', index=False)
    
    # Get existing bugs
    df = pd.read_csv('bugs.csv')
    
    # Add the new bug
    new_row = pd.DataFrame([report])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Write back to file
    df.to_csv('bugs.csv', index=False)

def save_screenshot(screenshot, file_path):
    """Saves uploaded image to the reports folder"""
    # Make sure folder exists
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Save the file
    img = Image.open(screenshot)
    img.save(file_path)

def load_bugs():
    """Reads bugs from CSV and sorts by date"""
    if os.path.exists('bugs.csv'):
        df = pd.read_csv('bugs.csv')
        if not df.empty and 'timestamp' in df.columns:
            # Sort newest first
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp', ascending=False)
        return df
    else:
        # Return empty DataFrame with the right columns
        return pd.DataFrame(columns=['id', 'title', 'description', 'severity', 'type', 'status', 'reporter', 'screenshot', 'timestamp'])

def filter_bugs(df, status_filters=None, type_filters=None):
    """Applies selected filters to the bug list"""
    filtered_df = df.copy()
    
    # Filter by status if any selected
    if status_filters and len(status_filters) > 0:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filters)]
        
    # Filter by bug type if any selected
    if type_filters and len(type_filters) > 0:
        filtered_df = filtered_df[filtered_df['type'].isin(type_filters)]
        
    return filtered_df

def generate_markdown_report(report):
    """Formats bug report as markdown for export"""
    timestamp = report.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    markdown = f"""# Bug Report: {report['title']}

## Details
- **Bug ID**: {report['id']}
- **Severity**: {report['severity']}
- **Type**: {report['type']}
- **Status**: {report['status']}
- **Reporter**: {report['reporter']}
- **Timestamp**: {timestamp}

## Description
{report['description']}

"""
    if report['screenshot']:
        markdown += f"## Screenshot\nFilename: {report['screenshot']}\n"
    
    return markdown

def get_bug_statistics(df):
    """Counts bugs by severity and type"""
    stats = {}
    
    if df.empty:
        return {
            'total': 0,
            'by_severity': {},
            'by_type': {}
        }
    
    stats['total'] = len(df)
    
    # Count bugs by severity level
    severity_counts = df['severity'].value_counts().to_dict()
    stats['by_severity'] = severity_counts
    
    # Count bugs by type
    type_counts = df['type'].value_counts().to_dict()
    stats['by_type'] = type_counts
    
    return stats

def generate_random_bug_title():
    """Picks a random title for untitled bug reports"""
    random_titles = [
        "Button not clickable",
        "Modal not closing",
        "Layout shifts on scroll",
        "Text overlapping in navbar",
        "Dropdown menu disappears",
        "Form submission fails",
        "Colors wrong on mobile",
        "Login redirect issue",
        "Image loading broken",
        "Scrolling performance issue"
    ]
    return random.choice(random_titles) 