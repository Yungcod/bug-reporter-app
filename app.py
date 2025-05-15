import streamlit as st
import pandas as pd
import os
from datetime import datetime
from bug_utils import (
    generate_bug_id, 
    save_bug_report, 
    save_screenshot, 
    load_bugs, 
    filter_bugs, 
    generate_markdown_report, 
    get_bug_statistics,
    generate_random_bug_title
)

# Clean start for demo mode
if os.environ.get("CLEAR_BUGS") == "1" and os.path.exists("bugs.csv"):
    os.remove("bugs.csv")
    if os.path.exists("reports"):
        for file in os.listdir("reports"):
            os.remove(os.path.join("reports", file))

# Main page header
st.title("Bug Reporter")

# Get all bugs from database
bugs_df = load_bugs()

# Show stats at the top if we have any bugs
if not bugs_df.empty:
    st.subheader("Bug Statistics")
    stats = get_bug_statistics(bugs_df)
    
    # Layout in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Bugs", stats['total'])
    
    with col2:
        st.markdown("**Bugs by Severity**")
        for severity, count in stats['by_severity'].items():
            st.text(f"{severity}: {count}")
    
    with col3:
        st.markdown("**Bugs by Type**")
        for bug_type, count in stats['by_type'].items():
            st.text(f"{bug_type}: {count}")
    
    st.markdown("---")

# Track the currently submitted report
if 'current_bug_report' not in st.session_state:
    st.session_state.current_bug_report = None

# Bug submission form
with st.form("bug_report_form"):
    st.subheader("Submit a Bug Report")
    
    # Input fields
    title = st.text_input("Bug Title")
    description = st.text_area("Description")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    bug_type = st.selectbox("Bug Type", ["UI", "Functional", "Performance", "Security", "Content"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Rejected"])
    reporter = st.text_input("Reporter Name")
    screenshot = st.file_uploader("Upload Screenshot", type=["png", "jpg", "jpeg"])
    
    # Submit button at bottom of form
    submitted = st.form_submit_button("Submit Bug Report")
    
    if submitted:
        if description and reporter:
            # Fill in random title if empty
            if not title:
                title = generate_random_bug_title()
                
            # Create new bug ID
            bug_id = generate_bug_id()
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Handle screenshot if one was uploaded
            screenshot_file = None
            if screenshot:
                screenshot_file = f"reports/bug_{bug_id}.{screenshot.name.split('.')[-1]}"
                save_screenshot(screenshot, screenshot_file)
            
            # Put together the bug report
            report = {
                "id": bug_id,
                "title": title,
                "description": description,
                "severity": severity,
                "type": bug_type,
                "status": status,
                "reporter": reporter,
                "screenshot": screenshot_file,
                "timestamp": timestamp
            }
            save_bug_report(report)
            
            # Keep track of what we just submitted
            st.session_state.current_bug_report = report
            
            st.success(f"Bug report submitted successfully! Bug ID: {bug_id}")
            
            # Refresh our bug list
            bugs_df = load_bugs()
        else:
            st.error("Please fill in required fields: Description and Reporter Name")

# Show the submitted report details (after form, since download button can't be in a form)
if st.session_state.current_bug_report:
    report = st.session_state.current_bug_report
    
    st.subheader("Submitted Report")
    st.write(f"**Bug ID:** {report['id']}")
    st.write(f"**Title:** {report['title']}")
    st.write(f"**Description:** {report['description']}")
    st.write(f"**Severity:** {report['severity']}")
    st.write(f"**Type:** {report['type']}")
    st.write(f"**Status:** {report['status']}")
    st.write(f"**Reporter:** {report['reporter']}")
    st.write(f"**Time:** {report['timestamp']}")
    
    # Show screenshot if one was uploaded
    if report['screenshot']:
        if os.path.exists(report['screenshot']):
            st.image(report['screenshot'], caption="Uploaded Screenshot", use_column_width=True)
    
    # Add option to download as markdown
    markdown = generate_markdown_report(report)
    st.download_button(
        label="Download Bug Report as Markdown",
        data=markdown,
        file_name=f"bug_report_{report['id']}.md",
        mime="text/markdown"
    )

# Table of all bug reports with filtering options
st.subheader("All Bug Reports")
if not bugs_df.empty:
    # Filter dropdowns
    col1, col2 = st.columns(2)
    
    with col1:
        status_filters = st.multiselect(
            "Filter by Status",
            options=bugs_df['status'].unique()
        )
    
    with col2:
        type_filters = st.multiselect(
            "Filter by Bug Type",
            options=bugs_df['type'].unique()
        )
    
    # Apply any selected filters
    filtered_df = filter_bugs(bugs_df, status_filters, type_filters)
    
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.info("No bugs match the selected filters.")
else:
    st.info("No bug reports submitted yet.") 