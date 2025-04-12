# Perspective-Driven LinkedIn Post Generator

A service that generates LinkedIn posts reflecting a physician's perspective on healthcare AI topics using Google Gemini.

## Overview

This project implements an AI service that generates LinkedIn posts from a physician's perspective on healthcare AI topics. It takes an article summary or URL as input, applies the physician's perspective statements, and generates a LinkedIn post that reflects the client's "AI as enabler" philosophy.

## Features

- Uses Google Gemini 1.5 Pro for content generation
- Takes article summaries or URLs as input
- Applies supplied perspective statements to maintain consistent viewpoints
- Generates LinkedIn posts (200-250 words) reflecting the client's philosophy
- Includes a confidence score indicating alignment with the client's views
- Available as an API or command-line tool

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/perspective-post-generator.git
   cd perspective-post-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### API

Start the API server: 

```
python api.py
```
The API will be available at `http://localhost:8000`.  You can use the `/generate-post` endpoint to generate LinkedIn posts.

Example request:

json
{
"content": "A new AI algorithm developed by researchers at Stanford has shown 94% accuracy in detecting early-stage pancreatic cancer from routine CT scans, potentially improving survival rates through earlier intervention. The tool is designed to assist radiologists by flagging suspicious findings for further review, not to replace human expertise.",
"is_url": false,
"word_count": 225,
"perspectives": [
"AI should augment healthcare professionals, not replace them",
"Healthcare AI should focus on improving patient outcomes and experience"
]
}
```

### Command Line

Generate a post from an article summary:

```
python cli.py --input "Article summary text here"
```

Generate a post from an article URL:

```
python cli.py --input "https://www.example.com/article-url"
```

Generate a post from an article URL with custom perspectives:

```
python cli.py --input "https://www.example.com/article-url" --perspectives-file perspectives.txt
```

### Sample Tests

Run the sample tests to see example outputs:

```
python test_samples.py
```


## Project Structure

- `perspective_post_generator.py`: Core class for generating posts
- `api.py`: FastAPI implementation for serving the generator
- `cli.py`: Command-line interface
- `test_samples.py`: Sample test cases
- `design_decisions.md`: Documentation of design decisions and limitations

## Prompt Engineering Approach

The system uses a structured prompt with:

1. Clear sections for article content and physician perspectives
2. Explicit instructions for tone, length, and content structure
3. First-person voice to maintain authenticity
4. Specific output format requirements
5. Self-evaluation mechanism for confidence scoring

## Limitations and Future Work

See [design_decisions.md](design_decisions.md) for a detailed discussion of limitations and potential future improvements.

## Requirements

- Python 3.10
- Google Generative AI Python SDK
- FastAPI
- Uvicorn
- BeautifulSoup4
- Requests
- python-dotenv

## License

[MIT License](LICENSE)



