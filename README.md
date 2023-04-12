# YouTube Transcript Summarizer

This project is a simple web application that takes a YouTube video URL as input, extracts the video's transcript, and uses the OpenAI API to generate a summary of the transcript's content. It's built using Flask, Pytube, and the YouTube Transcript API.

## Prerequisites

To run this project, you'll need:

- Python 3.6 or higher
- Pip (Python package manager)
- An OpenAI API key

## Installation

1. Clone this repository to your local machine and navigate to the root.
1. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
1. Set OpenAI API Key: 
```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Running the Application
1. Start the Flask application
    ```bash
    python app.py
    ```
1. Open your web browser and navigate to http://localhost:5000.
1. Enter a YouTube video URL and click "Summarize" to generate a summary of the video's transcript.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request or submit an issue.

