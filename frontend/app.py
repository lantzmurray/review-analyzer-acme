"""
Frontend Application for Product Review Analyzer.

This Streamlit app provides an interface for analyzing product reviews.
Users can either enter individual reviews for quick analysis or upload
a CSV file containing multiple reviews for bulk processing.
"""

import os
import sys

import streamlit as st
import requests

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from components import render_app_footer, run_with_status_updates

# Set the main title of the Streamlit app
st.title("Product Review Analyzer (Mistral)")

# Create a radio button to select input type
# Users choose between single review or bulk CSV upload
option = st.radio("Select input type:", ("Single Review", "CSV Upload"))

# Handle single review analysis mode
if option == "Single Review":
    # Create a text area for entering a single product review
    # height=150 provides enough space for longer reviews
    review_text = st.text_area("Enter product review:", height=150)

    # Check if the user clicked the "Analyze Review" button
    if st.button("Analyze Review"):
        # Send the review text to the backend API for analysis
        response = run_with_status_updates(
            lambda: requests.post(
                "http://localhost:8000/analyze/",
                data={"text": review_text}
            ),
            start_message="Analyzing the product review..."
        )

        # Check if the request was successful (HTTP 200)
        if response.status_code == 200:
            # Extract the analysis from the JSON response
            analysis = response.json().get("analysis", "Error")

            # Display the analysis results section header
            st.subheader("Analysis Results:")

            # Render the analysis on the page
            st.write(analysis)
        else:
            # Display an error message if the backend request failed
            st.error("Error analyzing review. Make sure the backend is running.")

# Handle CSV bulk upload mode
else:
    # Create a file uploader for CSV files
    # Only accepts CSV files containing a 'review' column
    uploaded_file = st.file_uploader("Upload CSV file with 'review' column", type=["csv"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Check if the user clicked the "Analyze All Reviews" button
        if st.button("Analyze All Reviews"):
            # Prepare the file for upload - get raw bytes
            files = {"file": uploaded_file.getvalue()}

            # Show a keep-alive status while analysis is processing
            response = run_with_status_updates(
                lambda: requests.post(
                    "http://localhost:8000/analyze_csv/",
                    files=files
                ),
                start_message="Analyzing all reviews..."
            )

            # Check if the request was successful (HTTP 200)
            if response.status_code == 200:
                # Extract the list of results from the JSON response
                results = response.json().get("results", [])

                # Display each review with its analysis
                for i, r in enumerate(results, 1):
                    # Show review number as a subheader
                    st.subheader(f"Review {i}:")

                    # Display the original review text
                    st.write(f"**Original:** {r['review']}")

                    # Display the AI-generated analysis
                    st.write(f"**Analysis:** {r['analysis']}")

                    # Add a visual separator between reviews
                    st.write("---")
            else:
                # Display an error message if the backend request failed
                st.error("Error analyzing reviews. Make sure the backend is running.")


render_app_footer()
