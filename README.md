# Project 6: Acme Product Review Analyzer

An AI-powered review intelligence dashboard that analyzes customer reviews for sentiment, topics, and key insights. Perfect for product managers, marketers, and customer experience teams.

## Features

- **Sentiment Classification**: Identifies positive, neutral, or negative sentiment
- **Topic Detection**: Categorizes reviews by product features or themes
- **Text Summarization**: Creates concise summaries of review content
- **Interactive Dashboard**: Real-time visualization of review analytics
- **CSV Upload**: Batch processing of multiple reviews
- **Export Functionality**: Download results for reporting
- **Local Processing**: All analysis runs locally using Ollama LLMs - no external API dependencies

## Architecture

### Backend Components

1. **Sentiment Analyzer** (`backend/main.py`)
   - Classifies overall review sentiment
   - Identifies positive/negative indicators
   - Provides sentiment context

2. **Topic Detector** (`backend/main.py`)
   - Categorizes reviews by themes
   - Identifies product features mentioned
   - Groups similar reviews

3. **Summarizer** (`backend/main.py`)
   - Creates concise summaries
   - Extracts key points from reviews
   - Generates overview statistics

### Frontend Components

1. **Streamlit UI** (`frontend/app.py`)
   - User interface for review input
   - Results display and visualization
   - Dashboard with analytics

2. **Reusable Components** (`frontend/components.py`)
   - Modular UI elements
   - Consistent styling and layout

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local LLM inference)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd SchoolOfAI/Official/soai-06-product-review
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama** (if not already installed):
   ```bash
   # Install Ollama from https://ollama.com
   # Pull a model (mistral is recommended)
   ollama pull mistral
   # Start Ollama service
   ollama serve
   ```

## Running the Application

### Backend API

1. **Start the FastAPI backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Access the API**: Navigate to `http://localhost:8000` for API documentation

### Frontend UI

1. **Start the Streamlit application** (in a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

2. **Open your browser**: Navigate to `http://localhost:8501`

## Usage

### 1. Upload Reviews

- Paste product reviews in the text area
- Or upload a CSV file with multiple reviews
- Format: One review per line with text content

### 2. Analyze Reviews

- Click "Analyze" to process the reviews
- Wait for the AI to generate insights
- View the comprehensive results

### 3. Review Dashboard

- **Sentiment Distribution**: See positive, neutral, negative breakdown
- **Topic Cloud**: Visual representation of common themes
- **Summary Statistics**: Key metrics and insights
- **Individual Reviews**: Detailed analysis for each review

### 4. Export Results

- Copy summary for reports
- Export analysis as CSV or JSON
- Save for future reference

## Workflow

```
Upload Reviews → Backend API → Ollama LLM → Generate Analysis → Display Dashboard
     ↓               ↓            ↓                ↓                  ↓
  Paste text     FastAPI      Call model      Extract sentiment,   Show to
  or CSV         endpoint     with prompt   topics, summary   user
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=mistral
OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Ollama Models

The system supports any Ollama model. Recommended models:
- `mistral` - Lightweight and efficient for sentiment and topic analysis (default)

## Project Structure

```
soai-06-product-review/
├── backend/
│   └── main.py                  # FastAPI backend
├── frontend/
│   ├── app.py                    # Streamlit UI
│   └── components.py             # Reusable UI components
├── requirements.txt              # Python dependencies
└── README.md                   # This file
```

## Dependencies

- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `streamlit` - Web UI framework
- `requests` - HTTP client for Ollama API
- `python-dateutil` - Date/time parsing

## Troubleshooting

### Ollama Connection Issues

If you see connection errors:
1. Verify Ollama is running: `ollama list`
2. Check the API URL: `curl http://localhost:11434/api/generate`
3. Ensure the model is pulled: `ollama pull mistral`

### Backend API Issues

If the backend isn't responding:
1. Verify uvicorn is running: `ps aux | grep uvicorn`
2. Check the port isn't in use: `lsof -i :8000`
3. Review backend logs for errors

### Frontend Connection Issues

If the frontend can't connect to the backend:
1. Verify both services are running
2. Check the API URL in frontend/app.py
3. Ensure CORS is configured correctly

### Analysis Issues

If sentiment or topic detection isn't working:
1. Check that reviews are properly formatted
2. Verify the LLM model is appropriate
3. Review the prompts in backend/main.py
4. Try with a different model

### CSV Upload Issues

If CSV upload isn't working:
1. Verify CSV format matches expectations
2. Check that pandas is reading the file correctly
3. Review the upload functionality in frontend/app.py

### Slow Performance

For faster analysis:
1. Use mistral for speed
2. Reduce the number of reviews
3. Increase Ollama's GPU resources if available
4. Process reviews in smaller batches

## Use Cases

- **Product Management**: Track customer sentiment over time
- **Marketing Analysis**: Identify key themes in customer feedback
- **Competitive Intelligence**: Analyze competitor reviews
- **Customer Experience**: Monitor review sentiment trends
- **Quality Assurance**: Identify issues from negative reviews
- **Report Generation**: Create summaries for presentations

## Important Notes

- All processing happens locally - no data is sent to external servers
- Analysis quality depends on the quality and quantity of reviews
- Sentiment classification is AI-based and should be verified
- Topic detection works best with substantial review data
- Mistral is optimized for text analysis tasks

## License

This project is part of the School of AI curriculum.
