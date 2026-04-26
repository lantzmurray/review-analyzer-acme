"""
Backend API for Product Review Analyzer using Mistral via Ollama.

This FastAPI application accepts product reviews (either individual or
bulk via CSV upload) and performs sentiment analysis to identify positive
and negative feedback patterns using the Mistral model.
"""

from fastapi import FastAPI, Form, UploadFile, File
import pandas as pd
import requests
import json

app = FastAPI()
OLLAMA_TIMEOUT_SECONDS = 1800

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def read_ollama_stream(response: requests.Response) -> str:
    """Read Ollama's streamed NDJSON chunks into one response string."""
    chunks = []
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        chunks.append(data.get("response", ""))
        if data.get("done"):
            break
    return "".join(chunks).strip()


def call_ollama(payload: dict) -> str:
    """Call Ollama with streaming enabled so long local generations stay alive."""
    streamed_payload = {**payload, "stream": True}
    with requests.post(
        OLLAMA_API_URL,
        json=streamed_payload,
        timeout=(10, OLLAMA_TIMEOUT_SECONDS),
        stream=True,
    ) as response:
        response.raise_for_status()
        return read_ollama_stream(response)

@app.post("/analyze/")
def analyze_reviews(text: str = Form(...)):
    """
    Analyze sentiment of product reviews.

    Uses Mistral to classify each review as positive, negative, or neutral
    and provides insights about common themes in the feedback.

    Args:
        text: Product review text (from HTML form data)

    Returns:
        A dictionary containing the sentiment analysis results
    """
    # Construct a detailed prompt for comprehensive review analysis
    # The prompt requests sentiment, key points, and a rating estimate
    # This multi-part request gives users actionable feedback
    prompt = (
        "Analyze this product review and provide:\n"
        "1. Sentiment (Positive/Negative/Neutral)\n"
        "2. Key points mentioned\n"
        "3. Rating (1-5 stars) estimate\n\n"
        f"Review: {text}"
    )

    # Send the review to Ollama's API for analysis.
    # The helper streams chunks from Ollama, then returns one complete analysis.
    result = call_ollama({
        "model": "mistral",  # Using mistral for sentiment analysis
        "prompt": prompt,     # The formatted prompt with review text
    })

    # Return the analysis in a structured format.
    return {"analysis": result}

@app.post("/analyze_csv/")
async def analyze_csv(file: UploadFile = File(...)):
    """
    Analyze multiple product reviews from a CSV file.

    Reads a CSV file containing reviews and processes each one
    to generate overall sentiment analysis and insights.

    Args:
        file: A CSV file containing product reviews

    Returns:
        A dictionary with analysis of all reviews
    """
    # Read the uploaded CSV file contents
    contents = await file.read()
    
    # Use io.BytesIO to read from the loaded memory bytes 
    # since await file.read() exhausted the file cursor
    import io
    df = pd.read_csv(io.BytesIO(contents))

    # Initialize a list to store results for each review
    results = []

    # Process each review in the CSV file
    for _, row in df.iterrows():
        # Extract the review text from either 'review' or 'text' column
        # Fallback to converting entire row to string if neither found
        review = row.get('review', row.get('text', str(row)))

        # Send each review to Ollama for individual analysis.
        analysis = call_ollama({
            "model": "mistral",  # Using mistral for sentiment analysis
            "prompt": f"Analyze this review: {review}",  # Concise prompt for batch processing
        })

        # Append the review and its analysis to results.
        results.append({
            "review": review,      # Original review text
            "analysis": analysis,  # AI-generated analysis
        })

    # Return all results for display on the frontend
    return {"results": results}
